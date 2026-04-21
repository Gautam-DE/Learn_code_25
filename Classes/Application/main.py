from Application.data_processor import DataProcessor, SampleDataGenerator
from Core.config import ProcessingConfig
from Core.services import (
    CsvRecordParser,
    RecordFilter,
    RecordTransformer,
    RecordValidator,
    StatisticsCalculator,
)
from Infrastructure.exporters import CsvExporter, ExporterRegistry, JsonExporter, XmlExporter
from Infrastructure.file_store import FileStore
from Infrastructure.logger import BufferedLogger


def build_processor() -> DataProcessor:
    registry = ExporterRegistry()
    registry.register("csv", CsvExporter())
    registry.register("json", JsonExporter())
    registry.register("xml", XmlExporter())

    return DataProcessor(
        input_file_path="input.csv",
        output_file_path="output.csv",
        file_store=FileStore(),
        logger=BufferedLogger(),
        parser=CsvRecordParser(),
        validator=RecordValidator(),
        transformer=RecordTransformer(),
        statistics_calculator=StatisticsCalculator(),
        record_filter=RecordFilter(),
        exporter_registry=registry,
        config=ProcessingConfig(validate_data=True, transform_data=True, date_format="%m/%d/%Y", batch_size=50),
    )


def main() -> None:
    SampleDataGenerator.generate("input.csv", 50)

    processor = build_processor()
    result = processor.process_data()

    processor.display_statistics()

    processor.export_by_format("output.json", "json")
    processor.export_by_format("output.xml", "xml")

    filtered = processor.filter_by_value(100)

    print(f"\nRecords processed: {result.records_processed}")
    print(f"Errors: {result.error_count}")
    print(f"Filtered records: {len(filtered)}")


if __name__ == "__main__":
    main()
