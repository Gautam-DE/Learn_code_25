from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional, Tuple

from Core.models import Record


class CsvRecordParser:
    def parse_lines(self, lines: List[str]) -> Tuple[List[Record], List[str]]:
        parsed_records: List[Record] = []
        errors: List[str] = []

        for line in lines:
            if not line or not line.strip():
                continue

            parts = [part.strip() for part in line.split(",")]
            if len(parts) < 3:
                errors.append(f"Invalid line format: {line}")
                continue

            record_id = parts[0]
            name = parts[1]
            value_raw = parts[2]
            date_raw = parts[3] if len(parts) >= 4 else None

            try:
                value = float(value_raw)
            except ValueError:
                errors.append(f"Record {record_id or '[unknown]'} has invalid numeric value: {value_raw}")
                continue

            date_value: Optional[datetime] = None
            if date_raw:
                try:
                    date_value = datetime.fromisoformat(date_raw)
                except ValueError:
                    errors.append(f"Record {record_id or '[unknown]'} has invalid date: {date_raw}")
                    continue

            parsed_records.append(Record(id=record_id, name=name, value=value, date=date_value))

        return parsed_records, errors


class RecordValidator:
    def validate(self, records: List[Record]) -> Tuple[List[Record], List[str]]:
        valid: List[Record] = []
        errors: List[str] = []

        for record in records:
            is_valid = True

            if not record.id:
                is_valid = False
                errors.append("Record missing ID")

            if not record.name:
                is_valid = False
                errors.append(f"Record {record.id or '[unknown]'} missing name")

            if is_valid:
                valid.append(record)

        return valid, errors


class RecordTransformer:
    def transform(self, records: List[Record]) -> List[Record]:
        transformed: List[Record] = []

        for record in records:
            transformed.append(
                Record(
                    id=record.id,
                    name=record.name.upper(),
                    value=record.value,
                    date=record.date,
                )
            )

        return transformed


class StatisticsCalculator:
    def calculate(self, records: List[Record], error_count: int) -> Dict[str, float]:
        total_records = len(records)
        total_value = sum(record.value for record in records)
        average_value = total_value / total_records if total_records else 0.0

        return {
            "total_records": float(total_records),
            "error_count": float(error_count),
            "total_value": total_value,
            "average_value": average_value,
        }


class RecordFilter:
    def filter_by_min_value(self, records: List[Record], min_value: float) -> List[Record]:
        return [record for record in records if record.value >= min_value]
