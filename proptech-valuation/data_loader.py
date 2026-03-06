import pandas as pd


def load_price_paid_data():

    df = pd.read_csv(
        "data/uk_price_paid_sample.csv",
        names=[
            "transaction_id",
            "price",
            "date",
            "postcode",
            "property_type",
            "new_build",
            "tenure",
            "paon",
            "saon",
            "street",
            "locality",
            "town",
            "district",
            "county",
            "category"
        ]
    )

    df["date"] = pd.to_datetime(df["date"])

    return df