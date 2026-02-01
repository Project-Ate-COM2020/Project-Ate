from dataclasses import dataclass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


@dataclass
class ForecastInput:
    seller_id: int
    category: str
    day_of_week: int
    time_window: str
    weather: None


def get_similar_listings(df, inp):
    # Get adjacent days (one above, one below, and the day itself)
    adjacent_days = get_adjacent_days(inp.day_of_week)
    similar_times = get_adjacent_time_slots(inp.time_window)
    subset = df[
        (df["category"] == inp.category)
        & (df["day_of_week"].isin(adjacent_days))
        & (df["time_window"].isin(similar_times))
    ]
    return subset
        
def get_adjacent_time_slots(time_range):
    """
    Given a time range like '10:00-11:00',
    return the previous, current, and next adjacent time ranges.

    Returns:
        ['09:00-10:00', '10:00-11:00', '11:00-12:00']
    """
    start_str, end_str = time_range.split('-')

    start = datetime.strptime(start_str, "%H:%M")
    end = datetime.strptime(end_str, "%H:%M")

    duration = end - start  # usually 1 hour

    prev_start = start - duration
    prev_end = start

    next_start = end
    next_end = end + duration

    return [
        f"{prev_start.strftime('%H:%M')}-{prev_end.strftime('%H:%M')}",
        f"{start.strftime('%H:%M')}-{end.strftime('%H:%M')}",
        f"{next_start.strftime('%H:%M')}-{next_end.strftime('%H:%M')}",
    ]
    
def get_adjacent_days(day_of_week):
    """
    Given a day of the week (1-7),
    return the previous, current, and next days.

    Returns:
        [prev_day, current_day, next_day]
    """
    return [
        (int(day_of_week) - 1) % 7,
        int(day_of_week),
        (int(day_of_week) + 1) % 7,
    ]
    
def get_no_show_probability(subset):
    """
    From the subet find the average no-show probability.
    No-show probability is defined as observed_no_show / observed_reservations
    Returns value between 0 and 1.
    """
    if len(subset) == 0:
        return 0.0
    total_no_show = subset["observed_no_show"].sum()
    total_reservations = subset["observed_reservations"].sum()
    if total_reservations == 0:
        return 0.0
    return total_no_show / total_reservations