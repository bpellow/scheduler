import pytest
from datetime import datetime, timedelta
from scheduler import Scheduler, ScheduleStartBeforeHandoverError


def test_no_overrides():
    scheduler_json = {
        "handover_start_at": "2023-11-20T17:00:00",
        "handover_interval_days": 1,
        "users": ["user1", "user2", "user3"]
    }
    scheduler = Scheduler(scheduler_json)
    start = datetime.fromisoformat("2023-11-20T17:00:00")
    end = datetime.fromisoformat("2023-11-25T17:00:00")

    schedule = scheduler.generate_schedule(start, end)
    assert len(schedule) == 5


def test_override1():
    scheduler_json = {
        "handover_start_at": "2023-11-20T17:00:00Z",
        "handover_interval_days": 2,
        "users": ["A", "B", "C", "D"]
    }
    scheduler = Scheduler(scheduler_json)
    overrides = [{
        "user": "D",
        "start_at": "2023-11-25T14:00:00Z",
        "end_at": "2023-11-27T18:00:00Z"
    }, {
        "user": "D",
        "start_at": "2023-11-21T14:00:00Z",
        "end_at": "2023-11-23T18:00:00Z"
    }
    ]
    start = datetime.fromisoformat("2023-11-20T17:00:00Z")
    end = datetime.fromisoformat("2023-11-30T17:00:00Z")
    schedule = scheduler.generate_schedule(start, end, overrides)
    expected = [{'user': 'A', 'start_at': '2023-11-20T17:00:00Z', 'end_at': '2023-11-21T14:00:00Z'}, {'user': 'D', 'start_at': '2023-11-21T14:00:00Z', 'end_at': '2023-11-23T18:00:00Z'}, {'user': 'B', 'start_at': '2023-11-23T18:00:00Z', 'end_at': '2023-11-24T17:00:00Z'},
                {'user': 'C', 'start_at': '2023-11-24T17:00:00Z', 'end_at': '2023-11-25T14:00:00Z'}, {'user': 'D', 'start_at': '2023-11-25T14:00:00Z', 'end_at': '2023-11-28T17:00:00Z'}, {'user': 'A', 'start_at': '2023-11-28T17:00:00Z', 'end_at': '2023-11-30T17:00:00Z'}]
    assert schedule == expected


def test_override2():
    scheduler_json = {
        "handover_start_at": "2023-11-20T17:00:00Z",
        "handover_interval_days": 2,
        "users": ["A", "B", "C", "D"]
    }
    scheduler = Scheduler(scheduler_json)
    overrides = [{
        "user": "D",
        "start_at": "2023-11-25T14:00:00Z",
        "end_at": "2023-11-27T18:00:00Z"
    }, {
        "user": "D",
        "start_at": "2023-11-21T14:00:00Z",
        "end_at": "2023-11-23T18:00:00Z"
    }
    ]
    start = datetime.fromisoformat("2023-11-20T17:00:00Z")
    end = datetime.fromisoformat("2023-11-30T17:00:00Z")
    expected = [{'user': 'A', 'start_at': '2023-11-20T17:00:00Z', 'end_at': '2023-11-21T14:00:00Z'}, {'user': 'D', 'start_at': '2023-11-21T14:00:00Z', 'end_at': '2023-11-23T18:00:00Z'}, {'user': 'B', 'start_at': '2023-11-23T18:00:00Z', 'end_at': '2023-11-24T17:00:00Z'},
                {'user': 'C', 'start_at': '2023-11-24T17:00:00Z', 'end_at': '2023-11-25T14:00:00Z'}, {'user': 'D', 'start_at': '2023-11-25T14:00:00Z', 'end_at': '2023-11-28T17:00:00Z'}, {'user': 'A', 'start_at': '2023-11-28T17:00:00Z', 'end_at': '2023-11-30T17:00:00Z'}]
    schedule = scheduler.generate_schedule(start, end, overrides)
    assert schedule == expected


def test_override3():
    # Override starts at the end time
    scheduler_json = {
        "handover_start_at": "2023-11-20T17:00:00Z",
        "handover_interval_days": 2,
        "users": ["A", "B", "C"]
    }
    scheduler = Scheduler(scheduler_json)
    overrides = [{
        "user": "D",
        "start_at": "2023-11-26T17:00:00Z",
        "end_at": "2023-11-27T18:00:00Z"
    }
    ]
    start = datetime.fromisoformat("2023-11-20T17:00:00Z")
    end = datetime.fromisoformat("2023-11-26T17:00:00Z")
    schedule = scheduler.generate_schedule(start, end, overrides)
    expected = [{'user': 'A', 'start_at': '2023-11-20T17:00:00Z', 'end_at': '2023-11-22T17:00:00Z'}, {'user': 'B', 'start_at': '2023-11-22T17:00:00Z',
                                                                                                      'end_at': '2023-11-24T17:00:00Z'}, {'user': 'C', 'start_at': '2023-11-24T17:00:00Z', 'end_at': '2023-11-26T17:00:00Z'}]
    assert schedule == expected


