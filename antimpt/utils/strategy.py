import pandas as pd

from ..agents.antimpt import AntiMPT
from .environment import create_envs


def take_positions(
    agent: AntiMPT,
    equity: pd.DataFrame,
    funds_init: float=10_000,
    render_mode: str="human",
) -> list[dict[str, bool|float|int|str]]:
    funds = funds_init
    histories = [{
        "date": equity.index[0].strftime("%Y-%m-%d"),
        "action_taken": "HOLD",
        "portfolio": funds,
    }]

    t0 = 0
    while t0 < len(equity)-1:
        env = create_envs(
            [equity],
            funds=funds,
            t0=t0,
            is_train=False,
            render_mode=render_mode,
        )
        obs = env.reset()
        env.render()

        done = False
        while not done:
            action, _ = agent.predict(obs)
            obs, _, done, info = env.step(action)
            env.render() if not done else None

            histories.append(info[0])

        t0 += info[0]["timestep"] + 15 - 1
        funds += (info[0]["portfolio"] - funds) * .9

    return histories
