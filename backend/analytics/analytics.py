from dataclasses import dataclass
import pandas as pd
import numpy as np
from core.models import Reservation
from django.db.models import F, Sum, DecimalField

# Here I will decide what analytics i WANT TO BE AVAILABLE TO THE USER
# For now:
# Total number of listings by a seller
# Total number of reservations
# Total revenue generated
# % of food waste reduced e.g number of collected / number of listings


def get_number_of_listings_by_seller(df, seller_id):
    seller_id = int(seller_id)
    subset = df[
        (df["seller_id"] == seller_id)
    ]
    print(subset)
    return len(subset)

def get_total_reservations_by_seller(seller_id):
    """Get total reservations for a seller by joining Reservation -> Posting -> Seller"""
    return Reservation.objects.filter(
        posting__seller__seller_id=seller_id
    ).count()

def get_total_revenue_by_seller(df, seller_id):
    result = (
        Reservation.objects
        .filter(
            posting__seller__seller_id=seller_id,
            status__in=["reserved", "collected"]
        )
        .aggregate(
            total_revenue=Sum(
                F("posting__price"),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        )
    )

    return result["total_revenue"] or 0

def get_reduction_in_food_waste_by_seller(df, seller_id):
    seller_df = df[df["seller_id"] == seller_id]
    total_listings = len(seller_df)
    if total_listings == 0:
        return 0.0
    collected = seller_df[seller_df['status'] == 'collected']
    return len(collected) / total_listings * 100.0

def get_total_no_shows_by_seller(seller_id):
    """Get total no-shows for a seller by joining Reservation -> Posting -> Seller"""
    return Reservation.objects.filter(
        posting__seller__seller_id=seller_id,
        status="no-show",
    ).count()