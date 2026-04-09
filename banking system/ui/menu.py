from __future__ import annotations

from typing import Callable, Dict, Optional, Tuple

from domain.exceptions import BankingError
from domain.models import Account, Customer, Loan, SavingsAccount, CurrentAccount
from services.loan_service import LoanService
from services.statement_service import StatementService
from services.transfer_service import TransferService
from ui.input_parser import read_non_negative_amount, read_positive_amount


class MenuController:
    def __init__(
        self,
        customer: Customer,
        primary_account: Account,
        secondary_account: Account,
        loan_service: LoanService,
        transfer_service: TransferService,
        statement_service: StatementService,
    ) -> None:
        self._customer          = customer
        self._account           = primary_account
        self._secondary_account = secondary_account
        self._loan_service      = loan_service
        self._transfer_service  = transfer_service
        self._statement_service = statement_service
        self._active_loan: Optional[Loan] = None
        self._is_running        = True

        self._commands: Dict[str, Tuple[str, Callable[[], None]]] = {
            "1": ("Deposit Funds",               self._handle_deposit),
            "2": ("Withdraw Funds",              self._handle_withdrawal),
            "3": ("Check Balance",               self._handle_balance_check),
            "4": ("Transfer to Savings Account", self._handle_transfer),
            "5": ("Apply for Loan",              self._handle_loan_application),
            "6": ("Repay Loan",                  self._handle_loan_repayment),
            "7": ("Apply Monthly Interest",      self._handle_interest),
            "8": ("View Account Statement",      self._handle_primary_statement),
            "9": ("View Savings Statement",      self._handle_secondary_statement),
            "0": ("Exit",                        self._handle_exit),
        }

    def run(self) -> None:
        self._print_welcome_banner()
        while self._is_running:
            self._display_menu()
            choice = input("\n  Select option: ").strip()
            self._execute_command(choice)

    def _print_welcome_banner(self) -> None:
        print(f"\n  Welcome back, {self._customer.name}!")
        print(f"  Primary Account  : {self._account.get_account_type()} "
              f"[{self._account.account_number[:8]}]")
        print(f"  Savings Account  : {self._secondary_account.get_account_type()} "
              f"[{self._secondary_account.account_number[:8]}]")

    def _display_menu(self) -> None:
        print("\n" + "-" * 42)
        print("  MAIN MENU")
        print("-" * 42)
        for key, (label, _) in self._commands.items():
            print(f"  [{key}]  {label}")
        print("-" * 42)

    def _execute_command(self, choice: str) -> None:
        command_entry = self._commands.get(choice)
        if command_entry is None:
            print("  Invalid option. Please choose a number from the menu.")
            return

        _, handler = command_entry
        try:
            handler()
        except BankingError as known_error:
            print(f"\n  Error: {known_error}")

    def _handle_deposit(self) -> None:
        amount = read_positive_amount("  Deposit amount: $")
        self._account.deposit(amount)
        print(f"  Deposited ${amount:.2f}. New balance: ${self._account.balance:.2f}")

    def _handle_withdrawal(self) -> None:
        amount = read_positive_amount("  Withdrawal amount: $")
        self._account.withdraw(amount)
        print(f"  Withdrew ${amount:.2f}. New balance: ${self._account.balance:.2f}")

    def _handle_balance_check(self) -> None:
        acct_type = self._account.get_account_type()
        print(f"\n  {acct_type} Account Balance : ${self._account.balance:.2f}")
        if isinstance(self._account, CurrentAccount):
            available = self._account.balance + self._account.overdraft_limit
            print(f"  Available (incl. ${self._account.overdraft_limit:.0f} overdraft): ${available:.2f}")
        print(f"  Savings Account Balance  : ${self._secondary_account.balance:.2f}")

    def _handle_transfer(self) -> None:
        print(f"\n  Transferring from {self._account.get_account_type()} "
              f"[{self._account.account_number[:8]}]"
              f"  to Savings [{self._secondary_account.account_number[:8]}]")
        amount = read_positive_amount("  Transfer amount: $")
        self._transfer_service.transfer(self._account, self._secondary_account, amount)
        print(f"  Transferred ${amount:.2f}.")
        print(f"     Primary balance : ${self._account.balance:.2f}")
        print(f"     Savings balance : ${self._secondary_account.balance:.2f}")

    def _handle_loan_application(self) -> None:
        principal = read_positive_amount("  Loan amount: $")
        rate      = read_non_negative_amount("  Annual interest rate (%): ")
        self._active_loan = self._loan_service.create_loan(self._customer, principal, rate)
        year_1_interest   = self._loan_service.calculate_interest_due(self._active_loan, 1)
        print(f"  Loan granted: ${principal:.2f} at {rate}% p.a.")
        print(f"     Year-1 interest estimate : ${year_1_interest:.2f}")
        print(f"     Outstanding balance      : ${self._active_loan.outstanding_balance:.2f}")

    def _handle_loan_repayment(self) -> None:
        if self._active_loan is None or not self._active_loan.is_active:
            print("  No active loan on this account. Apply for one first (option 5).")
            return
        print(f"  Outstanding loan balance: ${self._active_loan.outstanding_balance:.2f}")
        amount = read_positive_amount("  Repayment amount: $")
        self._loan_service.repay_loan(self._active_loan, amount)
        if not self._active_loan.is_active:
            print(f"  Loan fully repaid. Status: {self._active_loan.status.value}")
        else:
            print(f"  Repaid ${amount:.2f}. "
                  f"Remaining: ${self._active_loan.outstanding_balance:.2f}")

    def _handle_interest(self) -> None:
        if not isinstance(self._secondary_account, SavingsAccount):
            print("  The linked savings account does not support interest.")
            return
        txn      = self._secondary_account.apply_monthly_interest()
        rate_pct = self._secondary_account.interest_rate * 100
        print(f"  Interest credited at {rate_pct:.1f}%: +${txn.amount:.2f}")
        print(f"     New savings balance: ${self._secondary_account.balance:.2f}")

    def _handle_primary_statement(self) -> None:
        print(self._statement_service.generate(self._account))

    def _handle_secondary_statement(self) -> None:
        print(self._statement_service.generate(self._secondary_account))

    def _handle_exit(self) -> None:
        print(f"\n  Goodbye, {self._customer.name}! Thank you for banking with us.\n")
        self._is_running = False
