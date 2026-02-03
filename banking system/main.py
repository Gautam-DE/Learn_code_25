from domain.models import Customer, SavingsAccount, CheckingAccount
from services.banking_service import BankingService
from services.loan_service import LoanService
from services.interest_strategies import SimpleInterest

def get_valid_amount(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input.")

def main():
    name = input("Enter Customer Name: ")
    email = input("Enter Customer Email: ")
    customer = Customer(name, email)
    
    while True:
        account_type = input("Choose Account Type (1: Savings, 2: Checking): ")
        initial_balance = get_valid_amount("Enter Initial Deposit: ")
        
        if account_type == "1":
            account = SavingsAccount(customer, initial_balance)
            break
        elif account_type == "2":
            account = CheckingAccount(customer, initial_balance)
            break
        else:
            print("Invalid option.")

    loan_service = LoanService(SimpleInterest())

    while True:
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Apply for Loan")
        print("5. Print Statement")
        print("6. Exit")
        
        choice = input("Select option: ")

        try:
            if choice == "1":
                amount = get_valid_amount("Amount: ")
                account.deposit(amount)
                print("Deposited.")

            elif choice == "2":
                amount = get_valid_amount("Amount: ")
                account.withdraw(amount)
                print("Withdrawn.")

            elif choice == "3":
                print(f"Balance: {account.balance}")

            elif choice == "4":
                principal = get_valid_amount("Loan Amount: ")
                rate = get_valid_amount("Interest Rate (%): ")
                loan = loan_service.grant_loan(customer, principal, rate)
                print(f"Loan granted. Interest for 1 year: {loan_service.get_interest_due(loan, 1)}")

            elif choice == "5":
                print(BankingService.generate_account_statement(account))

            elif choice == "6":
                break
            
            else:
                print("Invalid choice.")
        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
