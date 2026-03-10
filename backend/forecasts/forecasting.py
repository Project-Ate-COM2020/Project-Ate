import pandas as pd
import numpy as np
from datetime import datetime

DAY_NAMES = {
    1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday",
    5: "Friday", 6: "Saturday", 7: "Sunday",
}

# ── core helpers ──────────────────────────────────────────────────────────────

def get_adjacent_days(day_of_week):
    """Return [previous_day, current_day, next_day] wrapping 1-7."""
    d = int(day_of_week)
    return [7 if d == 1 else d - 1, d, 1 if d == 7 else d + 1]


def get_adjacent_time_slots(time_range):
    """
    Given '10:00-11:00' return the previous, current, and next hourly slots.
    Returns: ['09:00-10:00', '10:00-11:00', '11:00-12:00']
    """
    start_str, end_str = time_range.split('-')
    start = datetime.strptime(start_str, "%H:%M")
    end = datetime.strptime(end_str, "%H:%M")
    duration = end - start
    return [
        f"{(start - duration).strftime('%H:%M')}-{start.strftime('%H:%M')}",
        f"{start.strftime('%H:%M')}-{end.strftime('%H:%M')}",
        f"{end.strftime('%H:%M')}-{(end + duration).strftime('%H:%M')}",
    ]


def get_similar_listings(df, inp):
    """Filter historical records to adjacent days/time-slots for the same category."""
    adjacent_days = get_adjacent_days(inp["day_of_week"])
    similar_times = get_adjacent_time_slots(inp["time_window"])
    return df[
        (df["category"] == inp["category"])
        & (df["day_of_week"].isin(adjacent_days))
        & (df["time_window"].isin(similar_times))
    ]


def _reservation_rate(subset):
    """Fraction of total posted stock that was actually reserved."""
    res = subset["observed_reservations"].sum()
    total = (
        res
        + subset["observed_no_show"].sum()
        + subset["unreserved_stock"].fillna(0).sum()
    )
    return res / total if total > 0 else 0.0


def get_no_show_probability(subset):
    """No-show probability = observed_no_show / observed_reservations."""
    if len(subset) == 0:
        return 0.0
    total_reservations = subset["observed_reservations"].sum()
    if total_reservations == 0:
        return 0.0
    return float(subset["observed_no_show"].sum() / total_reservations)


def get_expected_no_show_count(subset, inp):
    """Expected number of no-shows = no_show_probability × no_bundles."""
    return round(get_no_show_probability(subset) * inp["no_bundles"], 2)


def get_expected_reservations(subset, inp):
    """Legacy helper: reservation_rate × no_bundles (used by existing tests)."""
    return round(_reservation_rate(subset) * inp["no_bundles"], 2)


# baseline 1: seasonal naive

def seasonal_naive_predict(df, inp):
    """
    Baseline 1 – Seasonal Naive.

    Predicts demand using the average reservation rate observed on the exact
    same day-of-week + time-window + category.  Falls back to category-only
    if no exact slot match exists.

    Returns: (predicted_reservations, no_show_probability)
    """
    exact = df[
        (df["category"] == inp["category"])
        & (df["day_of_week"] == int(inp["day_of_week"]))
        & (df["time_window"] == inp["time_window"])
    ]
    if exact.empty:
        exact = df[df["category"] == inp["category"]]
    if exact.empty:
        return 0.0, 0.0
    rate = _reservation_rate(exact)
    return round(rate * inp["no_bundles"], 2), round(get_no_show_probability(exact), 4)


# baseline 2: moving average

def moving_average_predict(df, inp, window=10):
    """
    Baseline 2: Moving Average.

    Takes the last ``window`` records for the same category (ordered by
    record_id ascending) and averages their reservation rate.

    Returns: (predicted_reservations, no_show_probability)
    """
    cat_df = df[df["category"] == inp["category"]]
    if cat_df.empty:
        cat_df = df
    if cat_df.empty:
        return 0.0, 0.0
    window_df = cat_df.sort_values("record_id").tail(window)
    rate = _reservation_rate(window_df)
    return round(rate * inp["no_bundles"], 2), round(get_no_show_probability(window_df), 4)


