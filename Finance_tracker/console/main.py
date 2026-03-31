import os

from backend.adapters.console_notification_adapter import ConsoleNotificationAdapter
from backend.repositories.user_repository import UserRepository
from backend.repositories.transaction_repository import TransactionRepository
from backend.repositories.budget_repository import BudgetRepository
from backend.services.user_service import UserService
from backend.services.transaction_service import TransactionService
from backend.services.budget_service import BudgetService
from backend.services.report_service import ReportService
from backend.controllers.user_controller import UserController
from backend.controllers.transaction_controller import TransactionController
from backend.controllers.budget_controller import BudgetController
from backend.controllers.report_controller import ReportController
from console.handlers.user_handler import UserHandler
from console.handlers.transaction_handler import TransactionHandler
from console.handlers.budget_handler import BudgetHandler
from console.handlers.report_handler import ReportHandler
from console import menu

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_DATA_DIR = os.path.join(_PROJECT_ROOT, "data")


def _build_all_handlers():
    notification_port = ConsoleNotificationAdapter()

    user_repository = UserRepository(os.path.join(_DATA_DIR, "users.json"))
    transaction_repository = TransactionRepository(
        os.path.join(_DATA_DIR, "transactions.json")
    )
    budget_repository = BudgetRepository(os.path.join(_DATA_DIR, "budgets.json"))

    user_service = UserService(user_repository)
    budget_service = BudgetService(budget_repository)
    transaction_service = TransactionService(
        transaction_repository, budget_repository, notification_port
    )
    report_service = ReportService(transaction_repository)

    user_controller = UserController(user_service)
    transaction_controller = TransactionController(transaction_service)
    budget_controller = BudgetController(budget_service)
    report_controller = ReportController(report_service)

    return (
        UserHandler(user_controller),
        TransactionHandler(transaction_controller),
        BudgetHandler(budget_controller),
        ReportHandler(report_controller),
    )


def _require_active_user(active_user_id: str) -> bool:
    if not active_user_id:
        print("\nError: No active user. Please create a user (option 1) first,")
        print("then switch to them via option 5.")
        return False
    return True


def _run_user_section(user_handler: UserHandler) -> None:
    while True:
        menu.display_user_menu()
        choice = input("Choice: ").strip()
        if choice == "1":
            user_handler.handle_create_user()
        elif choice == "2":
            user_handler.handle_get_user()
        elif choice == "0":
            break


def _run_transaction_section(
    transaction_handler: TransactionHandler, active_user_id: str
) -> None:
    while True:
        menu.display_transaction_menu()
        choice = input("Choice: ").strip()
        if choice == "1":
            transaction_handler.handle_add_transaction(active_user_id)
        elif choice == "2":
            transaction_handler.handle_get_transactions(active_user_id)
        elif choice == "3":
            transaction_handler.handle_delete_transaction()
        elif choice == "0":
            break


def _run_budget_section(
    budget_handler: BudgetHandler, active_user_id: str
) -> None:
    while True:
        menu.display_budget_menu()
        choice = input("Choice: ").strip()
        if choice == "1":
            budget_handler.handle_set_budget(active_user_id)
        elif choice == "2":
            budget_handler.handle_get_budgets(active_user_id)
        elif choice == "0":
            break


def _run_report_section(
    report_handler: ReportHandler, active_user_id: str
) -> None:
    while True:
        menu.display_report_menu()
        choice = input("Choice: ").strip()
        if choice == "1":
            report_handler.handle_monthly_summary(active_user_id)
        elif choice == "0":
            break


def run() -> None:
    user_handler, transaction_handler, budget_handler, report_handler = (
        _build_all_handlers()
    )
    active_user_id = ""

    print("\nWelcome to Personal Finance Tracker!")

    while True:
        if active_user_id:
            print(f"\n[Active User ID: ...{active_user_id[-8:]}]")

        menu.display_main_menu()
        choice = input("Choice: ").strip()

        if choice == "1":
            _run_user_section(user_handler)

        elif choice == "2":
            if _require_active_user(active_user_id):
                _run_transaction_section(transaction_handler, active_user_id)

        elif choice == "3":
            if _require_active_user(active_user_id):
                _run_budget_section(budget_handler, active_user_id)

        elif choice == "4":
            if _require_active_user(active_user_id):
                _run_report_section(report_handler, active_user_id)

        elif choice == "5":
            active_user_id = input("Enter User ID: ").strip()
            print("Success: Active user switched.")

        elif choice == "0":
            print("\nGoodbye.\n")
            break
