from datetime import date, timedelta
from typing import Dict, Iterable, List

from models import Parent, DayRule

# Default rules for each weekday
DEFAULT_RULES: Dict[str, DayRule] = {
    "Monday": DayRule(capacity=1),
    "Tuesday": DayRule(capacity=1),
    "Wednesday": DayRule(capacity=1, full_day=True),
    "Thursday": DayRule(capacity=1),
    "Friday": DayRule(capacity=2),
}


def daterange(start: date, end: date) -> Iterable[date]:
    """Generate dates from start to end inclusive."""
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def schedule(
    parents: List[Parent],
    start: date,
    end: date,
    rules: Dict[str, DayRule] | None = None,
    closed_days: Iterable[date] | None = None,
) -> Dict[date, List[str]]:
    """Create a schedule for the given date range.

    Args:
        parents: List of parents participating in the schedule.
        start: Start date for scheduling.
        end: End date for scheduling.
        rules: Optional mapping of weekday name to DayRule.
        closed_days: Optional iterable of dates when the preschool is closed.

    Returns:
        Mapping from date to list of parent names assigned that day.
    """
    rules = rules or DEFAULT_RULES
    closed_days = set(closed_days or [])

    schedule: Dict[date, List[str]] = {}
    for day in daterange(start, end):
        if day in closed_days:
            continue
        weekday_name = day.strftime("%A")
        rule = rules.get(weekday_name)
        if not rule:
            continue  # skip days without defined rules

        available_parents = [p for p in parents if p.remaining_quota() > 0]
        if not available_parents:
            break

        # Sort parents based on their preference for the weekday
        available_parents.sort(key=lambda p: p.preferences.get(weekday_name, 3))

        assigned_today: List[str] = []
        for parent in available_parents:
            if len(assigned_today) >= rule.capacity:
                break
            priority = parent.preferences.get(weekday_name, 3)
            if priority <= 3:  # 1, 2 or 3 are acceptable
                parent.assigned.append(day)
                assigned_today.append(parent.name)
        schedule[day] = assigned_today
    return schedule
