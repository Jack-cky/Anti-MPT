from collections import defaultdict
from pathlib import Path

import yaml


def _create_artefacts(algorithm: str) -> str:
    pth = Path("logs", algorithm)
    pth.mkdir(parents=True, exist_ok=True)
    expt = f"{sum(subdir.is_dir() for subdir in pth.iterdir()):02}"

    Path("logs", algorithm, f"{expt}_0").mkdir(parents=True, exist_ok=True)
    Path("checkpoints", algorithm, expt).mkdir(parents=True, exist_ok=True)

    return expt


def _flatten_arguments(**kwargs) -> dict:
    args = defaultdict(dict)

    for k, v in kwargs.items():
        if isinstance(v, dict):
            for sub_k, sub_v in v.items():
                args[f"{k}"][f"{sub_k}"] = sub_v
        else:
            args[k] = str(v)

    return dict(args)


def _get_policy(algorithm: str) -> str:
    return {
        "ARS": "LinearPolicy",
        "RecurrentPPO": "MlpLstmPolicy",
    }.get(algorithm, "MlpPolicy")


def _save_argments(args: dict) -> None:
    with open(
        Path("logs", args["algorithm"], f"{args['experiment']}_0", "args.yaml"),
        "w",
        encoding="utf-8",
    ) as file:
        yaml.dump(args, file)


def setup_experiment(algorithm: str, **kwargs) -> tuple[list[str], str]:
    args = _flatten_arguments(**kwargs)
    experiment = _create_artefacts(algorithm)
    policy = _get_policy(algorithm)

    _save_argments({
        **dict(args),
        "algorithm": algorithm,
        "env": {
            "wrapper": [
                kwargs["env"].__class__.__name__,
                kwargs["env"].unwrapped.__class__.__name__,
            ],
            "n_envs": kwargs["env"].num_envs,
        },
        "experiment": experiment,
        "policy": policy,
    })

    return [algorithm, experiment], policy
