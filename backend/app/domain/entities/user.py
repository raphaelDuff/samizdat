from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from domain.entities.entity import Entity


@dataclass
class UserDomain(Entity):
    name: str
    email: str
    password_hash: str
    birth_date: date
    role: str = "user"
    is_active: bool = True
    created_at: datetime = datetime.now(timezone.utc)
    id: UUID = field(default_factory=uuid4)
    updated_at: datetime | None = field(default=None)

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
