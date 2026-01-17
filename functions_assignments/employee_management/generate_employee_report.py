from typing import List
import xml.etree.ElementTree as ET
import csv
import io
from .employee import Employee


class EmployeeReportGenerator:
    def generate_employee_xml_report(self, employee: Employee) -> str:
        xml_root = ET.Element("Employee")
        ET.SubElement(xml_root, "ID").text = str(employee.employee_id)
        ET.SubElement(xml_root, "Name").text = employee.name
        ET.SubElement(xml_root, "Department").text = employee.department
        ET.SubElement(xml_root, "IsWorking").text = str(employee.is_active)
        ET.indent(xml_root)
        return ET.tostring(xml_root, encoding='unicode')

    def generate_employee_csv_report(self, employee: Employee) -> str:
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["ID", "Name", "Department", "IsWorking"])
        writer.writerow([
            employee.employee_id,
            employee.name,
            employee.department,
            employee.is_active
        ])
        return csv_buffer.getvalue()

    def generate_employees_xml_report(self, employees: List[Employee]) -> str:
        xml_root = ET.Element("Employees")
        for employee in employees:
            employee_element = ET.SubElement(xml_root, "Employee")
            ET.SubElement(employee_element, "ID").text = str(employee.employee_id)
            ET.SubElement(employee_element, "Name").text = employee.name
            ET.SubElement(employee_element, "Department").text = employee.department
            ET.SubElement(employee_element, "IsWorking").text = str(employee.is_active)
        ET.indent(xml_root)
        return ET.tostring(xml_root, encoding='unicode')

    def generate_employees_csv_report(self, employees: List[Employee]) -> str:
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["ID", "Name", "Department", "IsWorking"])
        for employee in employees:
            writer.writerow([
                employee.employee_id,
                employee.name,
                employee.department,
                employee.is_active
            ])
        return csv_buffer.getvalue()

