import argparse
import json
from scheduler import Scheduler


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='Render on-call schedule with overrides.')
    parser.add_argument('--schedule', type=str,
                        help='Path to schedule JSON file', required=True)
    parser.add_argument('--overrides', type=str,
                        help='Path to overrides JSON file', required=True)
    parser.add_argument('--from', dest='start_time', type=str,
                        help='Start time for rendering schedule', required=True)
    parser.add_argument('--until', dest='end_time', type=str,
                        help='End time for rendering schedule', required=True)
    args = parser.parse_args()

    schedule = load_json(args.schedule)
    scheduler = Scheduler(schedule)
    overrides = load_json(args.overrides)
    start_string = args.start_time
    end_string = args.end_time

    final_schedule = scheduler.generate_schedule(
        start_string, end_string, overrides)

    save_json("output.json", final_schedule)


if __name__ == "__main__":
    main()
