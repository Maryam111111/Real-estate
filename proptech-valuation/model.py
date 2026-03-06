import pandas as pd
import numpy as np
from xgboost import XGBRegressor


def train_model(df):

    df = df.dropna(subset=["price"])

    df["year"] = df["date"].dt.year

    X = df[["year"]]

    y = np.log(df["price"])

    model = XGBRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05
    )

    model.fit(X, y)

    return model