# main approach: weighted similarity

def similarity_predict(df, inp):
    """
    Main approach: Weighted Similarity.

    Builds a neighbourhood of historically similar postings (adjacent days,
    adjacent time-slots, same category).  Two enhancements over the baselines:

    1. Weather weighting: records whose weather_flag matches the requested
       flag are double-weighted, reflecting that bad-weather days behave
       differently from fair-weather days.

    2. Price sensitivity: if a posted price is provided the reservation rate
       is scaled by (avg_historical_price / posted_price), clamped to [0.5, 1.5].
       A lower-than-average price boosts uptake; a higher price suppresses it.

    Returns: (predicted_reservations, no_show_probability)
    """
    subset = get_similar_listings(df, inp)
    if subset.empty:
        return 0.0, 0.0

    if inp.get("weather_flag") is not None and "weather_flag" in subset.columns:
        weights = subset["weather_flag"].apply(
            lambda w: 2.0 if int(w) == int(inp["weather_flag"]) else 1.0
        )
        w_res = float((subset["observed_reservations"] * weights).sum())
        w_no_show = float((subset["observed_no_show"] * weights).sum())
        w_unreserved = float((subset["unreserved_stock"].fillna(0) * weights).sum())
        total = w_res + w_no_show + w_unreserved
        if total == 0:
            return 0.0, 0.0
        rate = w_res / total
        no_show_prob = w_no_show / w_res if w_res > 0 else 0.0
    else:
        rate = _reservation_rate(subset)
        no_show_prob = get_no_show_probability(subset)

    # Price sensitivity adjustment
    if inp.get("price") is not None and "price" in subset.columns:
        avg_price = float(subset["price"].mean())
        if avg_price > 0:
            price_factor = max(0.5, min(avg_price / float(inp["price"]), 1.5))
            rate = rate * price_factor

    return round(rate * inp["no_bundles"], 2), round(no_show_prob, 4)


# cross-validation / error metrics

def _loo_row(train_df, row):
    """
    Evaluate all three approaches on a single held-out row using leave-one-out.
    Returns (actual, sn_pred, ma_pred, sim_pred) or None if row is unusable.
    """
    total_stock = (
        int(row["observed_reservations"])
        + int(row["observed_no_show"])
        + int(row["unreserved_stock"] if pd.notna(row.get("unreserved_stock")) else 0)
    )
    if total_stock == 0:
        return None

    test_inp = {
        "category": row["category"],
        "day_of_week": int(row["day_of_week"]),
        "time_window": row["time_window"],
        "weather_flag": int(row["weather_flag"]),
        "no_bundles": total_stock,
        "price": float(row["price"]) if pd.notna(row.get("price")) else None,
    }
    actual = int(row["observed_reservations"])
    sn, _ = seasonal_naive_predict(train_df, test_inp)
    ma, _ = moving_average_predict(train_df, test_inp)
    sim, _ = similarity_predict(train_df, test_inp)
    return actual, sn, ma, sim


def evaluate_baselines(df):
    """
    Leave-one-out cross-validation across the full historical dataset.

    Compares Seasonal Naive, Moving Average, and Weighted Similarity using
    Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).

    Returns a dict keyed by approach name, each with mae, rmse, and n.
    """
    actuals, sn_preds, ma_preds, sim_preds = [], [], [], []

    for idx in df.index:
        train = df.drop(index=idx)
        if train.empty:
            continue
        pair = _loo_row(train, df.loc[idx])
        if pair is None:
            continue
        actual, sn, ma, sim = pair
        actuals.append(actual)
        sn_preds.append(sn)
        ma_preds.append(ma)
        sim_preds.append(sim)

    if not actuals:
        empty = {"mae": None, "rmse": None, "n": 0}
        return {"seasonal_naive": empty, "moving_average": empty, "similarity": empty}

    a = np.array(actuals, dtype=float)
    n = len(a)

    def _metrics(preds):
        p = np.array(preds, dtype=float)
        return {
            "mae": round(float(np.mean(np.abs(a - p))), 3),
            "rmse": round(float(np.sqrt(np.mean((a - p) ** 2))), 3),
            "n": n,
        }

    return {
        "seasonal_naive": _metrics(sn_preds),
        "moving_average": _metrics(ma_preds),
        "similarity": _metrics(sim_preds),
    }


