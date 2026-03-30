from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class Pet:
	pet_name: str
	age: int


@dataclass
class Activity:
	activity_name: str
	duration: timedelta


class Owner:
	def __init__(self, name: str, preferences: list[str]) -> None:
		self.name = name
		self.preferences = preferences
		self.schedule: dict[datetime, Activity] = {}

	def checkavailability(self, start_time: datetime, activity: Activity) -> bool:
		"""Return True if the proposed time does not overlap with existing activities."""
		proposed_end = start_time + activity.duration

		for scheduled_start, scheduled_activity in self.schedule.items():
			scheduled_end = scheduled_start + scheduled_activity.duration

			overlaps = start_time < scheduled_end and proposed_end > scheduled_start
			if overlaps:
				return False

		return True

	def schedule_activity(self, start_time: datetime, activity: Activity) -> bool:
		"""Add an activity if the owner is available at the requested time."""
		if not self.checkavailability(start_time, activity):
			return False

		self.schedule[start_time] = activity
		return True

