"""Module for Cloudpayments API client."""
import urllib.parse as urllib

from aiohttp import BasicAuth

from abstract_client import AbstractInteractionClient, BaseInteractionError


class TransactionValueError(BaseInteractionError):
    pass


class CloudPaymentsClient(AbstractInteractionClient):
    """Cloudpayments API client, inherited from AbstractInteractionClient."""
    BASE_URL = 'https://api.cloudpayments.ru/'
    SERVICE = 'CloudPayments'

    def __int__(self):
        self.test_url = urllib.urljoin(self.BASE_URL, 'test')
        self.cloudpayments_session = self.create_session()

    def validate_amount(self, amount):
        min_transaction_value = 0.01
        if amount < min_transaction_value:
            raise TransactionValueError(
                service=self.SERVICE,
                method=None,
                message='The amount parameter does not accept a transaction amount less than 0.01.',
            )

    def charge(self, auth: BasicAuth, headers: dict, params: dict, one_stage_payment: bool = None):
        """
        Method for payment by payment data cryptogram result of encryption algorithm.
        :param one_stage_payment: flag, that define which payment we need to use.
        :return: None
        """
        one_stage_endpoint = 'payments/cards/charge'
        two_stage_endpoint = 'payments/cards/auth'

        if one_stage_payment:
            url = self.endpoint_url(relative_url=one_stage_endpoint)
        else:
            url = self.endpoint_url(relative_url=two_stage_endpoint)

        self.validate_amount(params['Amount'])
        response = await self.post(interaction_method='', url=url, **params)  # maybe we should use asyncio

        if response['Success']:
            token = ''
