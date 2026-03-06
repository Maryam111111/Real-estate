import numpy as np


def comparable_sales(df, postcode):
    """
    Find comparable sales based on postcode.
    
    Priority:
    1. Exact postcode
    2. Postcode district (first part, e.g. SW3)
    3. First 3 characters (fallback)
    """

    postcode = postcode.upper().strip()

    # ----------------
    # 1 Exact match
    # ----------------
    exact = df[df["postcode"] == postcode]

    if not exact.empty:
        return exact

    # ----------------
    # 2 District match (SW3)
    # ----------------
    district = postcode.split(" ")[0]
    district_matches = df[df["postcode"].str.startswith(district)]

    if not district_matches.empty:
        return district_matches

    # ----------------
    # 3 First 3 characters fallback
    # ----------------
    prefix3 = postcode[:3]
    prefix_matches = df[df["postcode"].str.startswith(prefix3)]

    if not prefix_matches.empty:
        return prefix_matches

    # ----------------
    # 4 Last fallback: return entire dataset
    # ----------------
    return df


def price_per_sqft(df, fallback=500):
    """
    Calculate price per sqft safely.
    """

    if df.empty:
        return fallback

    avg_area = 900

    price = df["price"].median()

    ppsqft = price / avg_area

    if ppsqft < 100 or np.isnan(ppsqft):
        return fallback

    return ppsqft
def baseline_price(price_sqft, area):

    return price_sqft * area


def hedonic_adjustment(price, bedrooms, bathrooms, garden, detached):

    price += bedrooms * 20000
    price += bathrooms * 15000

    if garden:
        price += 30000

    if detached:
        price *= 1.2

    return price


def location_premium(price, distance):

    factor = np.exp(-distance / 1200)

    return price * (1 + factor * 0.1)


def build_cost(area):

    cost_sqft = 150

    return area * cost_sqft
