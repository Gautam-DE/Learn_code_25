from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    id: str
    name: str
    email: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
