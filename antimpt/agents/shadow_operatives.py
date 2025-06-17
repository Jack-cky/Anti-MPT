from stable_baselines3 import A2C, DQN, HerReplayBuffer, PPO
from stable_baselines3.common.sb2_compat.rmsprop_tf_like import RMSpropTFLike

from .base import BaseAgent


class AgentA2C(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            sb3=A2C,
            device="cpu",
            policy_kwargs={
                "optimizer_class": RMSpropTFLike,
                "optimizer_kwargs": {
                    "eps": 1e-5,
                },
            },
            **kwargs,
        )


class AgentDQN(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            sb3=DQN,
            device="cuda",
            **kwargs,
        )


class AgentHER(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            sb3=DQN,
            replay_buffer_class=HerReplayBuffer,
            replay_buffer_kwargs={
                "n_sampled_goal": 4,
                "goal_selection_strategy": "future",
            },
            device="cuda",
            **kwargs,
        )


class AgentPPO(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            sb3=PPO,
            device="cpu",
            # learning_rate=3e-3,
            # gamma=0.9,
            # gae_lambda=0.9,
            # ent_coef=0.01,
            # policy_kwargs={
            #     "net_arch": {
            #         "pi": [256, 256],
            #         "vf": [256, 256],
            #     },
            # },
            **kwargs,
        )
