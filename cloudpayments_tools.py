"""Module with helpful tools."""
from exceptions import TransactionValueError


def validate_amount(amount: int) -> int:
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
    return amount
