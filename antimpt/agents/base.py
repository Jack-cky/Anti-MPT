from pathlib import Path

from .mission import setup_mission


class BaseAgent:
    def __init__(self, sb3, **kwargs):
        if kwargs.get("artefact"):
            self.model = sb3.load(Path(
                "antimpt", "models",
                *kwargs["artefact"],
            ))
        else:
            self.algo_expt, policy = setup_mission(sb3.__name__, **kwargs)

            self.model = sb3(
                policy,
                tensorboard_log=Path("antimpt", "logs"),
                verbose=1,
                seed=42,
                **kwargs,
            )

    def train(self, iters: int=1, steps: int=10_000) -> None:
        for iter_ in range(1, iters+1):
            self.model.learn(
                total_timesteps=steps,
                reset_num_timesteps=False,
                tb_log_name=Path(*self.algo_expt),
            )

            self.model.save(Path(
                "antimpt", "models",
                *self.algo_expt, f"{iter_*steps:_}",
            ))

    def predict(
        self,
        obs: tuple[float],
        **kwargs
    ) -> tuple[int, tuple[float]|None]:
        return self.model.predict(obs, deterministic=True, **kwargs)
