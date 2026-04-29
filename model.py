from utils import compute_distance_km


def match_requests_priority(model, requests_df, donor_row, k=3):

    candidates = requests_df.copy()

    # -------- Features --------

    # 1. Need match
    candidates["need_match"] = (
        candidates["need_type"] == donor_row["donation_type"]
    ).astype(int)

    # 2. Quantity fit
    ratio = donor_row["available_quantity"] / candidates["needed_quantity"]
    candidates["quantity_fit"] = ratio.clip(upper=1)
    candidates.loc[ratio < 1, "quantity_fit"] *= 0.3

    # 3. Urgency
    candidates["urgency_score"] = candidates["urgency"].map({
    "منخفض": 1,
    "متوسط": 2,
    "عاجل": 3
}).fillna(1)

    # 4. Availability
    candidates["availability_score"] = {
        "خلال أسبوع": 1,
        "غدا": 2,
        "اليوم": 3
    }.get(donor_row["availability"], 1)
    
    # Location
    candidates["location_match"] = (
        candidates["location_requester"] == donor_row["location"]
    ).astype(int)

    candidates["trust_score"] = donor_row.get("trust_score", 0.5)
    
    # -------- Filtering --------
    candidates = candidates[
        (candidates["need_match"] == 1) &
        (candidates["quantity_fit"] > 0.1)
    ]

    if candidates.empty:
        return []

    # -------- Model Features --------
    FEATURE_COLS = [
    "need_match",
    "location_match",
    "urgency_score",
    "availability_score",
    "quantity_fit",
    "distance_score"
]
    # distance
    candidates["distance_km"] = candidates.apply(
        lambda row: compute_distance_km(row, donor_row),
        axis=1
    )

    candidates["distance_score"] = 1 / (1 + (candidates["distance_km"] / 50))
    
    X = candidates[FEATURE_COLS]
    print(X.columns)


    # -------- Prediction --------
    candidates["predicted_score"] = model.predict(X)

    # -------- Ranking --------
    candidates = candidates.sort_values(
        by="predicted_score",
        ascending=False
    )

    # -------- Output --------
    return candidates.head(k)[[
        "need_type",
        "urgency",
        "location_requester",
        "predicted_score"
    ]].to_dict(orient="records")