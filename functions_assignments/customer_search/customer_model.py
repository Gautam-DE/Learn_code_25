from typing import List


class Customer:
    def __init__(self, customer_id: str, company_name: str, contact_name: str, country: str):
        self.customer_id = customer_id
        self.company_name = company_name
        self.contact_name = contact_name
        self.country = country

