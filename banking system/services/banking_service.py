"""Banking Service Module."""
from domain.models import Account
from utils.validation import validate_positive_amount, validate_sufficient_funds

class BankingService:

    @staticmethod
    def transfer_funds(sender: Account, receiver: Account, amount: float) -> None:
        BankingService._validate_transfer(sender, amount)
        
        BankingService._process_transfer_transaction(sender, receiver, amount)
        BankingService._update_transaction_descriptions(sender, receiver)

    @staticmethod
    def generate_account_statement(account: Account) -> str:
        header = f"\n--- Account Statement: {account.account_number} ({account.get_account_type()}) ---\n"
        owner_info = f"Owner: {account.customer.name}\n"
        balance_info = f"Current Balance: {account.balance}\n"
        
        transactions_list = "Transactions:\n"
        for txn in account.transactions:
            transactions_list += f"  {txn}\n"
            
        return header + owner_info + balance_info + transactions_list

    @staticmethod
    def _validate_transfer(sender: Account, amount: float):
        validate_positive_amount(amount, "Transfer Amount")
        validate_sufficient_funds(sender.balance, amount)

    @staticmethod
    def _process_transfer_transaction(sender: Account, receiver: Account, amount: float):
        sender.withdraw(amount)
        receiver.deposit(amount)

    @staticmethod
    def _update_transaction_descriptions(sender: Account, receiver: Account):
        # This assumes the last transaction is the one we just made.
        # In a real system, we'd pass the transaction object back or use IDs.
        if sender.transactions:
            sender.transactions[-1].description = f"Transfer to {receiver.account_number}"
        if receiver.transactions:
            receiver.transactions[-1].description = f"Transfer from {sender.account_number}"
