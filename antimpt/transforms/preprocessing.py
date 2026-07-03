import pandas as pd


def cleanse_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    df.ffill(inplace=True)
    df.reset_index(names="date", inplace=True)

    return df


def filter_equity(df: pd.DataFrame, yr_from: int, yr_to: int) -> pd.DataFrame:
    df.dropna(inplace=True)
    df.index = df["date"]
    df = df[df.index.year.isin(range(yr_from, yr_to + 1))]

    return df[[
        "adx_07", "adx_14", "atr",
        "bbands_10_width", "bbands_20_width", "cci_10",
        "cci_20", "close", "crossover_06_12",
        "crossover_12_26", "fluctuation", "macd_06_12",
        "macd_12_26", "obv", "pivot_r1",
        "pivot_s1", "pivot_trend_ema10", "pivot_trend_ema20",
        "price", "return_ema05", "return_ema10",
        "return_ema20", "return", "rsi_07",
        "rsi_14", "signal_06_12", "signal_12_26",
        "ssma_03", "ssma_09", "ssma_12",
        "volatility_ema05", "volatility_ema10", "volatility_ema20",
    ]]
