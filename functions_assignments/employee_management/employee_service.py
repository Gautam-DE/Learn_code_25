from .employee_model import Employee
from .repository import EmployeeRepository


class EmployeeStatus:
    def terminate(self, employee: Employee) -> None:
        employee.is_active = False

    def is_working(self, employee: Employee) -> bool:
        return employee.is_active


class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    def terminate_employee(self, employee: Employee) -> bool:
        employee.is_active = False
        return self._repository.update_employee(employee)

    def is_working(self, employee: Employee) -> bool:
        return employee.is_active

    def activate_employee(self, employee: Employee) -> bool:
        employee.is_active = True
        return self._repository.update_employee(employee)

