from dataclasses import dataclass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


@dataclass
class ForecastInput:
    seller_id: int
    category: str
    day_of_week: int
    time_window: str
    weather_flag = None


def get_similar_listings(df, inp):
    # Get adjacent days (one above, one below, and the day itself)
    adjacent_days = [
        (inp.day_of_week - 1) % 7,
        inp.day_of_week,
        (inp.day_of_week + 1) % 7,
    ]

    # Parse time_window and get adjacent times
    time_parts = inp.time_window.split("-")
    start_time = time_parts[0]

    # Get adjacent time windows (assuming hourly slots)
    time_slots = get_adjacent_time_windows(start_time)

    # Filter by category and adjacent day/time combinations
    mask = (
        (df["category"] == inp.category)
        & (df["day_of_week"].isin(adjacent_days))
        & (df["time_window"].isin(time_slots))
    )

    if inp.weather_flag is not None:
        mask &= df["weather_flag"] == inp.weather_flag

    return df.loc[mask].copy()


def get_adjacent_time_windows(time_str):
    """Get the given time and adjacent hourly slots"""
    try:
        hour, minute = map(int, time_str.split(":"))
        prev_hour = (hour - 1) % 24
        next_hour = (hour + 1) % 24

        return [
            f"{prev_hour:02d}:{minute:02d}",
            f"{hour:02d}:{minute:02d}",
            f"{next_hour:02d}:{minute:02d}",
        ]
    except:
        return [time_str]


def add_no_show_probability(df):
    df = df.copy()
    df["no_show_prob"] = np.where(
        df["observed_reservations"] > 0,
        df["observed_no_show"] / df["observed_reservations"],
        np.nan,
    )
    return df.dropna(subset=["no_show_prob"])


def aggregate_by_price(df):
    agg = (
        df.groupby("price")
        .agg(
            avg_no_show_prob=("no_show_prob", "mean"),
            total_reservations=("observed_reservations", "sum"),
            n_listings=("no_show_prob", "count"),
        )
        .reset_index()
        .sort_values("price")
    )
    return agg
