from domain.models import Account


class StatementService:
    _SEPARATOR = "=" * 62

    def generate(self, account: Account) -> str:
        sections = [
            self._build_header(account),
            self._build_owner_section(account),
            self._build_balance_section(account),
            self._build_transactions_section(account),
            self._SEPARATOR,
        ]
        return "\n".join(sections)

    def _build_header(self, account: Account) -> str:
        return (
            f"\n{self._SEPARATOR}\n"
            f"  Account Statement - {account.get_account_type()} Account\n"
            f"  Number : {account.account_number}\n"
            f"{self._SEPARATOR}"
        )

    def _build_owner_section(self, account: Account) -> str:
        return (
            f"  Owner  : {account.customer.name}\n"
            f"  Email  : {account.customer.email}"
        )

    def _build_balance_section(self, account: Account) -> str:
        return f"\n  Current Balance : ${account.balance:>10.2f}\n"

    def _build_transactions_section(self, account: Account) -> str:
        transactions = account.transactions
        if not transactions:
            return "  No transactions recorded yet.\n"

        col_header = (
            f"  {'Date & Time':<22}"
            f"{'Type':<18}"
            f"{'Amount':>10}  "
            f"Description"
        )
        divider = "  " + "-" * 58
        rows    = [f"  {txn}" for txn in transactions]
        return "\n".join([col_header, divider] + rows) + "\n"
