"""Module for marshmallow schemas."""
from marshmallow import Schema, fields, validates

from exceptions import TransactionValueError


class ParamsSchema(Schema):
    Amount = fields.Integer()
    IpAddress = fields.String()
    CardCryptogramPacket = fields.String()

    @validates('amount')
    def validate_amount(self, amount: int) -> None:
        """Validate amount of transaction, if it less than 0.01, then raise an exception.
        :param amount: Payment amount, Numeric, Required.
        :return: None
        """
        min_transaction_value = 0.01
        if amount < min_transaction_value:
            raise TransactionValueError(
                service=None,
                method=None,
                message='The amount parameter does not accept a transaction amount less than 0.01.',
            )
