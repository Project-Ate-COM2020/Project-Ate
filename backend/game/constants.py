import os


def get_co2_per_item():
    if os.getenv("DJANGO_DEBUG"):
        return {
            "hot_meals": 250,
            "fresh_produce": 0.5,
            "prepared_salads": 1.2,
            "bakery": 0.8,
            "desserts": 1.0,
            "dairy": 1.5,
        }
    else:
        return {
            "hot_meals": 2.5,
            "fresh_produce": 0.5,
            "prepared_salads": 1.2,
            "bakery": 0.8,
            "desserts": 1.0,
            "dairy": 1.5,
        }
