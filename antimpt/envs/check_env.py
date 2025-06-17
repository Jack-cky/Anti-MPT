import gymnasium as gym
from gymnasium.utils.env_checker import check_env

from ..utils import get_equities


def main() -> None:
    gym.register(id="TradingFloor-v0", entry_point="antimpt:TradingFloorEnv")

    equity = get_equities(2025, 2025, "WSM")[0]
    env = gym.make("TradingFloor-v0", equities=[equity], is_train=False)

    check_env(env.unwrapped)


if __name__ == "__main__":
    main()
