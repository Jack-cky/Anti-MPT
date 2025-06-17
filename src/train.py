import argparse

from antimpt import AntiMPT
from antimpt.utils import get_equities, create_envs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Training Script for Anit-MPT.",
    )

    parser.add_argument(
        "algorithm",
        type=str,
        choices=[
            "A2C", "DQN", "HER", "PPO",
            "ARS", "MaskablePPO", "RecurrentPPO", "QRDQN", "TRPO",
        ],
        help="RL algorithm that supports discrete actions.",
    )

    parser.add_argument(
        "--yr-from",
        type=int,
        default=2010,
        choices=range(2010, 2020),
        help="Start year of the training data (inclusive)."
    )

    parser.add_argument(
        "--yr-to",
        type=int,
        default=2020,
        choices=range(2020, 2047),
        help="End year of the training data (inclusive).",
    )

    parser.add_argument(
        "--n-envs",
        type=int,
        default=3,
        help="Number of virtual environments.",
    )

    parser.add_argument(
        "--iters",
        type=int,
        default=100,
        help="Number of training iterations.",
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=1_000_000,
        help="Number of timesteps per iteration.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    equities = get_equities(args.yr_from, args.yr_to)
    env = create_envs(equities, n_envs=args.n_envs)

    agent = AntiMPT(args.algorithm, env=env)
    agent.train(iters=args.iters, steps=args.steps)


if __name__ == "__main__":
    main()
