from domain.exceptions import BankingError
from domain.models import Customer, SavingsAccount, CurrentAccount, Account
from services.interest_strategies import SimpleInterest
from services.loan_service import LoanService
from services.statement_service import StatementService
from services.transfer_service import TransferService
from ui.input_parser import read_non_empty_string, read_positive_amount
from ui.menu import MenuController


def main() -> None:
    _print_startup_banner()
    customer          = _register_customer()
    primary_account   = _open_primary_account(customer)
    secondary_account = _open_savings_account(customer)
    controller        = _build_controller(customer, primary_account, secondary_account)
    controller.run()


def _print_startup_banner() -> None:
    print("=" * 50)
    print("        Clean Bank - Banking System")
    print("=" * 50)


def _register_customer() -> Customer:
    print("\n--- New Customer Registration ---")
    while True:
        try:
            name  = read_non_empty_string("  Full name  : ")
            email = read_non_empty_string("  Email      : ")
            return Customer(name, email)
        except BankingError as error:
            print(f"  Registration error: {error}")


def _open_primary_account(customer: Customer) -> Account:
    print("\n--- Open Your Primary Account ---")
    while True:
        print("  [1]  Savings Account  (3% interest rate)")
        print("  [2]  Current Account  ($500 overdraft limit)")
        choice = input("  Select account type: ").strip()
        try:
            if choice == "1":
                return _create_savings_account(customer, "  Initial deposit: $")
            elif choice == "2":
                return _create_current_account(customer)
            else:
                print("  Please enter 1 or 2.")
        except BankingError as error:
            print(f"  {error}")


def _open_savings_account(customer: Customer) -> SavingsAccount:
    print("\n--- Linked Savings Account ---")
    return _create_savings_account(customer, "  Initial savings deposit: $")


def _create_savings_account(customer: Customer, prompt: str) -> SavingsAccount:
    initial = read_positive_amount(prompt)
    account = SavingsAccount(customer, initial)
    print(f"  Savings account opened. Number: {account.account_number[:8]}")
    return account


def _create_current_account(customer: Customer) -> CurrentAccount:
    initial = read_positive_amount("  Initial deposit: $")
    account = CurrentAccount(customer, initial)
    print(f"  Current account opened. Number: {account.account_number[:8]}")
    return account


def _build_controller(
    customer: Customer,
    primary_account: Account,
    secondary_account: Account,
) -> MenuController:
    loan_service      = LoanService(SimpleInterest())
    transfer_service  = TransferService()
    statement_service = StatementService()

    return MenuController(
        customer          = customer,
        primary_account   = primary_account,
        secondary_account = secondary_account,
        loan_service      = loan_service,
        transfer_service  = transfer_service,
        statement_service = statement_service,
    )


if __name__ == "__main__":
    main()
