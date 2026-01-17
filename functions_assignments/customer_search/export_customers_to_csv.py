from typing import List
from .customer_model import Customer


class CustomerCsvExporter:
    def convert_to_csv(self, customers: List[Customer]) -> str:
        csv_rows = []
        for customer in customers:
            csv_rows.append(
                f"{customer.customer_id},"
                f"{customer.company_name},"
                f"{customer.contact_name},"
                f"{customer.country}"
            )
        return "\n".join(csv_rows)

