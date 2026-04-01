from backend.services.report_service import ReportService


class ReportController:
    def __init__(self, report_service: ReportService):
        self._service = report_service

    def get_monthly_summary(self, user_id: str, month: str) -> dict:
        return self._service.get_monthly_summary(user_id, month)
