import datetime
import json
import os

file_name = f'generated_logs.json'

if os.path.exists(file_name):
    os.remove(file_name)

with open(file_name, 'w') as f:
    pass

data = []
for i in os.listdir('reserve_logs'):
    with open(f"reserve_logs/{i}", 'r') as f:
        try:
            data += json.load(f)
        except json.decoder.JSONDecodeError:
            data += []
with open(f"logs.json", 'r') as f:
    try:
        data += json.load(f)
    except json.decoder.JSONDecodeError:
        data += []


def sort_and_remove_duplicates(data):
    def sort_by_timestamp(item):
        try:
            return datetime.datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return datetime.datetime.strptime(item['timestamp'], '%Y-%m-%d %H:%M:%S')

    sorted_data = sorted(data, key=sort_by_timestamp)
    unique_data = []
    seen_timestamps = set()

    for item in sorted_data:
        timestamp = item['timestamp']
        if timestamp not in seen_timestamps:
            unique_data.append(item)
            seen_timestamps.add(timestamp)

    return unique_data

sorted_data = sort_and_remove_duplicates(data)

with open(file_name, 'w') as f:
    f.write(json.dumps(sorted_data, indent=4, ensure_ascii=False))
