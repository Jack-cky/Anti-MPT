import pandas as pd
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv, VecNormalize

from ..envs.trading_floor import TradingFloorEnv


def create_envs(
    equities: list[pd.DataFrame],
    n_envs: int=1,
    funds: float=10_000.,
    t0: int=0,
    is_train: bool=True,
    render_mode: str="human",
    seed: int=42,
) -> VecNormalize:
    vec_env = make_vec_env(
        TradingFloorEnv,
        n_envs=n_envs,
        env_kwargs={
            "equities": equities,
            "funds": funds,
            "t0": t0,
            "is_train": is_train,
            "render_mode": render_mode,
        },
        # vec_env_cls=SubprocVecEnv,
        seed=seed,
    )

    return VecNormalize(vec_env, norm_obs=True, norm_reward=True)
