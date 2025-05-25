from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List

@dataclass
class Parent:
    """Represents a parent and their scheduling data."""
    name: str
    quota: int  # number of required shifts per schedule period
    preferences: Dict[str, int]  # mapping from weekday name to priority (1..3)
    assigned: List[date] = field(default_factory=list)

    def remaining_quota(self) -> int:
        return max(self.quota - len(self.assigned), 0)

@dataclass
class DayRule:
    """Configuration for how many parents are needed a particular weekday."""
    capacity: int
    full_day: bool = False

