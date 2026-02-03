from domain.models import Account, Transaction
from utils.validators import validate_positive_amount, validate_sufficient_funds

class BankingService:
    """
    Service responsible for banking operations like transfers and account management logic.
    """

    @staticmethod
    def transfer_funds(sender: Account, receiver: Account, amount: float) -> None:
        validate_positive_amount(amount, "Transfer Amount")
        validate_sufficient_funds(sender.balance, amount)

        sender.withdraw(amount)
        receiver.deposit(amount)

        # Update descriptions
        sender.transactions[-1].description = f"Transfer to {receiver.account_number}"
        receiver.transactions[-1].description = f"Transfer from {sender.account_number}"

    @staticmethod
    def generate_account_statement(account: Account) -> str:
        """Generates a printable statement for the account."""
        statement = f"\n--- Account Statement: {account.account_number} ({account.get_account_type()}) ---\n"
        statement += f"Owner: {account.customer.name}\n"
        statement += f"Current Balance: {account.balance}\n"
        statement += "Transactions:\n"
        for txn in account.transactions:
            statement += f"  {txn}\n"
        return statement
