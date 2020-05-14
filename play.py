import torch
from torch import device
from mujoco_py.generated import const
from mujoco_py import GlfwContext
GlfwContext(offscreen=True)



class Play:
    def __init__(self, env, agent, max_episode=4):
        self.env = env
        # self.env = gym.wrappers.Monitor(env, "./vid", video_callable=lambda episode_id: True, force=True)
        self.max_episode = max_episode
        self.agent = agent
        self.agent.load_weights()
        self.agent.set_to_eval_mode()
        self.device = device("cuda" if torch.cuda.is_available() else "cpu")

    def evaluate(self):

        for _ in range(self.max_episode):
            s = self.env.reset()
            done = False
            episode_reward = 0
            # x = input("Push any button to proceed...")
            while not done:
                action = self.agent.choose_action(s)
                s_, r, done, _ = self.env.step(action)
                episode_reward += r
                s = s_
                self.env.render(mode="human")
                self.env.viewer.cam.type = const.CAMERA_FIXED
                self.env.viewer.cam.fixedcamid = 0
                # time.sleep(0.03)
            print(f"episode reward:{episode_reward:3.3f}")
