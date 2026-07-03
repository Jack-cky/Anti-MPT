import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

from ..models import ChartColours


def _update_layout(fig: go.Figure, title: str, yaxis_title: str) -> None:
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
        gridcolor=ChartColours.GREY_LIGHT.value,
        linecolor=ChartColours.GREY.value,
        tickcolor=ChartColours.GREY.value,
    )
    fig.update_yaxes(
        showgrid=True, zeroline=False,
        gridcolor=ChartColours.GREY_LIGHT.value,
        linecolor=ChartColours.GREY.value,
        tickcolor=ChartColours.GREY.value,
    )


def _get_reference_frame(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values("trading_date") \
        .drop_duplicates(subset=["trading_date"])


def _get_trading_actions(df: pd.DataFrame) -> str:
    reference_df = _get_reference_frame(df)
    figure = go.Figure([
        go.Scatter(
            x=reference_df["trading_date"], y=reference_df["price_close"],
            name="Price", mode="lines",
            line={"color": ChartColours.BLACK.value},
        ),
    ])
    figure.add_trace(go.Scatter(
        x=df["trading_date"], y=df["price_long"],
        name="Buy", mode="markers",
        marker={
            "color": ChartColours.GREEN.value,
            "size": 9,
            "symbol": "triangle-up",
        },
    ))
    figure.add_trace(go.Scatter(
        x=df["trading_date"], y=df["price_short"],
        name="Sell", mode="markers",
        marker={
            "color": ChartColours.RED.value,
            "size": 9,
            "symbol": "triangle-down",
        },
    ))

    _update_layout(figure, "Trading Actions", "Close Price")

    return plot(figure, output_type="div", config={"responsive": True})


def _get_trading_returns(df: pd.DataFrame) -> str:
    reference_df = _get_reference_frame(df)

    figure = go.Figure()
    figure.add_trace(go.Scatter(
        x=df["trading_date"], y=df["portfolio"],
        name="AntiMPT", mode="lines",
        line={
            "color": (
                ChartColours.GREEN.value
                if df["portfolio"].iat[-1] > df["market_index"].iat[-1]
                else ChartColours.RED.value
            )
        },
    ))
    figure.add_trace(go.Scatter(
        x=reference_df["trading_date"], y=reference_df["market_index"],
        name="S&P Homebuilders ETF", mode="lines",
        line={"color": ChartColours.ORANGE.value},
    ))
    figure.add_trace(go.Scatter(
        x=reference_df["trading_date"], y=reference_df["risk_free"],
        name="13-Week Treasury Bill", mode="lines",
        line={"color": ChartColours.GREY.value},
    ))

    _update_layout(figure, "Return over Time", "USD (in thousands)")

    return plot(figure, output_type="div", config={"responsive": True})


def get_interactive_graphs(df: pd.DataFrame) -> dict[str, str]:
    actions = _get_trading_actions(df)
    returns = _get_trading_returns(df)

    return {"plot_actions": actions, "plot_returns": returns}
