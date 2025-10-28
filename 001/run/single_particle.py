# === IMPORTS ===
# Standard library imports
import os

# Numpy (https://numpy.org/)
# and ctypes (https://docs.python.org/3/library/ctypes.html)
from ctypes import c_float,cdll

# Matplotlib (https://matplotlib.org/) 
# imports for plotting and animation
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# === CONSTANTS ===
position_velocity = [1.0,0.1]
dt    = 0.05

# === C LIBRARY LOADING ===
# Define the path to the compiled C library (.so file)
# This assumes 'libsolver.so' is in a 'solve' directory one level *up*
# from the directory containing this Python script.
__solver_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'solver/libsolver.so'))
_libsolver    = cdll.LoadLibrary(__solver_path)

# === C FUNCTION PROTOTYPING ===
# Get the functions from the loaded library
next_coordinate_1D = _libsolver.next_coordinate_1D
next_velocity_1D   = _libsolver.next_velocity_1D

# Define the argument types (argtypes) for the C functions
# This tells ctypes how to interpret the Python arguments.
# The signature is:
# (IN coord, IN vel, OUT new_(pos|vel), IN dt)
next_coordinate_1D.argtypes = [c_float,c_float,c_float]
next_velocity_1D.argtypes   = [c_float,c_float,c_float]

# Define the return types (restype) for the C functions
next_coordinate_1D.restype  = c_float
next_velocity_1D.restype    = c_float

# === PLOTTING SETUP ===
fig, ax = plt.subplots()

# Set up the figure and axes
points = ax.scatter(*position_velocity,c="b", s=57, label=f'simple')
# Set plot limits and labels
ax.set(xlim=[0, 3], ylim=[-1, 2], xlabel='position', ylabel='velocity')

# === ANIMATION FUNCTION ===
def update_frame(frame):
    """
    This function is called for each frame of the animation.
    It calculates the new state of the simulation and updates the plot.
    """
    position_velocity[0] = next_coordinate_1D(*position_velocity,dt)
    position_velocity[1] = next_velocity_1D(*position_velocity,dt)

    # --- Update Matplotlib elements ---
    # Update the positions of the scattered points
    points.set_offsets(position_velocity)

# === RUN ANIMATION ===
# Create the animation object
ani = animation.FuncAnimation(fig=fig, func=update_frame, frames=40, interval=30)
plt.show()
