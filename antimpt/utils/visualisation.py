from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from matplotlib.ticker import FuncFormatter
from plotly.offline import plot

from .dataset import consolidate_data


matplotlib.use("Agg")

COLOUR_BLUE = "#63c5da"
COLOUR_GREEN = "#2e8b57"
COLOUR_RED = "#ba110c"
COLOUR_GREY = "#b8b4b4"
COLOUR_GREY_LIGHT = "#e5e7eb"
COLOUR_ORANGE = "#ffd3b0"


def format_thousand_unit(x: float, pos: int) -> str:
    return f"{x/1_000:,.0f}"


def plot_trading_actions(df: pd.DataFrame, ax: matplotlib.axes) -> None:
    ax.plot(
        df["trading_date"], df["price_close"],
        label="Price", color=COLOUR_BLUE,
    )
    ax.scatter(
        df["trading_date"], df["price_long"],
        label="LONG", color=COLOUR_GREEN,
        marker="^", alpha=0.5,
    )
    ax.scatter(
        df["trading_date"], df["price_short"],
        label="SHORT", color=COLOUR_RED,
        marker="v", alpha=0.5,
    )

    ax.set_title("Trading Actions")
    ax.set_xlabel("Date")
    ax.set_ylabel("USD (in thousands)")
    ax.legend()


def plot_trading_returns(df: pd.DataFrame, ax: matplotlib.axes) -> None:
    ax.plot(
        df["trading_date"], df["portfolio"],
        label="AntiMPT", color=COLOUR_GREEN \
            if df["portfolio"].iat[-1] > df["market_index"].iat[-1] \
            else COLOUR_RED,
    )
    ax.plot(
        df["trading_date"], df["market_index"],
        label="S&P Homebuilders ETF", color=COLOUR_ORANGE,
    )
    ax.plot(
        df["trading_date"], df["risk_free"],
        label="13-Week Treasury Bill", color=COLOUR_GREY,
    )

    ax.set_title("Return over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("USD (in thousands)")
    ax.yaxis.set_major_formatter(FuncFormatter(format_thousand_unit))
    ax.legend()


def plot_action_return(df: pd.DataFrame, artefact: list[str]) -> None:
    pth = Path("antimpt", "results", *artefact[:-1])
    pth.mkdir(parents=True, exist_ok=True)

    ax1, ax2 = plt.subplots(2, 1, figsize=(12, 8))[1]
    plot_trading_actions(df, ax1)
    plot_trading_returns(df, ax2)

    plt.tight_layout()
    plt.savefig(pth / f"{artefact[-1]}.png")


def visualise_returns(
    equity: pd.DataFrame,
    histories: list[dict[str, bool|float|int|str]],
    artefact: list[str],
) -> None:
    df = consolidate_data(equity, histories)

    plot_action_return(df, artefact)


def update_layout(fig: go.Figure, title: str, yaxis_title: str) -> None:
    fig.update_layout(
        title=title, yaxis_title=yaxis_title,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        legend={
            "x": 0, "y": 0,
            "traceorder": "normal",
            "font": {
                "family": "sans-serif",
                "size": 12,
                "color": "black",
            },
            "bgcolor": "rgba(255, 255, 255, 0.7)",
        },
        margin={"l": 20, "r": 20, "t": 30, "b": 20},
    )

    fig.update_xaxes(
        showgrid=True, zeroline=False,
        gridcolor=COLOUR_GREY_LIGHT, linecolor=COLOUR_GREY,
        tickcolor=COLOUR_GREY,
    )

    fig.update_yaxes(
        showgrid=True, zeroline=False,
        gridcolor=COLOUR_GREY_LIGHT, linecolor=COLOUR_GREY,
        tickcolor=COLOUR_GREY,
    )


def get_trading_actions(df: pd.DataFrame) -> str:
    figure = go.Figure([
        go.Scatter(
            x=df["trading_date"], y=df["price_close"],
            name="Price", mode="lines",
            line={"color": COLOUR_BLUE},
        ),
        go.Scatter(
            x=df["trading_date"], y=df["price_long"],
            name="Buy", mode="markers",
            marker={"color": COLOUR_GREEN, "size": 9, "symbol": "triangle-up"},
        ),
        go.Scatter(
            x=df["trading_date"], y=df["price_short"],
            name="Sell", mode="markers",
            marker={"color": COLOUR_RED, "size": 9, "symbol": "triangle-down"},
        ),
    ])

    update_layout(figure, "Trading Actions", "Close Price")

    return plot(figure, output_type="div", config={"responsive": True})


def get_trading_returns(df: pd.DataFrame) -> str:
    figure = go.Figure([
        go.Scatter(
            x=df["trading_date"], y=df["portfolio"],
            name="AntiMPT", mode="lines",
            line={
                "color": COLOUR_GREEN \
                    if df["portfolio"].iat[-1] > df["market_index"].iat[-1] \
                    else COLOUR_RED
            },
        ),
        go.Scatter(
            x=df["trading_date"], y=df["market_index"],
            name="S&P Homebuilders ETF", mode="lines",
            line={"color": COLOUR_ORANGE},
        ),
        go.Scatter(
            x=df["trading_date"], y=df["risk_free"],
            name="13-Week Treasury Bill", mode="lines",
            line={"color": COLOUR_GREY},
        ),
    ])

    update_layout(figure, "Return over Time", "USD (in thousands)")

    return plot(figure, output_type="div", config={"responsive": True})


def get_interactive_graphs(df: pd.DataFrame) -> dict[str, str]:
    actions = get_trading_actions(df)
    returns = get_trading_returns(df)

    return {"plot_actions": actions, "plot_returns": returns}
