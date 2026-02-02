from dataclasses import dataclass
import pandas as pd
import numpy as np

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

def get_total_reservations_by_seller(df, seller_id):
    return df[df["seller_id"] == seller_id]["quantity"].sum()

def get_total_revenue_by_seller(df, seller_id):
    return df[df["seller_id"] == seller_id]["price"].sum()

def get_reduction_in_food_waste_by_seller(df, seller_id):
    seller_df = df[df["seller_id"] == seller_id]
    total_listings = len(seller_df)
    if total_listings == 0:
        return 0.0
    collected = seller_df[seller_df['status'] == 'collected']
    return len(collected) / total_listings * 100.0