def _best_approach(metrics):
    """Return the approach name with the lowest RMSE."""
    best, best_rmse = "similarity", float("inf")
    for name, m in metrics.items():
        if m["rmse"] is not None and m["rmse"] < best_rmse:
            best_rmse, best = m["rmse"], name
    return best


# confidence

def get_confidence_level(n_records, best_rmse):
    """
    Classify forecast confidence.
      low   fewer than 5 similar records, or RMSE > 5
      medium 5-19 records and RMSE ≤ 5
      high 20+ records and RMSE ≤ 2
    """
    if n_records < 5:
        return "low"
    if best_rmse is not None and best_rmse > 5:
        return "low"
    if n_records >= 20 and (best_rmse is None or best_rmse <= 2):
        return "high"
    return "medium"


# ── recommendation ────────────────────────────────────────────────────────────

def generate_recommendation(inp, predicted_reservations, no_show_prob, n_records):
    """
    Generate a human-readable action and rationale for the seller.

    Strategy: target an 85% fill-rate.  If the predicted fill-rate is below
    that threshold recommend reducing quantity; if comfortably above, note
    that an increase is feasible.

    Returns: { "action": str, "rationale": str }
    """
    no_bundles = inp["no_bundles"]
    day_name = DAY_NAMES.get(int(inp["day_of_week"]), f"day {inp['day_of_week']}")
    slot = inp["time_window"]
    category = inp["category"]

    fill_rate = predicted_reservations / no_bundles if no_bundles > 0 else 0.0
    TARGET = 0.85
    optimal_qty = max(1, round(predicted_reservations / TARGET)) if fill_rate < TARGET else no_bundles

    parts = []

    if fill_rate < TARGET and optimal_qty < no_bundles:
        action = (
            f"Post {optimal_qty} bundle{'s' if optimal_qty != 1 else ''} "
            f"instead of {no_bundles} for {day_name} {slot}"
        )
        parts.append(
            f"Based on {n_records} similar historical postings, only "
            f"{predicted_reservations:.1f} reservations are expected from "
            f"{no_bundles} bundles ({fill_rate * 100:.0f}% fill rate). "
            f"Reducing to {optimal_qty} bundles targets an 85% fill rate "
            f"and minimises unsold food."
        )
    elif fill_rate >= TARGET:
        headroom = max(no_bundles, round(predicted_reservations / TARGET))
        action = f"Your quantity of {no_bundles} bundles looks appropriate for {day_name} {slot}"
        parts.append(
            f"Demand for {category} on {day_name} {slot} is strong "
            f"({fill_rate * 100:.0f}% expected fill rate from {n_records} similar records). "
        )
        if headroom > no_bundles:
            parts.append(
                f"You could increase to {headroom} bundles and still expect strong uptake."
            )
    else:
        action = f"Post {no_bundles} bundles for {day_name} {slot}"
        parts.append(f"Fill-rate estimate is {fill_rate * 100:.0f}% from {n_records} records.")

    if no_show_prob > 0.25:
        parts.append(
            f"No-show probability is elevated ({no_show_prob * 100:.0f}%). "
            f"Consider a shorter claim window to reduce wasted reservations."
        )

    if inp.get("price") is not None:
        parts.append(f"Price sensitivity factored in at £{float(inp['price']):.2f} per bundle.")

    if inp.get("weather_flag") == 1:
        parts.append("Adverse weather is flagged — this historically reduces reservation uptake.")

    return {"action": action, "rationale": " ".join(parts)}


# price helper

def calculate_recommended_price(subset, inp):
    """
    Recommended price = avg_historical_price x (1 - no_show_prob) x (1 + demand_factor).
    demand_factor reflects how many similar listings exist (more = higher demand).
    """
    if len(subset) == 0:
        return 0.0
    base_price = float(subset["price"].mean())
    no_show_prob = get_no_show_probability(subset)
    demand_factor = min(len(subset) / 10, 1)
    return round(base_price * (1 - no_show_prob) * (1 + demand_factor), 2)