def test_override4():
    scheduler_json = {
        "handover_start_at": "2023-11-20T17:00:00Z",
        "handover_interval_days": 2,
        "users": ["A", "B", "C"]
    }
    scheduler = Scheduler(scheduler_json)
    overrides = [{
        "user": "D",
        "start_at": "2023-11-26T17:00:00Z",
        "end_at": "2023-11-27T18:00:00Z"
    }
    ]
    start = datetime.fromisoformat("2023-11-20T17:00:00Z")
    end = datetime.fromisoformat("2023-11-26T17:00:00Z")
    expected = [{'user': 'A', 'start_at': '2023-11-20T17:00:00Z', 'end_at': '2023-11-22T17:00:00Z'}, {'user': 'B', 'start_at': '2023-11-22T17:00:00Z',
                                                                                                      'end_at': '2023-11-24T17:00:00Z'}, {'user': 'C', 'start_at': '2023-11-24T17:00:00Z', 'end_at': '2023-11-26T17:00:00Z'}]
    schedule = scheduler.generate_schedule(start, end, overrides)
    assert schedule == expected


def test_override5():
    scheduler_json = {
        "handover_start_at": "2023-11-20T17:00:00Z",
        "handover_interval_days": 2,
        "users": ["A", "B"]
    }
    scheduler = Scheduler(scheduler_json)
    overrides = [{
        "user": "D",
        "start_at": "2023-11-20T17:00:00Z",
        "end_at": "2023-11-27T18:00:00Z"
    }
    ]
    start = datetime.fromisoformat("2023-11-20T17:00:00Z")
    end = datetime.fromisoformat("2023-11-24T17:00:00Z")
    expected = [{'user': 'D', 'start_at': '2023-11-20T17:00:00Z',
                 'end_at': '2023-11-24T17:00:00Z'}]
    schedule = scheduler.generate_schedule(start, end, overrides)
    assert schedule == expected


def test_override6():
    scheduler_json = {
        "handover_start_at": "2023-11-20T17:00:00Z",
        "handover_interval_days": 2,
        "users": ["A"]
    }
    scheduler = Scheduler(scheduler_json)
    overrides = [{
        "user": "B",
        "start_at": "2023-11-19T17:00:00Z",
        "end_at": "2023-11-20T23:00:00Z"
    },
        {
        "user": "B",
        "start_at": "2023-11-21T10:00:00Z",
        "end_at": "2023-11-21T12:00:00Z"
    }

    ]
    start = datetime.fromisoformat("2023-11-20T17:00:00Z")
    end = datetime.fromisoformat("2023-11-22T17:00:00Z")
    expected = [{'user': 'B', 'start_at': '2023-11-20T17:00:00Z', 'end_at': '2023-11-20T23:00:00Z'}, {'user': 'A', 'start_at': '2023-11-20T23:00:00Z', 'end_at': '2023-11-21T10:00:00Z'},
                {'user': 'B', 'start_at': '2023-11-21T10:00:00Z', 'end_at': '2023-11-21T12:00:00Z'}, {'user': 'A', 'start_at': '2023-11-21T12:00:00Z', 'end_at': '2023-11-22T17:00:00Z'}]
    schedule = scheduler.generate_schedule(start, end, overrides)
    assert schedule == expected


def test_override7():
    scheduler_json = {
        "handover_start_at": "2023-11-20T17:00:00Z",
        "handover_interval_days": 2,
        "users": ["A"]
    }
    scheduler = Scheduler(scheduler_json)
    overrides = [{
        "user": "B",
        "start_at": "2023-11-19T17:00:00Z",
        "end_at": "2023-11-20T23:00:00Z"
    },
        {
        "user": "B",
        "start_at": "2023-11-21T10:00:00Z",
        "end_at": "2023-11-22T18:00:00Z"
    }

    ]
    start = datetime.fromisoformat("2023-11-20T17:00:00Z")
    end = datetime.fromisoformat("2023-11-22T17:00:00Z")
    expected = [{'user': 'B', 'start_at': '2023-11-20T17:00:00Z', 'end_at': '2023-11-20T23:00:00Z'}, {'user': 'A', 'start_at': '2023-11-20T23:00:00Z',
                                                                                                      'end_at': '2023-11-21T10:00:00Z'}, {'user': 'B', 'start_at': '2023-11-21T10:00:00Z', 'end_at': '2023-11-22T17:00:00Z'}]
    schedule = scheduler.generate_schedule(start, end, overrides)
    assert schedule == expected
