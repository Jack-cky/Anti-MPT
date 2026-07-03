import random

import numpy as np
import pandas as pd
from finta import TA
from scipy.signal import find_peaks


SEED = 42
random.seed(SEED)
np.random.seed(SEED)


def get_fluctuations(df: pd.DataFrame) -> pd.DataFrame:
    df["fluctuation"] = 0.0
    peaks, _ = find_peaks(df["close"])
    df.loc[peaks, "fluctuation"] = 1
    bottoms, _ = find_peaks(-df["close"])
    df.loc[bottoms, "fluctuation"] = -1

    transition = df.query("fluctuation != 0")["fluctuation"]
    for i in range(len(transition) - 1):
        cur, nxt = transition.index[i : i + 2]
        for j in range(cur + 1, nxt):
            df.at[j, "fluctuation"] = transition.at[nxt] \
                * np.exp(-0.7 * (nxt - j))

    return df


def get_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df["price"] = np.random.uniform(df["low"], df["high"]).round(2)

    df["return"] = np.log1p(df["close"].pct_change())
    df["return_ema20"] = df["return"].ewm(span=20).mean()
    df["return_ema10"] = df["return"].ewm(span=10).mean()
    df["return_ema05"] = df["return"].ewm(span=5).mean()

    df["volatility_ema20"] = df["return"].ewm(span=20).std()
    df["volatility_ema10"] = df["return"].ewm(span=10).std()
    df["volatility_ema05"] = df["return"].ewm(span=5).std()

    df["ssma_12"] = TA.SSMA(df, 12)
    df["ssma_09"] = TA.SSMA(df)
    df["ssma_03"] = TA.SSMA(df, 3)

    df[["macd_12_26", "signal_12_26"]] = TA.MACD(df)
    df["crossover_12_26"] = df["macd_12_26"] - df["signal_12_26"]
    df[["macd_06_12", "signal_06_12"]] = TA.MACD(df, 6, 12)
    df["crossover_06_12"] = df["macd_06_12"] - df["signal_06_12"]

    df["adx_14"] = TA.ADX(df)
    df["adx_07"] = TA.ADX(df, 7)

    df["rsi_14"] = TA.RSI(df)
    df["rsi_07"] = TA.RSI(df, 7)

    df["cci_20"] = TA.CCI(df)
    df["cci_10"] = TA.CCI(df, 10)

    df["bbands_20_width"] = TA.BBANDS(df).eval("BB_UPPER-BB_LOWER")
    df["bbands_10_width"] = TA.BBANDS(df, 10).eval("BB_UPPER-BB_LOWER")

    df["obv"] = TA.OBV(df)

    df[["pivot_r1", "pivot_s1"]] = TA.PIVOT(df)[["r1", "s1"]]
    df["pivot_trend_ema20"] = (df["close"] - df["pivot_r1"]) \
        .ewm(span=20).mean()
    df["pivot_trend_ema10"] = (df["close"] - df["pivot_r1"]) \
        .ewm(span=10).mean()

    df["atr"] = TA.ATR(df)

    return df
