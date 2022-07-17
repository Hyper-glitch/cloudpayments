"""Module for Cloudpayments API client."""
import uuid

import aiohttp

from abstract_client import AbstractInteractionClient
from exceptions import TransactionValueError, SuccessResponseError


class CloudPaymentsClient(AbstractInteractionClient):
    """Cloudpayments API client, inherited from AbstractInteractionClient."""
    BASE_URL = 'https://api.cloudpayments.ru/'
    SERVICE = 'CloudPayments'
    CONNECTOR = aiohttp.TCPConnector()

    def __init__(self, login, password):
        super().__init__()
        self.auth = aiohttp.BasicAuth(login=login, password=password, encoding='utf-8')
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Request-ID': str(uuid.uuid4()),
        }

    @staticmethod
    def validate_amount(amount: int) -> None:
        """Validate amount of transaction, if it less than 0.01, then raise an exception.
        :param amount: Payment amount, Numeric, Required.
        :return: None
        """
        min_transaction_value = 0.01
        if amount < min_transaction_value:
            raise TransactionValueError(
                service=None,
                method=None,
                message='The amount parameter does not accept a transaction amount less than 0.01.'
            )

    async def check_on_success(self, response: dict) -> None:
        """Raise an exception if response unsuccessful.
        :param response: - response from request.
        :return: None
        """
        if not response['Success']:
            raise SuccessResponseError(
                service=self.SERVICE,
                method=None,
                message=f'Something went wrong, please check response["Message"] or response["Model"]["ReasonCode"]',
            )

    async def charge(self, params: dict, one_stage_payment: bool = None) -> None:
        """
        Method for payment by data cryptogram result of encryption algorithm.
        :param params: Needed parameters for make a success request.
        :param one_stage_payment: flag, that define which payment we need to use.
        :return: None.
        """
        one_stage_endpoint = 'payments/cards/charge'
        two_stage_endpoint = 'payments/cards/auth'
        confirm_url = 'payments/confirm'
        amount = params['Amount']
        self.validate_amount(amount=amount)

        kwargs = {
            'params': params,
            'headers': self.headers,
            'auth': self.auth,
        }

        if one_stage_payment:
            url = self.endpoint_url(relative_url=one_stage_endpoint)
            response = await self.post(interaction_method='', url=url, **kwargs)
        else:
            first_step_url = self.endpoint_url(relative_url=two_stage_endpoint)
            response = await self.post(interaction_method='', url=first_step_url, **kwargs)
            await self.check_on_success(response=response)
            transaction_id = response['Model']['TransactionId']

            confirm_kwargs = {
                'TransactionId': transaction_id,
                'Amount': amount,
            }
            second_step_url = self.endpoint_url(relative_url=confirm_url)
            response = await self.post(interaction_method='', url=second_step_url, **confirm_kwargs)

        await self.close()
        await self.check_on_success(response=response)
