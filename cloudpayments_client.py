"""Module for Cloudpayments API client."""
import uuid

import aiohttp
from marshmallow import ValidationError

from abstract_client import AbstractInteractionClient
from marshmallow_schemas import ParamsSchema, SuccessfulResponseSchema


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

    async def check_on_success(self, response: dict) -> dict:
        """Raise an exception if response unsuccessful.
        :param response: - response from request.
        :return: successfully deserialized object.
        """
        try:
            return SuccessfulResponseSchema().load(response)
        except ValidationError as error:
            print(error.messages)
            raise ValidationError

    async def charge(self, raw_params: dict, one_stage_payment: bool = None) -> None:
        """
        Method for payment by data cryptogram result of encryption algorithm.
        :param raw_params: Needed parameters for make a success request.
        :param one_stage_payment: flag, that define which payment we need to use.
        :return: None.
        """
        one_stage_endpoint = 'payments/cards/charge'
        two_stage_endpoint = 'payments/cards/auth'
        confirm_url = 'payments/confirm'
        params = ParamsSchema().dumps(raw_params)

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
            deserialized_response = await self.check_on_success(response=response)
            transaction_id = deserialized_response['Model']['TransactionId']

            confirm_kwargs = {
                'TransactionId': transaction_id,
                'Amount': raw_params['Amount'],
            }
            second_step_url = self.endpoint_url(relative_url=confirm_url)
            response = await self.post(interaction_method='', url=second_step_url, **confirm_kwargs)

        await self.close()
        await self.check_on_success(response=response)
