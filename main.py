from datetime import datetime

import interpolation
import parser_utils
import plots

# download, load and process data
data_url = "https://ftp2.mvolfik.com/vojta_scraper/zaznam.txt"
save_path = "data.txt"
parser_utils.download_txt_file(data_url, save_path)
data = parser_utils.process_data_from_file(save_path, sort_by_days=False)

# filter out days with too many missing values
threshold = 50
new_data = []
before = len(data)
data = [day for day in data if 1440 - len(day) < threshold]

print(f"Filtered out {before - len(data)} {'day' if before - len(data) == 1 else 'days'}")

# fill in missing data with zeros
for i in range(len(data)):
    if len(data[i]) < 1440:
        data[i] = interpolation.fill_missing_minutes(data[i])

# interpolate
for day in data:
    interpolation.interpolate_on_single_day(day, verbose=True)

# filter out corrupted data
to_filter = [
    # complete loss of data
    datetime(2024, 8, 5),
    datetime(2024, 8, 6),
    datetime(2024, 8, 7),
    datetime(2024, 8, 8),
    datetime(2024, 8, 9),
    datetime(2024, 8, 11),
    # too much interpolation
    datetime(2024, 8, 12),
    # weird
    datetime(2024, 8, 26),
    # shifted
    datetime(2024, 9, 26),
]

data = [day for day in data if datetime(day[0][0].year, day[0][0].month, day[0][0].day) not in to_filter]

# plot graph and generate animation
plots.plot_days(data[:30])
plots.plot_days_animated(data, anim_interval=200)
