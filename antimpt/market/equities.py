import pandas as pd

from ..transforms import (
    cleanse_data,
    filter_equity,
    get_fluctuations,
    get_indicators,
    list_tickers,
    load_ticker,
)


def get_equity(
    yr_from: int,
    yr_to: int,
    ticker: str,
    src: str = "cache",
) -> pd.DataFrame:
    df = load_ticker("equities", ticker, src, yr_from) \
        .pipe(cleanse_data) \
        .pipe(get_fluctuations) \
        .pipe(get_indicators) \
        .pipe(filter_equity, yr_from, yr_to)

    return df


def get_equities(
    yr_from: int,
    yr_to: int,
    ticker: str | None = None,
    src: str = "cache",
) -> list[pd.DataFrame]:
    if ticker:
        return [get_equity(yr_from, yr_to, ticker, src)]
    if src != "cache":
        raise ValueError("ticker is required when src is not 'cache'")

    return [
        get_equity(yr_from, yr_to, cached_ticker, src)
        for cached_ticker in list_tickers("equities")
    ]
