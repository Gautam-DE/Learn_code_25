from backend.controllers.report_controller import ReportController


class ReportHandler:
    def __init__(self, report_controller: ReportController):
        self._controller = report_controller

    def handle_monthly_summary(self, user_id: str) -> None:
        print("\nMonthly Financial Summary")
        month = input("Month (YYYY-MM) : ").strip()
        summary = self._controller.get_monthly_summary(user_id, month)
        self._display_summary(summary)



    def _display_summary(self, summary: dict) -> None:
        print(f"\nReport for {summary['month']}")
        print(f"Total Income  : ₹{summary['total_income']:.2f}")
        print(f"Total Expense : ₹{summary['total_expense']:.2f}")
        print(f"Net Savings   : ₹{summary['savings']:.2f}")
        print(f"Transactions  : {summary['transaction_count']}")
