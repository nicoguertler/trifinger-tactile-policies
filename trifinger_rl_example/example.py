"""Example policy for Real Robot Challenge 2022"""
import numpy as np
import torch

from trifinger_rl_datasets import PolicyBase, PolicyConfig

from . import policies


class TorchBasePolicy(PolicyBase):

    _goal_order = ["object_keypoints", "object_position", "object_orientation"] 

    def __init__(
        self,
        torch_model_path,
        action_space,
        observation_space,
        episode_length,
    ):
        self.action_space = action_space
        self.device = "cpu"
        self.dtype = np.float32

        # load torch script
        self.policy = torch.jit.load(
            torch_model_path, map_location=torch.device(self.device)
        )

    @staticmethod
    def get_policy_config():
        return PolicyConfig(
            flatten_obs=True,
            image_obs=False,
        )

    def reset(self):
        pass  # nothing to do here

    def get_action(self, observation):
        observation = torch.tensor(observation, dtype=torch.float, device=self.device)
        action = self.policy(observation.unsqueeze(0))
        action = action.detach().numpy()[0]
        action = np.clip(action, self.action_space.low, self.action_space.high)
        return action


class TorchPushPolicy(TorchBasePolicy):
    """Example policy for the push task, using a torch model to provide actions.

    Expects flattened observations.
    """

    def __init__(self, action_space, observation_space, episode_length):
        model = policies.get_model_path("push.pt")
        super().__init__(model, action_space, observation_space, episode_length)


class TorchLiftPolicy(TorchBasePolicy):
    """Example policy for the lift task, using a torch model to provide actions.

    Expects flattened observations.
    """

    def __init__(self, action_space, observation_space, episode_length):
        model = policies.get_model_path("lift.pt")
        super().__init__(model, action_space, observation_space, episode_length)

class CRRTorchLiftPolicy(TorchBasePolicy):
    """CRR policy for the lift task, using a torch model to provide actions.

    Expects flattened observations.
    """

    def __init__(self, action_space, observation_space, episode_length):
        model = policies.get_model_path("/userhome/crr_old_data.pt")
        super().__init__(model, action_space, observation_space, episode_length)
