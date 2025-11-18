# === IMPORTS ===
# Standard library imports
import os
from sys import argv

# Third party imports
import numpy as np

# Local imports
import cprototype as cp
import animation as anim
from ccompiler import CSharedLibraryCompiler

# === CONSTANTS ===
if len(argv) > 1:
    try:
        NUMBER_OF_PARTICLES = int(argv[1]) # Number of particles read from command line
    except ValueError as e:
        print(e)
        NUMBER_OF_PARTICLES = np.random.randint(1,23)
        print(f"Number of particles is now set to randomly chosen: {NUMBER_OF_PARTICLES}")
else:
    NUMBER_OF_PARTICLES = 1      # Number of particles in the simulation
RADIUS              = 2.0    # Initial radius for particle placement
dt                  = 0.01   # Timestep for the simulation

# === C LIBRARY LOADING ===
# Define the path to the compiled C library (.so file)
# This assumes 'libsolver.so' is in a 'solve' directory one level *up*
# from the directory containing this Python script.
ccompiler = CSharedLibraryCompiler(source_file="../solver/solver.c")
__solver_path = ccompiler.compile()
_libsolver    = cp.EOMSolver(__solver_path, NUMBER_OF_PARTICLES, DIMENSIONS=2)

# +== INITIAL CONDITIONS ===
positions = [_libsolver.vector(x=RADIUS * np.cos(2 * np.pi * i / NUMBER_OF_PARTICLES),
                               y=RADIUS * np.sin(2 * np.pi * i / NUMBER_OF_PARTICLES))
             for i in range(NUMBER_OF_PARTICLES)]
velocities = [_libsolver.vector(x=0, y=0) for i in range(NUMBER_OF_PARTICLES)]

# === PLOTTING SETUP ===
ani = anim.Animation2D(vector_factory=_libsolver.vector,
                       c_arr=_libsolver.c_arr,
                       next_step=_libsolver.next_step,
                       positions=positions,
                       velocities=velocities,
                       dt=dt,
                       NUMBER_OF_PARTICLES=NUMBER_OF_PARTICLES)
ani.create_canvas()

# === RUN ANIMATION ===
ani.run_animation()
