from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from ..transforms import cleanse_data, load_ticker


def get_risk_free(
    start: str,
    end: str,
    funds: float = 10_000,
    mths: int = 4,
    ticker: str = "^IRX",
    src: str = "cache",
) -> pd.DataFrame:
    df = load_ticker("bills", ticker, src, int(start[:4]) + 1)
    df = cleanse_data(df)
    df.index = df["date"].dt.strftime("%Y-%m-%d")

    available = df.index[df.index >= start]
    if len(available) == 0:
        raise ValueError(f"No risk-free data on or after {start}")
    start = available[0]

    dates, rates = [], []
    while start < end:
        dates.append(start)
        rates.append(1 + df.at[start, "close"] / 100 / mths)
        start = datetime.strptime(start, "%Y-%m-%d") + timedelta(days=13 * 7)

        while (
            start.strftime("%Y-%m-%d") not in df.index
            and start.strftime("%Y-%m-%d") < end
        ):
            start += timedelta(days=1)
        start = start.strftime("%Y-%m-%d")

    return pd.DataFrame({
        "date": dates,
        "risk_free": np.cumprod([funds] + list(rates))[:-1],
    })


def get_market_index(
    start: str,
    funds: float = 10_000,
    ticker: str = "XHB",
    src: str = "cache",
) -> pd.DataFrame:
    df = load_ticker("indices", ticker, src, int(start[:4]) + 1)
    df = cleanse_data(df)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    df["market_index"] = (
        df["close"] * (funds // df.query("date >= @start")["close"].iat[0])
    )

    return df[["date", "market_index"]]
