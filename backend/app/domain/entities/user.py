from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import UUID

from domain.entities.entity import Entity


@dataclass
class User(Entity):
    name: str
    email: str
    password_hash: str
    role: str
    birth_date: date
    is_active: bool = False
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime | None = field(default=None)
    saved_list_ids: list[UUID] = field(default_factory=list)

    @property
    def age(self) -> int:
        date_today = date.today()
        return (
            date_today.year
            - self.birth_date.year
            - (
                (date_today.month, date_today.day)
                < (self.birth_date.month, self.birth_date.day)
            )
        )

    def save_list(self, booklist_id: UUID):
        if booklist_id not in self.saved_list_ids:
            self.saved_list_ids.append(booklist_id)
