from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Record:
    id: str
    name: str
    value: float
    date: Optional[datetime] = None


@dataclass
class ProcessingResult:
    records_processed: int
    error_count: int
