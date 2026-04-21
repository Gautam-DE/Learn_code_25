from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List, Protocol
import xml.etree.ElementTree as ET

from Core.models import Record


class Exporter(Protocol):
    def export(self, file_path: str, records: List[Record]) -> None:
        ...


class CsvExporter:
    def export(self, file_path: str, records: List[Record]) -> None:
        path = Path(file_path)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["ID", "NAME", "VALUE", "DATE", "DOUBLED_VALUE", "SQUARED_VALUE"])
            for record in records:
                doubled = record.value * 2
                squared = record.value * record.value
                date_text = record.date.strftime("%Y-%m-%d") if record.date else ""
                writer.writerow([record.id, record.name, record.value, date_text, doubled, squared])


class JsonExporter:
    def export(self, file_path: str, records: List[Record]) -> None:
        payload = []
        for record in records:
            payload.append(
                {
                    "id": record.id,
                    "name": record.name,
                    "value": record.value,
                    "date": record.date.strftime("%Y-%m-%d") if record.date else None,
                    "doubled_value": record.value * 2,
                    "squared_value": record.value * record.value,
                }
            )

        Path(file_path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


class XmlExporter:
    def export(self, file_path: str, records: List[Record]) -> None:
        root = ET.Element("records")
        for record in records:
            node = ET.SubElement(root, "record")
            ET.SubElement(node, "id").text = record.id
            ET.SubElement(node, "name").text = record.name
            ET.SubElement(node, "value").text = str(record.value)
            ET.SubElement(node, "date").text = record.date.strftime("%Y-%m-%d") if record.date else ""
            ET.SubElement(node, "doubled_value").text = str(record.value * 2)
            ET.SubElement(node, "squared_value").text = str(record.value * record.value)

        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)


class ExporterRegistry:
    def __init__(self) -> None:
        self._exporters: Dict[str, Exporter] = {}

    def register(self, format_name: str, exporter: Exporter) -> None:
        self._exporters[format_name.lower()] = exporter

    def get(self, format_name: str) -> Exporter:
        key = format_name.lower()
        if key not in self._exporters:
            raise ValueError(f"Unsupported format: {format_name}")
        return self._exporters[key]
