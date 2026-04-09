from domain.models import Account
from services.statement_service import StatementService
from services.transfer_service import TransferService


class BankingService:
    """Facade that coordinates specialized banking services.

    This keeps backward compatibility for callers that expect a single entry point,
    while delegating concrete behavior to focused services.
    """

    def __init__(
        self,
        transfer_service: TransferService | None = None,
        statement_service: StatementService | None = None,
    ) -> None:
        self._transfer_service = transfer_service or TransferService()
        self._statement_service = statement_service or StatementService()

    def transfer_funds(self, sender: Account, receiver: Account, amount: float) -> None:
        self._transfer_service.transfer(sender, receiver, amount)

    def generate_account_statement(self, account: Account) -> str:
        return self._statement_service.generate(account)
