import numpy as np

from .algorithms import AgentA2C, AgentDQN, AgentEnsemble, AgentPPO


class AntiMPT:
    def __init__(self, algorithm, **kwargs):
        match algorithm:
            case "A2C":
                self.agent = AgentA2C(**kwargs)
            case "DQN":
                self.agent = AgentDQN(**kwargs)
            case "PPO":
                self.agent = AgentPPO(**kwargs)
            case "Ensemble":
                self.agent = AgentEnsemble(**kwargs)
            case _:
                raise ValueError(f"Invalid algorithm: {algorithm}")

    def train(self, **kwargs) -> None:
        self.agent.train(**kwargs)

    def predict(
        self,
        obs: tuple[float],
        **kwargs
    ) -> tuple[np.ndarray, tuple[np.ndarray, ...] | None]:
        return self.agent.predict(obs, **kwargs)
