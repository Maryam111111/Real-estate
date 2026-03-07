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
    Uses actual area if available, otherwise estimates based on price distribution.
    """

    if df.empty:
        return fallback

    # Remove invalid prices
    df_clean = df[df["price"] > 0].copy()
    
    if df_clean.empty:
        return fallback

    # Check if area column exists and has valid data
    if "area" in df_clean.columns:
        df_clean = df_clean[df_clean["area"] > 0]
        if not df_clean.empty:
            # Calculate actual price per sqft
            ppsqft = (df_clean["price"] / df_clean["area"]).median()
            if ppsqft > 0 and not np.isnan(ppsqft):
                return ppsqft

    # Fallback: estimate ppsqft from price distribution
    # Assumes median property is ~1000 sqft (typical UK home)
    median_price = df_clean["price"].median()
    estimated_ppsqft = median_price / 1000

    if estimated_ppsqft < 100 or np.isnan(estimated_ppsqft):
        return fallback

    return estimated_ppsqft


def baseline_price(price_sqft, area):
    """
    Calculate baseline price from price per sqft and area.
    Includes validation for both parameters.
    """
    if area <= 0 or price_sqft <= 0:
        return 0
    
    if np.isnan(area) or np.isnan(price_sqft):
        return 0

    return price_sqft * area


def hedonic_adjustment(price, bedrooms, bathrooms, garden, detached):
    """
    Apply property feature adjustments using percentage-based multipliers.
    This scales better across different price ranges.
    """
    if price <= 0 or np.isnan(price):
        return price

    # Percentage-based adjustments (more realistic)
    price *= (1 + bedrooms * 0.08)    # 8% per bedroom
    price *= (1 + bathrooms * 0.06)   # 6% per bathroom

    if garden:
        price *= 1.15  # 15% garden premium

    if detached:
        price *= 1.20  # 20% detached premium

    return price


def location_premium(price, distance):
    """
    Apply location adjustment based on distance to nearest station.
    
    Closer to station = higher premium.
    Uses exponential decay with 1200m half-life.
    """
    if price <= 0 or distance < 0:
        return price
    
    # Exponential decay: closer stations get stronger premium
    factor = np.exp(-distance / 1200)
    
    # Cap the premium at ±25% to avoid unrealistic adjustments
    premium = factor * 0.25
    premium = np.clip(premium, -0.25, 0.25)

    return price * (1 + premium)


def build_cost(area):
    """
    Estimate construction cost based on area.
    Uses UK market standard of £150-200 per sqft.
    """
    if area <= 0 or np.isnan(area):
        return 0

    cost_per_sqft = 150
    return area * cost_per_sqft
