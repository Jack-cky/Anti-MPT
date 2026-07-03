import random
from typing import TypeAlias

import gymnasium as gym
import numpy as np
import numpy.typing as npt
import pandas as pd

from ..models import AgentAction

ObsType: TypeAlias = npt.NDArray[np.float32]
RewardType: TypeAlias = float | npt.NDArray[np.float64]
InfoDict: TypeAlias = dict[str, float | int | str]
ResetReturn: TypeAlias = tuple[ObsType, InfoDict]
StepReturn: TypeAlias = tuple[ObsType, RewardType, bool, bool, InfoDict]


class TradingFloorEnv(gym.Env):
    metadata = {
        "render_modes": ["human"],
        "render_fps": 60,
    }

    def __init__(
        self,
        equities: list[pd.DataFrame],
        funds: float = 10_000.,
        t0: int = 0,
        fee: float = .01,
        risk_tol: float = .05,
        is_train: bool = True,
        render_mode: str | None = None,
    ) -> None:
        super(TradingFloorEnv, self).__init__()

        self.equities = [equity for equity in equities if len(equity)]
        self.funds = funds
        self.t0 = t0
        self.fee = fee
        self.risk_tol = risk_tol
        self.is_train = is_train
        self.render_mode = render_mode

        self.action_space = gym.spaces.Discrete(4)

        self.observation_space = gym.spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(32,),
            dtype=np.float32,
        )

        self.reset()

    def reset(
        self,
        seed: int | None = None,
        options: dict[str, object] | None = None,
    ) -> ResetReturn:
        super().reset(seed=seed, options=options)

        self.equity = self.equities[random.randint(0, len(self.equities) - 1)]
        t0 = (
            random.randint(0, len(self.equity) - 3)
            if self.is_train
            else self.t0
        )
        self.equity = self.equity.iloc[t0:]

        self.action_taken = "HOLD"
        self.balance = self.funds
        self.portfolio = self.funds
        self.position = 0
        self.timestep = 0

        self.date = self.equity.index[self.timestep].strftime("%Y-%m-%d")
        self.fluctuation = self.equity["fluctuation"].iat[self.timestep]
        self.price = self.equity["price"].iat[self.timestep]

        return self._get_obs(), self._get_info()

    def step(self, action: int) -> StepReturn:
        self.timestep += 1
        self.date = self.equity.index[self.timestep].strftime("%Y-%m-%d")
        self.price = self.equity["price"].iat[self.timestep]
        self.fluctuation = self.equity["fluctuation"].iat[self.timestep]
        self.atr = self.equity["atr"].iat[self.timestep - 1]

        match action:
            case AgentAction.HOLD:
                flag = 0 if not self.position \
                    else np.where(0 < self.fluctuation < 1, 1, -1)

                self.action_taken = "HOLD"
            case AgentAction.LONG:
                size_max = self.balance // (self.price * (1 + self.fee))
                size_atr = (self.balance * self.risk_tol) // (self.atr * 2)
                size = max(min(size_max, size_atr) - self.position, 0)
                amount = self.price * size

                self.balance -= amount * (1 + self.fee)
                self.position += size

                self.action_taken = "LONG" if size else "HOLD"

                flag = 0 if not size \
                    else np.where(self.fluctuation < 0, 1, -1)
            case AgentAction.SHORT:
                size_max = self.position
                size_atr = (self.balance * self.risk_tol) // (self.atr * 2)
                size = max(self.position - min(size_max, size_atr), 0)
                amount = self.price * size

                self.balance += amount * (1 + self.fee)
                self.position -= size

                self.action_taken = "SHORT" if size else "HOLD"

                flag = 0 if not size \
                    else np.where(self.fluctuation > 0, 1, -1)
            case AgentAction.CLOSE:
                size = self.position
                amount = self.price * size

                self.balance += amount * (1 + self.fee)
                self.position -= size

                self.action_taken = "CLOSE" if size else "HOLD"

                flag = 0 if not size \
                    else np.where(self.fluctuation > 0, 1, -1)

        self.portfolio = self.balance + self.price * self.position

        reward = flag * abs(self.fluctuation) * 2

        terminated = not -.3 < self.portfolio / self.funds - 1 < .5
        truncated = self.timestep >= len(self.equity) - 1

        return self._get_obs(), reward, terminated, truncated, self._get_info()

    def render(self) -> None:
        if self.render_mode == "human":
            print(
                f"[{self.timestep:4}] {self.date} | "
                f"Price: ${self.price:6.2f} | "
                f"Action: {self.action_taken:5}, "
                f"Balance: ${self.balance:8.2f}, "
                f"Position: {self.position:3.0f} | "
                f"Portfolio: ${self.portfolio:8.2f}"
            )

    def close(self) -> None:
        pass

    def _get_obs(self) -> ObsType:
        return np.array(
            [self.balance, self.position]
            + self.equity[[
                "adx_07", "adx_14", "bbands_10_width",
                "bbands_20_width", "cci_10", "cci_20",
                "close", "crossover_06_12", "crossover_12_26",
                "macd_06_12", "macd_12_26", "obv",
                "pivot_r1", "pivot_s1", "pivot_trend_ema10",
                "pivot_trend_ema20", "return_ema05", "return_ema10",
                "return_ema20", "return", "rsi_07",
                "rsi_14", "signal_06_12", "signal_12_26",
                "ssma_03", "ssma_09", "ssma_12",
                "volatility_ema05", "volatility_ema10", "volatility_ema20",
            ]].iloc[self.timestep].to_list(),
            dtype=np.float32,
        )

    def _get_info(self) -> InfoDict:
        return {
            "action_taken": self.action_taken,
            "balance": self.balance,
            "date": self.date,
            "portfolio": self.portfolio,
            "shares": self.position,
            "timestep": self.timestep,
        }
