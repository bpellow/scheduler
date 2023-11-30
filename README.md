# Rota scheduler
## Example usage:
```bash
python parse_schedule.py --schedule schedule.json --overrides overrides.json --from '2023-11-17T17:00:00Z' --until '2023-11-23T17:00:00Z'
```
### Schedule
```json
{
    "users": [
        "alice",
        "charlie"
    ],
    "handover_start_at": "2023-11-17T17:00:00Z",
    "handover_interval_days": 3
}
```
### Overrides
```json
[
    {
        "user": "bill",
        "start_at": "2023-11-18T12:00:00Z",
        "end_at": "2023-11-20T19:00:00Z"
    }
]
```
### Output
```json
[
  {
    "user": "alice",
    "start_at": "2023-11-17T17:00:00Z",
    "end_at": "2023-11-18T12:00:00Z"
  },
  {
    "user": "bill",
    "start_at": "2023-11-18T12:00:00Z",
    "end_at": "2023-11-20T19:00:00Z"
  },
  {
    "user": "charlie",
    "start_at": "2023-11-20T19:00:00Z",
    "end_at": "2023-11-23T17:00:00Z"
  }
]
```
