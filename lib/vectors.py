import yaml
import numpy as np

from tqdm import tqdm
from lib.utils import logger


class Solve:
    def __init__(self, config: str = "default"):
        with open("data/config.yaml", 'r') as file:
            cfgs = yaml.safe_load(file)
        self.cfg = cfgs[config]
        self.m_vec = np.ones((self.cfg["N"], 1)) * self.cfg["m"]
        self.ys = None  # solutions (positions at each time step)

    def y_0(self, method: str):
        N = self.cfg["N"]
        if method == "random":
            return np.row_stack((np.random.random((N, 3)), np.zeros((N, 3))))
        log.info("Finished initialization of positions and velocities !")

    def f(self, i, r: np.ndarray):
        mm = np.delete(self.m_vec, i, 0)
        rr = np.delete(r, i, 0)
        rr -= r[i]
        divide = np.linalg.norm(rr, axis=1) ** 2
        divide = np.array([divide.tolist()]).transpose()
        to_sum = self.cfg["G"] * mm * rr / divide
        return np.sum(to_sum, axis=0)

    def f_vec(self, y: np.ndarray):
        n = int(len(y)/2)
        r = y[:n]
        ff = np.array([self.f(i, r) for i in range(n)])
        return ff

    def g(self, y: np.ndarray) -> np.ndarray:
        n = int(len(y)/2)
        return np.row_stack((y[n:], self.f_vec(y)))

    def y_k1(self, y_k0: np.ndarray, method: str) -> np.ndarray:
        if method == "euler":
            return y_k0 + self.cfg["dt"] * self.g(y_k0)

    def solve(self):
        log.info(f"The configuration for this resolution is: {self.cfg}")

        init, solv = self.cfg["init_method"], self.cfg["solve_method"]
        T, dt = self.cfg["T"], self.cfg["dt"]

        y = [self.y_0(method=init)]

        log.info(f"Starting resolution with {solv} method...")

        rg = range(1, int(T/dt))
        progress_bar = tqdm(rg, desc="Processing", unit="steps")
        for i, stp in zip(rg, progress_bar):
            y.append(self.y_k1(y[i - 1], solv))
            progress_bar.set_description(f"Computing solution (step): {stp}")
        progress_bar.close()

        self.ys = y
        log.info("Finished initialization of positions and velocities !")

        return y


log = logger

if __name__ == "__main__":
    pb_solve = Solve("default")
    breakpoint()





