from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime, date, timezone

from sqlmodel import SQLModel, Field, Column, JSON


class UserSQLModel(SQLModel, table=True):
    __tablename__ = "users"  # pyright: ignore[reportAssignmentType]

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    name: str
    email: str = Field(index=True, unique=True)
    password_hash: str
    role: str

    birth_date: date

    is_active: bool = Field(default=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    updated_at: Optional[datetime] = Field(default=None)
