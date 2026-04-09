from domain.models import Account
from utils.validation import validate_positive_amount


class TransferService:
    def transfer(self, sender: Account, receiver: Account, amount: float) -> None:
        validate_positive_amount(amount, "Transfer Amount")

        sender.debit_transfer(amount, receiver.account_number)
        receiver.credit_transfer(amount, sender.account_number)
