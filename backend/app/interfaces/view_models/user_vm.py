from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class UserViewModel:
    """View-specific representation of a user."""

    id: str
    name: str
    email: str
    brith_date: date
    role: str
    is_active: bool
