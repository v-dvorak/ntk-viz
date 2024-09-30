from datetime import datetime, timedelta

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from color_palette import PALETTE


def plot_days(
        data: list[list[tuple[datetime, int]]],
        figsize: tuple[int, int] = (10, 6),
        palette: list[str] = PALETTE,
):
    """
    Plot days data.
    :param data: list of data for each day
    :param figsize: final plot figure size
    :param palette: color palette
    """
    start_time = data[0][0][0]
    time_points = [start_time + timedelta(minutes=i) for i in range(len(data[0]))]

    # fig init
    plt.figure(figsize=figsize)

    # iterate over each list in `data` and plot it
    for i, day_data in enumerate(data):
        plt.plot(time_points, [dat[1] for dat in day_data],
                 label=day_data[0][0].strftime('%d. %m. %Y'), c=palette[i])

    # set the x-axis major locator to show the time every hour
    hours = mdates.HourLocator(interval=1)
    h_fmt = mdates.DateFormatter('%H:%M')

    # apply the locator and formatter to the current x-axis
    plt.gca().xaxis.set_major_locator(hours)
    plt.gca().xaxis.set_major_formatter(h_fmt)

    # rotate and align the x-ticks for better readability
    plt.gcf().autofmt_xdate()

    # plot legend
    plt.legend()

    # display
    plt.margins(x=0)
    plt.tight_layout()
    plt.show()


def plot_days_animated(
        data: list[list[tuple[datetime, int]]],
        save_path: str = "ani.gif",
        main_line_color: str = "blue",
        secondary_line_color: str = "gray",
        top_lim_offset: float = 1.05,
        figsize: tuple[int, int] = (10, 6),
        fade_out_rate: float = 0.9,
        anim_interval: float = 200,
):
    """
    Creates animation of days data, processed days gradually disappear.

    :param data: list of data for each day
    :param save_path: path to save animation
    :param main_line_color: color of the newest line
    :param secondary_line_color: color of all other lines
    :param top_lim_offset: offset for top y-axis limit, creates space between plotted lines and plot outline
    :param figsize: final plot figure size
    :param fade_out_rate: in each iteration line's opacity is multiplied by fade_out_rate
    :param anim_interval: animation interval in ms
    """
    # retrieve the start time and time points from the data
    start_time = data[0][0][0]
    time_points = [start_time + timedelta(minutes=i) for i in range(len(data[0]))]
    retrieved_values = [[day[1] for day in dato] for dato in data]

    # find y-axis limit
    mm = max([max(lst) for lst in retrieved_values])

    # fig init
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_ylim(0, int(mm * top_lim_offset))
    ax.set_xlim(time_points[0], time_points[-1])

    # store data for every line and set it invisible at first
    lines = []
    for _ in data:
        line, = ax.plot([], [], color=secondary_line_color, alpha=0.0)
        lines.append(line)

    # set x-axis locator and formatter
    hours = mdates.HourLocator(interval=1)
    h_fmt = mdates.DateFormatter("%H:%M")
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(h_fmt)

    # rotate and align the x-ticks, improve readability
    plt.gcf().autofmt_xdate()

    # update function for animation
    def update(frame):
        ax.set_title(data[frame][0][0].strftime("%d. %m. %Y"))
        # update data on current frame
        if frame < len(data):
            lines[frame].set_data(time_points, retrieved_values[frame])
            lines[frame].set_color(main_line_color)
            lines[frame].set_alpha(1.0)  # current line at full opacity
            lines[frame].set_linewidth(2)

        # fade previous lines
        for i in range(frame):
            lines[i].set_color(secondary_line_color)  # set previous lines to gray
            c = lines[i].get_alpha()
            lines[i].set_linewidth(1)
            lines[i].set_alpha(c * fade_out_rate)  # update opacity

    # create and save animation
    ani = FuncAnimation(fig, update, frames=len(data), interval=anim_interval, repeat=True)
    ani.save(save_path)

    # display
    plt.tight_layout()
    plt.show()
