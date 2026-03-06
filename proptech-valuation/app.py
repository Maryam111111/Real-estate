import streamlit as st
import numpy as np

from data_loader import load_price_paid_data
from geo_features import postcode_to_coordinates, distance_to_station
from pricing_engine import (
    comparable_sales,
    price_per_sqft,
    baseline_price,
    hedonic_adjustment,
    location_premium,
    build_cost
)

# ----------------------------
# Streamlit page config
# ----------------------------
st.set_page_config(page_title="Quant Property Valuation", layout="centered")

st.title("🏠 Property Valuation Engine")
st.markdown("""
Estimates property value based on UK Land Registry data, postcode, and property features.
""")

# ----------------------------
# User Inputs
# ----------------------------
postcode = st.text_input("Enter UK Postcode (e.g., SW1A 1AA)")

col1, col2 = st.columns(2)

with col1:
    area = st.number_input(
        "Floor Area (sqft)",
        min_value=200,
        max_value=10000,
        value=900,
        step=50
    )

    bedrooms = st.number_input(
        "Bedrooms",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )

with col2:
    bathrooms = st.number_input(
        "Bathrooms",
        min_value=1,
        max_value=6,
        value=1,
        step=1
    )

# ----------------------------
# Estimate Property Value
# ----------------------------
if st.button("Estimate Property Value"):

    # Load sample data
    df = load_price_paid_data()

    # Get comparable sales
    comps = comparable_sales(df, postcode)

    if comps.empty:
        st.warning("No comparable sales found for this postcode. Using default fallback price per sqft.")
    
    # Calculate price per sqft (with fallback)
    ppsqft = price_per_sqft(comps, fallback=350)

    st.write(f"Local Price per Sqft: £{ppsqft:,.0f}")

    # Baseline price
    base_price = baseline_price(ppsqft, area)

    # Hedonic adjustments
    price = hedonic_adjustment(base_price, bedrooms, bathrooms, garden, detached)

    # Geospatial adjustment
    coords = postcode_to_coordinates(postcode)
    if coords is None:
        st.warning("Postcode not found. Skipping distance-to-station adjustment.")
        distance = 0
    else:
        lat, lon = coords
        distance = distance_to_station(lat, lon)
        price = location_premium(price, distance)
        st.write(f"Distance to nearest station: {distance:.0f} meters")

    # Construction cost
    build = build_cost(area)

    # Ensure final price is valid
    if np.isnan(price) or price <= 0:
        st.error("Could not calculate a valid property value.")
        price = 0

    # Display results
    st.success(f"Estimated Property Value: £{price:,.0f}")
    st.info(f"Estimated Construction Cost: £{build:,.0f}")
