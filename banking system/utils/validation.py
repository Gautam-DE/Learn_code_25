from __future__ import annotations
from typing import Optional

from domain.exceptions import (
    AmountValidationError,
    EmptyFieldError,
    InsufficientFundsError,
)


def validate_positive_amount(amount: float, field_name: str) -> None:
    if amount <= 0:
        raise AmountValidationError(
            field_name=field_name,
            received_value=amount,
            constraint="must be greater than zero",
        )


def validate_non_negative_amount(amount: float, field_name: str) -> None:
    if amount < 0:
        raise AmountValidationError(
            field_name=field_name,
            received_value=amount,
            constraint="cannot be negative",
        )


def validate_non_empty_string(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise EmptyFieldError(field_name=field_name)


def validate_sufficient_funds(
    available: float,
    requested: float,
    account_ref: Optional[str] = None,
) -> None:
    if available < requested:
        raise InsufficientFundsError(
            available=available,
            requested=requested,
            account_ref=account_ref,
        )
