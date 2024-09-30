from datetime import datetime, timedelta


def _find_zero_sublists_indexes(numbers):
    zero_sublists_indexes = []
    start_index = None

    for i, num in enumerate(numbers):
        if num == 0:
            if start_index is None:
                start_index = i
        else:
            if start_index is not None:
                zero_sublists_indexes.append((start_index, i - 1))
                start_index = None

    # Handle case where the list ends with zeros
    if start_index is not None:
        zero_sublists_indexes.append((start_index, len(numbers) - 1))

    return zero_sublists_indexes


def _interpolate_on_indices(data, indexes, threshold=20, verbose: bool = False):
    for (a, b) in indexes:
        if a == 0 or b == len(data) - 1:
            continue

        left = a - 1
        right = b + 1

        if data[left] > threshold or data[right] > threshold:
            if verbose:
                print(f"Interpolating {left}:{right}")
            diff = data[left] - data[right]
            step = diff / (left - right)

            for i in range(a, b + 1):
                data[i] = data[i - 1] + step


def _interpolate_on_values(data, threshold=5, verbose: bool = False):
    zero_indexes = _find_zero_sublists_indexes(data)
    if verbose:
        print(zero_indexes)
    _interpolate_on_indices(data, zero_indexes, threshold=threshold, verbose=verbose)
    return data


def interpolate_on_single_day(day, threshold: int = 5, verbose: bool = False):
    interpolated = _interpolate_on_values([dat[1] for dat in day], threshold=threshold, verbose=verbose)

    for i in range(len(day)):
        day[i] = (day[i][0], int(interpolated[i]))

    return day


def fill_missing_minutes(day_data: list[tuple[datetime, int]], verbose: bool = False) -> list[tuple[datetime, int]]:
    # Ensure the list is sorted by datetime, in case it isn't
    day_data.sort(key=lambda x: x[0])

    minute_count = 0
    complete_list = []

    ex_pointer = 0
    while minute_count < 1440:
        if ex_pointer < len(day_data) and (day_data[ex_pointer][0].minute - minute_count) % 60 == 1:
            complete_list.append(day_data[ex_pointer])
            ex_pointer += 1
        else:
            # hot fix first data missing
            if len(complete_list) == 0:
                complete_list.append((day_data[0][0] - timedelta(minutes=1), 0))
            # data is missing, add value at +1 minute from last one
            else:
                complete_list.append((complete_list[-1][0] + timedelta(minutes=1), 0))
                if verbose:
                    print(f"adding {complete_list[-1]}")

        minute_count += 1

    return complete_list
