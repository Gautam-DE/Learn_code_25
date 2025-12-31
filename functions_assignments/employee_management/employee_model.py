class Employee:
    def __init__(self, employee_id: int, name: str, department: str, is_active: bool = True):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.is_active = is_active

