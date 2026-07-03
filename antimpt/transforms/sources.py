from pathlib import Path

import pandas as pd
import yfinance as yf


PTH_RAW = Path("data", "raw")


def _fetch_market_data(ticker: str, yr: int = 2025) -> pd.DataFrame:
    return yf.Ticker(ticker).history(start=f"{yr - 1}-01-01")


def load_ticker(category: str, ticker: str, src: str, yr: int) -> pd.DataFrame:
    match src:
        case "cache":
            return pd.read_parquet(PTH_RAW / category / f"{ticker}.parquet")
        case "yfinance":
            return _fetch_market_data(ticker, yr)
        case _:
            raise ValueError(f"Unsupported source: {src}")


def list_tickers(category: str) -> list[str]:
    return [file.stem for file in (PTH_RAW / category).glob("*.parquet")]
