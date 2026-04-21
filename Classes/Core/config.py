from dataclasses import dataclass


@dataclass
class ProcessingConfig:
    validate_data: bool = True
    transform_data: bool = True
    date_format: str = "%Y-%m-%d"
    batch_size: int = 100
