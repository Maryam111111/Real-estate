import numpy as np


def comparable_sales(df, postcode):

    area = postcode.split(" ")[0]

    comps = df[df["postcode"].str.startswith(area)]

    comps = comps.sort_values("date", ascending=False)

    return comps.head(50)


def price_per_sqft(df, fallback=350):
    """
    Compute average price per square foot.
    If no data is available, use a fallback estimate.
    """
    if df.empty:
        return fallback

    df = df.copy()

    # Assuming average house size 900 sqft if not available
    avg_area = 900

    # Calculate mean price per sqft
    return df["price"].mean() / avg_area

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
