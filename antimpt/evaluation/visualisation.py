from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.ticker import FuncFormatter

from ..market import consolidate_data
from ..models import ChartColours

matplotlib.use("Agg")


def _format_thousand_unit(x: float, pos: int) -> str:
    return f"{x/1_000:,.0f}"


def _plot_trading_actions(df: pd.DataFrame, ax: Axes) -> None:
    ax.plot(
        df["trading_date"], df["price_close"],
        label="Price", color=ChartColours.BLUE.value,
    )
    ax.scatter(
        df["trading_date"], df["price_long"],
        label="LONG", color=ChartColours.GREEN.value,
        marker="^", alpha=0.5,
    )
    ax.scatter(
        df["trading_date"], df["price_short"],
        label="SHORT", color=ChartColours.RED.value,
        marker="v", alpha=0.5,
    )

    ax.set_title("Trading Actions")
    ax.set_xlabel("Date")
    ax.set_ylabel("USD (in thousands)")
    ax.legend()


def _plot_trading_returns(df: pd.DataFrame, ax: Axes) -> None:
    ax.plot(
        df["trading_date"], df["portfolio"],
        label="AntiMPT",
        color=(
            ChartColours.GREEN.value
            if df["portfolio"].iat[-1] > df["market_index"].iat[-1]
            else ChartColours.RED.value
        ),
    )
    ax.plot(
        df["trading_date"], df["market_index"],
        label="S&P Homebuilders ETF", color=ChartColours.ORANGE.value,
    )
    ax.plot(
        df["trading_date"], df["risk_free"],
        label="13-Week Treasury Bill", color=ChartColours.GREY.value,
    )

    ax.set_title("Return over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("USD (in thousands)")
    ax.yaxis.set_major_formatter(FuncFormatter(_format_thousand_unit))
    ax.legend()


def _plot_action_return(df: pd.DataFrame, artefact: list[str]) -> None:
    pth = Path("runs", *artefact[:-1])
    pth.mkdir(parents=True, exist_ok=True)

    ax1, ax2 = plt.subplots(2, 1, figsize=(12, 8))[1]
    _plot_trading_actions(df, ax1)
    _plot_trading_returns(df, ax2)

    plt.tight_layout()
    plt.savefig(pth / f"{artefact[-1]}.png")


def visualise_returns(
    equity: pd.DataFrame,
    histories: list[dict[str, bool | float | int | str]],
    artefact: list[str],
) -> None:
    df = consolidate_data(equity, histories)

    _plot_action_return(df, artefact)
