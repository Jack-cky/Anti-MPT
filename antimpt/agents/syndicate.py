import random
import statistics

import numpy as np

# from .phantom_taskforce import AgentARS, AgentMaskablePPO, AgentRecurrentPPO, \
#     AgentQRDQN, AgentTRPO
from .shadow_operatives import AgentA2C, AgentDQN, AgentHER, AgentPPO


class AgentEnsemble:
    def __init__(self, **kwargs):
        self.agents = [
            AgentA2C(artefact=["A2C", "01", "1_000_000"]),
            # AgentDQN(artefact=["DQN", "00", "10_000"]),
            # AgentHER(artefact=["HER", "00", "10_000"]),
            AgentPPO(artefact=["PPO", "00", "7_000_000"]),
            # AgentARS(artefact=["ARS", "00", "10_000"]),
            # AgentMaskablePPO(artefact=["MaskablePPO", "00", "10_000"]),
            # AgentRecurrentPPO(artefact=["RecurrentPPO", "00", "10_000"]),
            # AgentQRDQN(artefact=["QRDQN", "00", "10_000"]),
            # AgentTRPO(artefact=["TRPO", "00", "10_000"]),
        ]

    def predict(self, obs: tuple[float], **kwargs) -> tuple[int, None]:
        actions = [agent.predict(obs, **kwargs)[0][0] for agent in self.agents]
        modes = statistics.multimode(actions)
        action = random.choice(modes)

        return np.array([action]), None
