from dataclasses import dataclass
from datetime import datetime


@dataclass
class Note:
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
