"""Validation Utilities."""

class ValidationError(Exception):
    pass

def validate_positive_amount(amount: float, name: str):
    if amount <= 0:
        raise ValidationError(f"{name} must be greater than zero.")

def validate_non_empty_string(value: str, name: str):
    if not value or not value.strip():
        raise ValidationError(f"{name} cannot be empty.")

def validate_sufficient_funds(balance: float, amount: float):
    if balance < amount:
        raise ValidationError("Insufficient funds for this transaction.")
