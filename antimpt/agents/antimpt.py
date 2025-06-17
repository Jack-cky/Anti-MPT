# from .phantom_taskforce import AgentARS, AgentMaskablePPO, AgentRecurrentPPO, \
#     AgentQRDQN, AgentTRPO
from .shadow_operatives import AgentA2C, AgentDQN, AgentHER, AgentPPO
from .syndicate import AgentEnsemble


class AntiMPT:
    def __init__(self, algorithm, **kwargs):
        if algorithm == "A2C":
            self.agent = AgentA2C(**kwargs)
        elif algorithm == "DQN":
            self.agent = AgentDQN(**kwargs)
        # elif algorithm == "HER":
        #     self.agent = AgentHER(**kwargs)
        elif algorithm == "PPO":
            self.agent = AgentPPO(**kwargs)
        # elif algorithm == "ARS":
        #     self.agent = AgentARS(**kwargs)
        # elif algorithm == "MaskablePPO":
        #     self.agent = AgentMaskablePPO(**kwargs)
        # elif algorithm == "RecurrentPPO":
        #     self.agent = AgentRecurrentPPO(**kwargs)
        # elif algorithm == "QRDQN":
        #     self.agent = AgentQRDQN(**kwargs)
        # elif algorithm == "TRPO":
        #     self.agent = AgentTRPO(**kwargs)
        elif algorithm == "Ensemble":
            self.agent = AgentEnsemble(**kwargs)
        else:
            raise ValueError("Invalid algorithm.")

    def train(self, **kwargs) -> None:
        self.agent.train(**kwargs)

    def predict(
        self,
        obs: tuple[float],
        **kwargs
    ) -> tuple[int, tuple[float]|None]:
        return self.agent.predict(obs, **kwargs)
