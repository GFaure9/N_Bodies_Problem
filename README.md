# N-Body Problem Solver

This project aims to solve an N-body problem, where given masses are subjected to gravitational force 
(see [Wikipedia page](https://en.wikipedia.org/wiki/N-body_problem) for more information on the problem). 
The method used to solve such a problem can be found in the chapter 4 of Kjartan Kari Gardasson Myrdal's
[Bachelor Thesis](https://lup.lub.lu.se/luur/download?func=downloadFile&recordOId=4780668&fileOId=4780676)
__Some Theoretical and Numerical Aspects of the N-Body Problem__ (2013).

*"No, emptiness is not nothingness. Emptiness is a form of existence. You must utilize this existential emptiness to fill yourself."*  
- The Three-Body Problem, Liu Cixin

<p align="center">
  <img src=docs/image_book.jpg alt="Image" width="200" height="300">
</p>

Further description of the equations and the resolution method can be found at [docs/N_bodies_problem.pdf](docs/N_bodies_problem.pdf).

## Demo
Click the image below to download a demonstration of the project:

<p align="center">
<a href=outputs/default_movie.mp4>
  <img src=docs/image_demo.png alt="Thumbnail" style="max-width: 300px;">
</a>
</p>

## Installation
To install this project, clone the repository using the following command:
```batch
git clone https://github.com/GFaure9/N_Bodies_Problem.git
```
Navigate to the project directory in a terminal (`cd path_to_project`) and run the following command to install the required dependencies:
```batch
pip install -r requirements.txt
```

## Usage

To use the library, first create the configuration you want by writing it in the [data/config.yaml](data/config.yaml)
file or check for already existing configurations.
```
# Example of a configuration

three_body:
  N : 4
  dt : 0.1
  T : 10000
  m:
    - [100000]
    - [100000]
    - [100000]
    - [50000]
  G : 6.67428e-11
  init_method: "random"
  solve_method: "euler"
```

Then in a Python file, run the following commands:
```python
from lib.animate import SolveAnim

solver_anim = SolveAnim(config="name_of_your_config", movie_path="path_for_the_output_movie")
solution = solver_anim.solve()
solver_anim.animation()
```
The output movie will be created at the path you gave in argument.
