import collections
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any

import requests


def download_txt_file(url: str, save_path: str):
    """
    Download txt file from url and save it to save_path.

    :param url: url to download
    :param save_path: path to save txt file
    """
    response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, 'w') as file:
            file.write(response.text)
        print(f"File successfully downloaded to {save_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")


def process_data_from_file(
        file_path: str,
        sort_by_days: bool = False
) -> defaultdict[Any, defaultdict[Any, list]] | list[tuple[datetime, int]]:
    """
    Process data from txt file, optionally sort it by days.

    :param file_path: path to txt file
    :param sort_by_days: sort by weekdays, defaults to False
    :return: list of data for days, or list of lists of data for weekdays
    """
    # Initialize lists for each weekday
    if sort_by_days:
        data_by_weekday = collections.defaultdict(lambda: collections.defaultdict(list))
    else:
        data_in_order = []
        current_day_data = []
        last_date_key = None

    # Open and read the file
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            # split the line into datetime and value parts
            date_time_str, value_str = line.split(' : ')
            value_str = value_str.strip()
            if value_str in ["None", "", "-1", "Array"]:
                value = 0
            else:
                value = int(value_str)

            # parse the datetime string into a datetime object
            date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
            # !!! time shift +2 hours
            date_time += timedelta(0, 0, 0, 0, 0, 2)

            # adjust time to align with 5:00 AM start of the day
            # if time is before 5:00 AM, it belongs to the previous day
            if date_time.hour < 4:
                date_time -= timedelta(days=1)

            date_key = date_time.date()  # use the date as the key
            if sort_by_days:
                weekday = date_time.weekday()  # Monday is 0, Sunday is 6
                data_by_weekday[weekday][date_key].append((date_time, value))
            else:
                if last_date_key == date_key or len(current_day_data) == 0:
                    current_day_data.append((date_time, value))
                else:
                    current_day_data.append((date_time, value))
                    data_in_order.append(current_day_data)
                    current_day_data = []
                last_date_key = date_key

    if sort_by_days:
        return data_by_weekday
    else:
        data_in_order.append(current_day_data)
        return data_in_order
