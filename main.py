from lib.animate import SolveAnim


def main():
    solver_anim = SolveAnim(
        config="default",  # default    different_masses     three_body
        movie_path="outputs/default_movie.mp4"
    )
    solution = solver_anim.solve()
    solver_anim.animation()
    return solution


if __name__ == "__main__":
    main()
