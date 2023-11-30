from datetime import datetime, timedelta


class ScheduleStartBeforeHandoverError(ValueError):
    pass


class OverlappingOverrideError(ValueError):
    pass


class Scheduler:
    def __init__(self, schedule_json):
        self.handover_start = datetime.fromisoformat(
            schedule_json["handover_start_at"])
        self.interval = timedelta(days=schedule_json["handover_interval_days"])
        self.users = schedule_json["users"]
        self.num_users = len(self.users)

    def _generate_schedule_item(self, user, start, end):
        return {
            "user": user,
            "start_at": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end_at": end.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

    def _parse_override(self, override):
        return datetime.fromisoformat(override["start_at"]), datetime.fromisoformat(override["end_at"]), override["user"]

    def _get_user(self, time):
        "Returns the index of the user on call at the given time."
        return self.users[(time - self.handover_start) // self.interval % self.num_users]

    def _time_to_handover(self, time):
        return self.interval - (time - self.handover_start) % self.interval

    def _append_or_merge_schedule(self, schedule, schedule_item):
        if schedule and schedule[-1]["user"] == schedule_item["user"]:
            schedule[-1]["end_at"] = schedule_item["end_at"]
        else:
            schedule.append(schedule_item)

    def _validate_overrides(self, sorted_overrides):
        for i in range(len(sorted_overrides) - 1):
            if sorted_overrides[i]["end_at"] > sorted_overrides[i + 1]["start_at"]:
                raise OverlappingOverrideError(
                    "Overrides cannot overlap with each other.")

    def generate_schedule(self, start_string, end_string, overrides=[]):
        start = datetime.fromisoformat(start_string)
        end = datetime.fromisoformat(end_string)
        if start < self.handover_start:
            raise ScheduleStartBeforeHandoverError(
                "Start time cannot be before handover start time.")
        overrides.sort(key=lambda x: x["start_at"])
        self._validate_overrides(overrides)

        schedule = []
        current_time = start
        for o in overrides:
            o_start, o_end, o_user = self._parse_override(o)
            o_end = min(o_end, end)
            if o_end < start:
                continue
            if o_start >= end or current_time >= end:
                break
            if current_time >= o_start:
                schedule.append(self._generate_schedule_item(
                    o_user, current_time, o_end))
                current_time = o_end
            while current_time < o_start:
                user = self._get_user(current_time)
                next_time = current_time + self._time_to_handover(current_time)
                if next_time < o_start:
                    schedule.append(self._generate_schedule_item(
                        user, current_time, next_time))
                    current_time = next_time
                else:
                    if user == o_user:
                        self._append_or_merge_schedule(schedule, self._generate_schedule_item(
                            user, current_time, o_end
                        ))
                    else:
                        self._append_or_merge_schedule(schedule, self._generate_schedule_item(
                            user, current_time, o_start
                        ))
                        self._append_or_merge_schedule(schedule, self._generate_schedule_item(
                            o_user, o_start, o_end
                        ))
                    current_time = o_end
        # Schedule remaining time once overrides are exhausted
        while current_time < end:
            user = self._get_user(current_time)
            next_time = min(end, current_time +
                            self._time_to_handover(current_time))
            self._append_or_merge_schedule(schedule, self._generate_schedule_item(
                user, current_time, next_time))
            current_time = next_time

        return schedule
