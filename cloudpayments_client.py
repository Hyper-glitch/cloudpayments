"""Module for Cloudpayments API client."""
import urllib.parse as urllib
import uuid

import aiohttp

from abstract_client import AbstractInteractionClient, BaseInteractionError


class TransactionValueError(BaseInteractionError):
    pass


class CloudPaymentsClient(AbstractInteractionClient):
    """Cloudpayments API client, inherited from AbstractInteractionClient."""
    BASE_URL = 'https://api.cloudpayments.ru/'
    SERVICE = 'CloudPayments'

    def __init__(self, login, password):
        super().__init__()
        self.test_url = urllib.urljoin(self.BASE_URL, 'test')
        self.cloudpayments_session = self.create_session()
        self.auth = aiohttp.BasicAuth(login=login, password=password, encoding='utf-8')
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Request-ID': str(uuid.uuid4()),
        }

    def validate_amount(self, amount: int) -> None:
        """Validate amount of transaction, if it less than 0.01, then raise an exception."""
        min_transaction_value = 0.01
        if amount < min_transaction_value:
            raise TransactionValueError(
                service=self.SERVICE,
                method=None,
                message='The amount parameter does not accept a transaction amount less than 0.01.',
            )

    async def charge(self, params: dict, one_stage_payment: bool = None):
        """
        Method for payment by payment data cryptogram result of encryption algorithm.
        :param params: Needed parameters for make a success request.
        :param auth: Basic access authentication, that contains login and password.
        :param one_stage_payment: flag, that define which payment we need to use.
        :return: None
        """
        one_stage_endpoint = 'payments/cards/charge'
        two_stage_endpoint = 'payments/cards/auth'

        self.validate_amount(params['Amount'])

        kwargs = {
            'params': params,
            'headers': self.headers,
            'auth': self.auth,
        }

        if one_stage_payment:
            url = self.endpoint_url(relative_url=one_stage_endpoint)
        else:
            url = self.endpoint_url(relative_url=two_stage_endpoint)

        response = await self.post(interaction_method='', url=url, **kwargs)  # maybe we should use asyncio

        if response['Success']:
            token = ''
