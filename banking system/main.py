"""Main entry point for the banking system application."""
from domain.models import Customer, SavingsAccount, CurrentAccount, Account
from services.banking_service import BankingService
from services.loan_service import LoanService
from services.interest_strategies import SimpleInterest

def main():

    print("Welcome to the Banking System")
    
    customer = _get_customer_details()
    account = _create_account(customer)
    loan_service = _initialize_loan_service()


    _run_application_loop(customer, account, loan_service)

def _get_customer_details() -> Customer:
    print("\n--- Customer Registration ---")
    name = input("Enter Customer Name: ")
    email = input("Enter Customer Email: ")
    return Customer(name, email)

def _create_account(customer: Customer) -> Account:
    print("\n--- Account Creation ---")
    while True:
        choice = input("Choose Account Type (1: Savings, 2: Current): ")
        if choice == "1":
            print("Creating Savings Account with 3% Interest Rate.")
            initial_balance = _get_valid_amount("Enter Initial Deposit: ")
            return SavingsAccount(customer, initial_balance)
        elif choice == "2":
            print("Creating Current Account with $500 Overdraft Limit.")
            initial_balance = _get_valid_amount("Enter Initial Deposit: ")
            return CurrentAccount(customer, initial_balance)
        else:
            print("Invalid option. Please try again.")

def _initialize_loan_service() -> LoanService:
    return LoanService(SimpleInterest())

def _run_application_loop(customer: Customer, account: Account, loan_service: LoanService):
    while True:
        try:
            _display_menu_options()
            user_choice = input("Select option: ")
            
            should_continue = _process_user_command(user_choice, customer, account, loan_service)
            if not should_continue:
                break
                
        except Exception as e:
            print(f"Error occurred: {e}")

def _display_menu_options():
    print("\n--- Main Menu ---")
    print("1. Deposit Funds")
    print("2. Withdraw Funds")
    print("3. Check Balance")
    print("4. Apply for Loan")
    print("5. View Statement")
    print("6. Apply Interest (Savings Only)")
    print("7. Exit")

def _process_user_command(choice: str, customer: Customer, account: Account, loan_service: LoanService) -> bool:
    if choice == "1":
        _perform_deposit(account)
    elif choice == "2":
        _perform_withdrawal(account)
    elif choice == "3":
        _display_balance(account)
    elif choice == "4":
        _process_loan_application(customer, loan_service)
    elif choice == "5":
        _print_account_statement(account)
    elif choice == "6":
        if isinstance(account, SavingsAccount):
            account.add_interest()
            print("Interest added successfully.")
        else:
            print("This feature is only available for Savings Accounts.")
    elif choice == "7":
        print(f"Goodbye, {customer.name}!")
        return False
    else:
        print("Invalid choice. Please select a valid option from the menu.")
    
    return True

def _perform_deposit(account: Account):
    amount = _get_valid_amount("Enter amount to deposit: ")
    account.deposit(amount)
    print(f"Successfully deposited {amount:.2f}.")

def _perform_withdrawal(account: Account):
    amount = _get_valid_amount("Enter amount to withdraw: ")
    account.withdraw(amount)
    print(f"Successfully withdrawn {amount:.2f}.")

def _display_balance(account: Account):
    print(f"Current Balance: {account.balance:.2f}")

def _process_loan_application(customer: Customer, loan_service: LoanService):
    principal = _get_valid_amount("Enter Loan Amount: ")
    rate = _get_valid_amount("Enter Interest Rate (%): ")
    
    loan = loan_service.grant_loan(customer, principal, rate)
    interest_estimate = loan_service.get_interest_due(loan, 1)
    
    print("Loan granted successfully.")
    print(f"Estimated interest for 1 year: {interest_estimate:.2f}")

def _print_account_statement(account: Account):
    statement = BankingService.generate_account_statement(account)
    print(statement)

def _get_valid_amount(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            # Assuming validators handle detailed business logic validation,
            # but we can prevent simple negative inputs here for UI purposes if desired,
            # though validators exist in the domain layer.
            # We'll rely on domain validators catching errors, but strictly for "amount", it should be numeric.
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
