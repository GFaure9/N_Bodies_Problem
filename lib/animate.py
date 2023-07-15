import pyvista as pv
import numpy as np
from colour import Color
from lib.utils import logger
from tqdm import tqdm


from lib.vectors import Solve


class SolveAnim(Solve):
    """
    Main class to animate the solution of the N-body problem.
    """
    def __init__(self, movie_path: str = "outputs/test.mp4", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pth = movie_path

    def animation(self):
        """
        Create a movie of the N bodies movement from the resolution of positions/velocities.
        The movie is saved at self.pth.
        :return: None
        """
        log.info("Starting creating a movie to visualize solution...")

        if self.ys is not None:
            ys = self.ys
        else:
            log.error("You must solve the problem first with SolveAnim.solve()")

        n = int(len(ys[0])/2)
        rs = [y[:n] for y in ys]

        p = pv.Plotter(off_screen=True)
        # Open a movie file
        p.open_movie(self.pth)

        # Add initial mesh
        m_p = self.m_vec / np.max(self.m_vec)
        green = Color("blue")
        red = Color("magenta")
        colors = list(green.range_to(red, n))
        # colors = [Color("yellow"), Color("yellow"), Color("yellow"), Color("blue")]
        planets = [pv.Sphere(radius=0.04 * m_p[j], center=rs[0][j]) for j in range(n)]
        for i, planet in enumerate(planets):
            p.add_mesh(planet, color=colors[i].rgb)

        p.camera.zoom(0.7)
        p.set_background("white")

        # Run through each frame
        p.write_frame()  # write initial data

        # Update scalars on each frame
        rg = range(1, len(rs), 100)
        progress_bar = tqdm(rg, desc="Processing", unit="steps")
        for t, stp in zip(rg, progress_bar):
            for j, planet in enumerate(planets):
                planet.translate(xyz=rs[t][j] - np.array(planet.center), inplace=True)
            p.write_frame()  # Write this frame
            progress_bar.set_description(f"Writing frame: {stp}")
        progress_bar.close()

        # Be sure to close the plotter when finished
        p.close()

        log.info(f"Finished creating movie! Movie created at: {self.pth}")


log = logger

if __name__ == "__main__":
    anim = SolveAnim()
    anim.animation()
