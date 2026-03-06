import streamlit as st

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

st.set_page_config(page_title="Quant Property Valuation", layout="centered")

st.title("🏠 Quant Property Valuation Engine")

st.markdown(
"""
Hedonic Pricing + Comparable Sales + Geospatial Factors
"""
)

postcode = st.text_input("Enter UK Postcode")

col1, col2 = st.columns(2)

with col1:
    area = st.slider("Floor Area (sqft)", 400, 4000, 900)
    bedrooms = st.slider("Bedrooms", 1, 6, 2)

with col2:
    bathrooms = st.slider("Bathrooms", 1, 4, 1)
    garden = st.checkbox("Garden")
    detached = st.checkbox("Detached")

if st.button("Estimate Property Value"):

    df = load_price_paid_data()

    comps = comparable_sales(df, postcode)

    ppsqft = price_per_sqft(comps)

    base = baseline_price(ppsqft, area)

    price = hedonic_adjustment(
        base,
        bedrooms,
        bathrooms,
        garden,
        detached
    )

    coords = postcode_to_coordinates(postcode)

    if coords:

        lat, lon = coords

        distance = distance_to_station(lat, lon)

        price = location_premium(price, distance)

        st.write(f"Distance to Station: {distance:.0f} meters")

    build = build_cost(area)

    st.success(f"Estimated Property Value: £{price:,.0f}")

    st.info(f"Estimated Construction Cost: £{build:,.0f}")

    st.write(f"Local Price per Sqft: £{ppsqft:.0f}")