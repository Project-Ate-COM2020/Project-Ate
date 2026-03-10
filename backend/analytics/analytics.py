from django.db.models import F, Sum, DecimalField, Count
from core.models import Reservation, BundlePosting

# Assumed average weight per rescued bundle (kg). Documented assumption for waste proxy.
AVG_BUNDLE_WEIGHT_KG = 0.6

# Price brackets used for pricing effectiveness analysis
_PRICE_BRACKETS = [
    (0,   3,   "£0-£3"),
    (3,   6,   "£3-£6"),
    (6,   10,  "£6-£10"),
    (10,  None, "£10+"),
]


def get_number_of_listings_by_seller(df, seller_id):
    seller_id = int(seller_id)
    subset = df[df["seller_id"] == seller_id]
    return len(subset)


def get_total_reservations_by_seller(seller_id):
    """Get total reservations for a seller by joining Reservation -> Posting -> Seller"""
    seller_id = int(seller_id)
    return Reservation.objects.filter(
        posting__seller__seller_id=seller_id
    ).count()


def get_total_revenue_by_seller(df, seller_id):
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
    """
    % of reservations that were collected (proxy for food not wasted).
    Fixed: uses Reservation.status='collected', not BundlePosting.status.
    """
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
    """Get total no-shows for a seller by joining Reservation -> Posting -> Seller"""
    seller_id = int(seller_id)
    return Reservation.objects.filter(
        posting__seller__seller_id=seller_id,
        status="no-show",
    ).count()


def get_collected_reservations_by_seller(seller_id):
    """Get total collected reservations for a seller by joining Reservation -> Posting -> Seller"""
    seller_id = int(seller_id)
    return Reservation.objects.filter(
        posting__seller__seller_id=seller_id,
        status="collected",
    ).count()


# ── Sprint 2 analytics ────────────────────────────────────────────────────────

def get_sell_through_breakdown(seller_id):
    """
    Full status breakdown for a seller's reservations.
    Returns collected/no-show/expired/reserved counts plus a sell_through_rate
    (collected / total reservations * 100).
    """
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
    """
    Estimate kg of food waste avoided.
    Assumption: each collected bundle weighs AVG_BUNDLE_WEIGHT_KG (0.6 kg).
    Source: WRAP UK average surplus food bundle weight estimate.
    """
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
    """
    Sell-through rate grouped by price bracket.
    Helps sellers see whether cheaper bundles sell better.
    Returns a list ordered by price bracket ascending.
    """
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
    """Reservation counts per bundle category, ordered by popularity descending."""
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
    """Reservation counts per pickup window, ordered by popularity descending."""
    seller_id = int(seller_id)
    rows = (
        Reservation.objects.filter(posting__seller__seller_id=seller_id)
        .values("posting__pickup_window")
        .annotate(total_reservations=Count("reservation_id"))
        .order_by("-total_reservations")
    )
    return [
        {"pickup_window": r["posting__pickup_window"], "total_reservations": r["total_reservations"]}
        for r in rows
    ]
