CO2_PER_ITEM = {
    "hot_meals": 2.5,
    "fresh_produce": 0.5,
    "prepared_salads": 1.2,
    "bakery": 0.8,
    "desserts": 1.0,
    "dairy": 1.5,
}

VARIETY_BADGES = [
    {"name": "Explorer", "min_categories": 2, "min_co2": 0},
    {"name": "Discoverer", "min_categories": 3, "min_co2": 0},
    {"name": "Adventurer", "min_categories": 4, "min_co2": 0},
    {"name": "Master", "min_categories": 6, "min_co2": 0},
]

# took a guess here with the co2 badges, might need a revisit
IMPACT_BADGES = [
    {"name": "Eco Starter", "min_co2": 100, "min_categories": 0},
    {"name": "Eco Friend", "min_co2": 500, "min_categories": 0},
    {"name": "Climate Hero", "min_co2": 1000, "min_categories": 0},
    {"name": "Planet Saver", "min_co2": 10000, "min_categories": 0},
]
