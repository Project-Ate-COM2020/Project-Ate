from dataclasses import dataclass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from .models import Reservation

def real_streak_weeks(consumer):
    """Gets reservations from database from a given consumer and returns int of current streak weeks"""
    reservations = Reservation.objects.filter(consumer=consumer, status="collected").order_by("collected_at")
    if not reservations.exists():
        return 0

    # Get the date of the most recent collection
    last_collected_date = reservations.last().collected_at.date()
    today = datetime.now().date()

    # If the last collected date is in the future, return 0
    if last_collected_date > today:
        return 0

    # Calculate the number of weeks in the current streak
    streak_weeks = 0
    current_week_start = last_collected_date - timedelta(days=last_collected_date.weekday())  # Start of the week (Monday)

    while True:
        # Check if there are any collections in the current week
        if reservations.filter(collected_at__date__gte=current_week_start, collected_at__date__lt=current_week_start + timedelta(days=7)).exists():
            streak_weeks += 1
            current_week_start -= timedelta(days=7)  # Move to the previous week
        else:
            break

    return streak_weeks