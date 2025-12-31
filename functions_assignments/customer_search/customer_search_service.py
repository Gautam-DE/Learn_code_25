from typing import List, Callable
from .customer_model import Customer


class CustomerSearch:
    def __init__(self, customer_database):
        self.customer_database = customer_database

    def search_by_country(self, country: str) -> List[Customer]:
        return self._search(lambda customer: country in customer.country)

    def search_by_company_name(self, company_name: str) -> List[Customer]:
        return self._search(lambda customer: company_name in customer.company_name)

    def search_by_contact_name(self, contact_name: str) -> List[Customer]:
        return self._search(lambda customer: contact_name in customer.contact_name)

    def _search(self, filter_predicate: Callable[[Customer], bool]) -> List[Customer]:
        return sorted(
            filter(filter_predicate, self.customer_database.customers),
            key=lambda customer: customer.customer_id
        )

