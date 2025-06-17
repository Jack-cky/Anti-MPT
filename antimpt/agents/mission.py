from collections import defaultdict
from pathlib import Path

import yaml


def get_mission_index(algorithm: str) -> str:
    Path("antimpt", "logs", algorithm).mkdir(exist_ok=True)

    index = sum(
        subdir.is_dir()
        for subdir in Path("antimpt", "logs", algorithm).iterdir()
    )

    return f"{index:02}"


def create_artefact_folders(algorithm: str, mission: str) -> None:
    Path("antimpt", "logs", algorithm, f"{mission}_0") \
        .mkdir(parents=True, exist_ok=True)

    Path("antimpt", "models", algorithm, mission) \
        .mkdir(parents=True, exist_ok=True)


def flatten_arguments(**kwargs) -> dict:
    args = defaultdict(dict)

    for k, v in kwargs.items():
        if isinstance(v, dict):
            for sub_k, sub_v in v.items():
                args[f"{k}"][f"{sub_k}"] = sub_v
        else:
            args[k] = str(v)

    return dict(args)


def get_policy(algorithm: str) -> str:
    return {
        "A2C": "MlpPolicy",
        "DQN": "MlpPolicy",
        "PPO": "MlpPolicy",
        "QRDQN": "MlpPolicy",
        "TRPO": "MlpPolicy",
        "ARS": "LinearPolicy",
        "RecurrentPPO": "MlpLstmPolicy",
    }.get(algorithm, "MlpPolicy")


def save_argments(args: dict) -> None:
    pth = Path(
        "antimpt", "logs",
        args["algorithm"], f"{args['mission']}_0",
        "args.yaml"
    )

    with open(pth, "w", encoding="utf-8") as file:
        yaml.dump(args, file)


def setup_mission(algorithm: str, **kwargs) -> str:
    mission = get_mission_index(algorithm)
    create_artefact_folders(algorithm, mission)

    args = flatten_arguments(**kwargs)
    save_argments({
        **dict(args),
        "algorithm": algorithm,
        "env": {
            "wrapper": [
                kwargs["env"].__class__.__name__,
                kwargs["env"].unwrapped.__class__.__name__,
            ],
            "n_envs": kwargs["env"].num_envs,
        },
        "mission": mission,
        "policy": (policy:=get_policy(algorithm)),
    })

    return [algorithm, mission], policy
