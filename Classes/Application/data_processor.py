from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Dict, List

from Core.config import ProcessingConfig
from Core.models import ProcessingResult, Record
from Core.services import (
    CsvRecordParser,
    RecordFilter,
    RecordTransformer,
    RecordValidator,
    StatisticsCalculator,
)
from Infrastructure.exporters import ExporterRegistry
from Infrastructure.file_store import FileStore
from Infrastructure.logger import BufferedLogger


class DataProcessor:
    def __init__(
        self,
        input_file_path: str,
        output_file_path: str,
        file_store: FileStore,
        logger: BufferedLogger,
        parser: CsvRecordParser,
        validator: RecordValidator,
        transformer: RecordTransformer,
        statistics_calculator: StatisticsCalculator,
        record_filter: RecordFilter,
        exporter_registry: ExporterRegistry,
        config: ProcessingConfig | None = None,
        log_file_path: str = "processing.log",
    ) -> None:
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.log_file_path = log_file_path

        self._file_store = file_store
        self._logger = logger
        self._parser = parser
        self._validator = validator
        self._transformer = transformer
        self._statistics_calculator = statistics_calculator
        self._record_filter = record_filter
        self._exporter_registry = exporter_registry
        self._config = config or ProcessingConfig()

        self.records_processed = 0
        self.error_count = 0
        self.error_messages: List[str] = []
        self.statistics: Dict[str, float] = {}
        self._records: List[Record] = []

        self._logger.log("DataProcessor initialized")

    def process_data(self) -> ProcessingResult:
        self._logger.log("Starting data processing")

        try:
            lines = self._file_store.read_lines(self.input_file_path)
            self._logger.log(f"Read {len(lines)} lines from {self.input_file_path}")

            parsed_records, parse_errors = self._parser.parse_lines(lines)
            self._records = parsed_records
            self._register_errors(parse_errors)
            self._logger.log(f"Parsed {len(self._records)} records")

            if self._config.validate_data:
                valid_records, validation_errors = self._validator.validate(self._records)
                self._records = valid_records
                self._register_errors(validation_errors)
                self._logger.log(f"Validation complete: {len(self._records)} valid records")

            if self._config.transform_data:
                self._records = self._transformer.transform(self._records)
                self._logger.log("Transformation complete")

            self.statistics = self._statistics_calculator.calculate(self._records, self.error_count)
            self._logger.log(f"Calculated {len(self.statistics)} statistics")

            csv_exporter = self._exporter_registry.get("csv")
            csv_exporter.export(self.output_file_path, self._records)
            self.records_processed = len(self._records)
            self._logger.log(f"Wrote {self.records_processed} records to {self.output_file_path}")

            self._file_store.write_text(self.log_file_path, self._logger.dump())
            return ProcessingResult(records_processed=self.records_processed, error_count=self.error_count)
        except Exception as exc:
            self._register_errors([f"Fatal error: {exc}"])
            self._logger.log(f"FATAL ERROR: {exc}")
            self._file_store.write_text(self.log_file_path, self._logger.dump())
            return ProcessingResult(records_processed=self.records_processed, error_count=self.error_count)

    def display_statistics(self) -> None:
        print("\n=== Processing Statistics ===")
        for key, value in self.statistics.items():
            print(f"{key}: {value}")

        if self.error_messages:
            print("\n=== Errors ===")
            for message in self.error_messages:
                print(f"- {message}")

    def export_by_format(self, file_path: str, format_name: str) -> None:
        self._logger.log(f"Exporting to {format_name}: {file_path}")
        exporter = self._exporter_registry.get(format_name)
        exporter.export(file_path, self._records)

    def filter_by_value(self, min_value: float) -> List[Record]:
        filtered = self._record_filter.filter_by_min_value(self._records, min_value)
        self._logger.log(f"Filtered {len(filtered)} records with value >= {min_value}")
        return filtered

    def update_configuration(self, date_format: str, batch_size: int, validate: bool, transform: bool) -> None:
        self._config.date_format = date_format
        self._config.batch_size = batch_size
        self._config.validate_data = validate
        self._config.transform_data = transform
        self._logger.log(
            f"Configuration updated: date_format={date_format}, batch_size={batch_size}, "
            f"validate={validate}, transform={transform}"
        )

    def _register_errors(self, messages: List[str]) -> None:
        if not messages:
            return

        self.error_messages.extend(messages)
        self.error_count += len(messages)
        for message in messages:
            self._logger.log(f"ERROR: {message}")


class SampleDataGenerator:
    @staticmethod
    def generate(file_path: str, record_count: int) -> None:
        randomizer = random.Random()
        lines: List[str] = []

        for index in range(1, record_count + 1):
            record_id = f"ID{index:04d}"
            name = f"Item{index}"
            value = round(randomizer.uniform(10, 1000), 2)
            date_value = datetime.now() - timedelta(days=randomizer.randint(0, 365))
            lines.append(f"{record_id},{name},{value},{date_value:%Y-%m-%d}")

        FileStore().write_lines(file_path, lines)
