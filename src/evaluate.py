import argparse
from pathlib import Path

from antimpt import AntiMPT
from antimpt.utils import get_equities, take_positions, visualise_returns


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluation Script for Anit-MPT.",
    )

    parser.add_argument(
        "algorithm",
        type=str,
        choices=[
            "A2C", "DQN", "HER", "PPO",
            "ARS", "MaskablePPO", "RecurrentPPO", "QRDQN", "TRPO",
            "Ensemble",
        ],
        help="RL algorithm that supports discrete actions.",
    )

    parser.add_argument(
        "experiment",
        type=str,
        help="Experiment index of the corresponding agent.",
    )

    parser.add_argument(
        "snapshot",
        type=str,
        help="Snapshot index of the experiment index.",
    )

    parser.add_argument(
        "--yr-from",
        type=int,
        default=2021,
        choices=range(2021, 2047),
        help="Start year of the backtesting data (inclusive).",
    )

    parser.add_argument(
        "--yr-to",
        type=int,
        default=2024,
        choices=range(2021, 2047),
        help="End year of the backtesting data (inclusive).",
    )

    parser.add_argument(
        "--funds",
        type=float,
        default=10_000.,
        help="Initial fund amount to invest.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    snapshots = [args.snapshot] if args.snapshot != "-1" else [
        file.stem
        for file in Path("antimpt", "models", args.algorithm, args.experiment) \
        .glob("*.zip")
    ]

    for snapshot in snapshots:
        artefact = [args.algorithm, args.experiment, snapshot]

        agent = AntiMPT(args.algorithm, artefact=artefact)

        equity = get_equities(args.yr_from, args.yr_to, "WSM")[0]
        histories = take_positions(agent, equity, args.funds)

        visualise_returns(equity, histories, artefact)


if __name__ == "__main__":
    main()
