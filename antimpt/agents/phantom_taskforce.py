from sb3_contrib import ARS, MaskablePPO, RecurrentPPO, QRDQN, TRPO

from .base import BaseAgent


class AgentARS(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(sb3=ARS, **kwargs)


class AgentMaskablePPO(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(sb3=MaskablePPO, **kwargs)


class AgentRecurrentPPO(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(sb3=RecurrentPPO, **kwargs)


class AgentQRDQN(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(sb3=QRDQN, **kwargs)


class AgentTRPO(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(sb3=TRPO, **kwargs)
