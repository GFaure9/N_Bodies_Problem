import yaml
import numpy as np

from typing import List
from tqdm import tqdm
from lib.utils import logger


class Solve:
    """
    Main class to solve the N-body problem.
    """
    def __init__(self, config: str = "default"):
        with open("data/config.yaml", 'r') as file:
            cfgs = yaml.safe_load(file)
        self.cfg = cfgs[config]
        self.m_vec = np.ones((self.cfg["N"], 1)) * self.cfg["m"]
        self.ys = None  # solutions (positions at each time step)

    def y_0(self, method: str) -> np.ndarray:
        """
        Initialize the solution of the problem. With N positions and N velocities.
        For the "random" method, the positions are chosen randomly in the unit cube, and
        the velocities are all set to 0.
        :param method: str : name of the method of initialization.
        :return: np.ndarray : a vector containing initial positions and velocities.
        """
        N = self.cfg["N"]
        if method == "random":
            init_vec = np.row_stack((np.random.random((N, 3)), np.zeros((N, 3))))
            log.info("Finished initialization of positions and velocities!")
            return init_vec

    def f(self, i: int, r: np.ndarray):
        """
        Compute the function:
        f_i = sum{j=1 to N with j != i}( G * m_j * (r_j - r_i)/|r_j - r_i| ** 2 )
        :param i: int : number of the body.
        :param r: np.ndarray : positions of the N bodies.
        :return: float : f_i.
        """
        mm = np.delete(self.m_vec, i, 0)
        rr = np.delete(r, i, 0)
        rr -= r[i]
        divide = np.linalg.norm(rr, axis=1) ** 2
        divide = np.array([divide.tolist()]).transpose()
        to_sum = self.cfg["G"] * mm * rr / divide
        return np.sum(to_sum, axis=0)

    def f_vec(self, y: np.ndarray) -> np.ndarray:
        """
        Return the vector made of all f_i.
        :param y: np.ndarray : (positions, velocities) array.
        :return: np.ndarray : (f_1, f_2, ..., f_N).
        """
        n = int(len(y)/2)
        r = y[:n]
        ff = np.array([self.f(i, r) for i in range(n)])
        return ff

    def g(self, y: np.ndarray) -> np.ndarray:
        """
        Return g = (positions, f_vec)
        :param y: np.ndarray : (positions, velocities) array.
        :return: np.ndarray : g.
        """
        n = int(len(y)/2)
        return np.row_stack((y[n:], self.f_vec(y)))

    def y_k1(self, y_k0: np.ndarray, method: str) -> np.ndarray:
        """
        Compute and return y_k1 = h(y_k0) (update of the positions/velocities array) at
        time step k+1 using solution at time step k.
        :param y_k0: np.ndarray : (positions, velocities) at time step k.
        :param method: str : name of method of update ("euler" = Euler's explicit method
        for instance).
        :return:
        """
        if method == "euler":
            return y_k0 + self.cfg["dt"] * self.g(y_k0)

    def solve(self) -> List[np.ndarray]:
        """
        Run the resolution of the N-body problem.
        :return: List[np.ndarray] : y the list of solutions at each time step.
        """
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
        log.info("Finished resolution!")

        return y


log = logger

if __name__ == "__main__":
    pb_solve = Solve("default")
    breakpoint()





