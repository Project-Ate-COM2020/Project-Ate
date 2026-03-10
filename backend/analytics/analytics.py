from django.db.models import F, Sum, DecimalField, Count
from core.models import Reservation, BundlePosting

# assumed average weight per rescued bundle (kg), used as proxy for food waste saved
AVG_BUNDLE_WEIGHT_KG = 0.6

# price brackets used for pricing effectiveness analysis
_PRICE_BRACKETS = [
    (0,   3,   "£0-£3"),
    (3,   6,   "£3-£6"),
    (6,   10,  "£6-£10"),
    (10,  None, "£10+"),
]


def get_number_of_listings_by_seller(df, seller_id):
    # count listings belonging to a specific seller from dataframe
    seller_id = int(seller_id)
    subset = df[df["seller_id"] == seller_id]
    return len(subset)


def get_total_reservations_by_seller(seller_id):
    # get total reservations by joining reservation -> posting -> seller
    seller_id = int(seller_id)
    return Reservation.objects.filter(
        posting__seller__seller_id=seller_id
    ).count()


def get_total_revenue_by_seller(df, seller_id):
    # sum prices of bundles that were reserved or collected
    seller_id = int(seller_id)
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
    total = result["total_revenue"]
    return float(total) if total is not None else 0.0


def get_reduction_in_food_waste_by_seller(seller_id):
    # percentage of reservations that were collected (proxy for food not wasted)
    seller_id = int(seller_id)
    total = Reservation.objects.filter(
        posting__seller__seller_id=seller_id
    ).count()
    if total == 0:
        return 0.0

    collected = Reservation.objects.filter(
        posting__seller__seller_id=seller_id,
        status="collected",
    ).count()

    return round(collected / total * 100.0, 2)


def get_total_no_shows_by_seller(seller_id):
    # count reservations where customer did not show up
    seller_id = int(seller_id)
    return Reservation.objects.filter(
        posting__seller__seller_id=seller_id,
        status="no-show",
    ).count()


def get_collected_reservations_by_seller(seller_id):
    # count bundles that were successfully collected
    seller_id = int(seller_id)
    return Reservation.objects.filter(
        posting__seller__seller_id=seller_id,
        status="collected",
    ).count()


#  --------  sprint 2 analytics -------

def get_sell_through_breakdown(seller_id):
    # breakdown of reservation statuses and sell-through rate
    seller_id = int(seller_id)
    reservations = Reservation.objects.filter(
        posting__seller__seller_id=seller_id
    )
    total = reservations.count()
    if total == 0:
        return {
            "collected": 0,
            "no_show": 0,
            "expired": 0,
            "reserved": 0,
            "total": 0,
            "sell_through_rate": 0.0,
        }
    counts = {
        item["status"]: item["count"]
        for item in reservations.values("status").annotate(count=Count("reservation_id"))
    }
    collected = counts.get("collected", 0)

    return {
        "collected": collected,
        "no_show": counts.get("no-show", 0),
        "expired": counts.get("expired", 0),
        "reserved": counts.get("reserved", 0),
        "total": total,
        "sell_through_rate": round(collected / total * 100.0, 2),
    }


def get_waste_proxy(seller_id):
    # estimate kg of food waste avoided using average bundle weight
    seller_id = int(seller_id)
    collected = Reservation.objects.filter(
        posting__seller__seller_id=seller_id,
        status="collected",
    ).count()
    return {
        "bundles_collected": collected,
        "kg_saved": round(collected * AVG_BUNDLE_WEIGHT_KG, 2),
        "assumed_weight_kg_per_bundle": AVG_BUNDLE_WEIGHT_KG,
    }


def get_pricing_effectiveness(seller_id):
    # sell-through rate grouped by price brackets
    seller_id = int(seller_id)

    rows = list(
        Reservation.objects.filter(
            posting__seller__seller_id=seller_id
        ).values("posting__price", "status")
    )

    if not rows:
        return []

    result = []

    for low, high, label in _PRICE_BRACKETS:

        if high is None:
            bucket = [r for r in rows if float(r["posting__price"]) >= low]
        else:
            bucket = [r for r in rows if low <= float(r["posting__price"]) < high]

        total = len(bucket)

        if total == 0:
            continue

        collected = sum(1 for r in bucket if r["status"] == "collected")

        result.append({
            "price_range": label,
            "total_reservations": total,
            "collected": collected,
            "sell_through_rate": round(collected / total * 100.0, 2),
        })

    return result


def get_popular_categories(seller_id):
    # reservation counts per bundle category
    seller_id = int(seller_id)
    rows = (
        Reservation.objects.filter(posting__seller__seller_id=seller_id)
        .values("posting__category")
        .annotate(total_reservations=Count("reservation_id"))
        .order_by("-total_reservations")
    )

    return [
        {"category": r["posting__category"], "total_reservations": r["total_reservations"]}
        for r in rows
    ]


def get_best_pickup_windows(seller_id):
    # reservation counts per pickup window
    seller_id = int(seller_id)

    rows = (
        Reservation.objects.filter(posting__seller__seller_id=seller_id)
        .values("posting__pickup_window")
        .annotate(total_reservations=Count("reservation_id"))
        .order_by("-total_reservations")
    )

    return [
        {"pickup_window": r["posting__pickup_window"], "total_reservations": r["total_reservations"]}
        for r in rows]