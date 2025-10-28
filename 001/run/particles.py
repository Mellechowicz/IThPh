# === IMPORTS ===
# Standard library imports
import os
import itertools as it
from sys import argv

# Numpy (https://numpy.org/)
# and ctypes (https://docs.python.org/3/library/ctypes.html)
import numpy as np 
from ctypes import c_float, Structure, POINTER, byref, cdll

# Matplotlib (https://matplotlib.org/) 
# imports for plotting and animation
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation

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

# === CTYPES STRUCTURE DEFINITION ===
class Vector2D(Structure):
    """
    A ctypes Structure to represent a 2D vector, allowing it
    to be passed to and from the C library.
    """
    _fields_ = [("x", c_float),
                ("y", c_float)]

    def __repr__(self):
        """String representation for debugging."""
        return f"({self.x:.4f}, {self.y:.4f})"

    def __call__(self, data, i):
        """
        A helper method to update a numpy array (for plotting)
        with this vector's data at a specific index 'i'.
        """
        data[i, :] = np.array((self.x, self.y))

# === C LIBRARY LOADING ===
# Define the path to the compiled C library (.so file)
# This assumes 'libsolver.so' is in a 'solve' directory one level *up*
# from the directory containing this Python script.
__solver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'solver/libsolver.so'))
_libsolver    = cdll.LoadLibrary(__solver_path)

# === C FUNCTION PROTOTYPING ===
# Get the functions from the loaded library
next_coordinate_2D = _libsolver.next_coordinate_2D
next_velocity_2D   = _libsolver.next_velocity_2D

# Define the argument types (argtypes) for the C functions
# This tells ctypes how to interpret the Python arguments.
# The signature is:
# (IN coord, IN vel, OUT new_(pos|vel), IN dt)
c_vec_ptr = POINTER(Vector2D)  # Alias for pointer to Vector2D
next_coordinate_2D.argtypes = [c_vec_ptr, c_vec_ptr, c_vec_ptr, c_float]
next_velocity_2D.argtypes   = [c_vec_ptr, c_vec_ptr, c_vec_ptr, c_float]

# Define the return types (restype) for the C functions
# 'None' corresponds to a 'void' return type in C.
next_coordinate_2D.restype = None
next_velocity_2D.restype   = None

# === SIMULATION INITIALIZATION ===
# Create the initial list of particle positions
# They are placed in a circle of the given RADIUS.
positions = [Vector2D(x=RADIUS * np.cos(2 * np.pi * i / NUMBER_OF_PARTICLES),
                      y=RADIUS * np.sin(2 * np.pi * i / NUMBER_OF_PARTICLES))
             for i in range(NUMBER_OF_PARTICLES)]

# Create the initial list of particle velocities (all start at rest)
velocities = [Vector2D(x=0, y=0) for i in range(NUMBER_OF_PARTICLES)]

# === PLOTTING SETUP ===
# 'data' is a NumPy array that will be updated each frame
# and used by Matplotlib for efficient plotting.
data = np.zeros((NUMBER_OF_PARTICLES, 2))
for i, pos in enumerate(positions):
    pos(data, i)  # Initialize 'data' with starting positions

# Create an iterator for particle colors
colours = it.cycle(mcolors.TABLEAU_COLORS)

# Set up the figure and axes
fig, ax = plt.subplots()
ax.set_aspect('equal', adjustable='box')  # Ensure x and y axes have the same scale

# Set plot limits and labels
ax.set(xlim=[-2.1, 2.1], ylim=[-2.1, 2.1], xlabel='x', ylabel='y')

# Create the plot elements that will be animated
# 'lines' will connect the particles (if more than 1)
if NUMBER_OF_PARTICLES > 1:
    lines = ax.plot(np.append(data[:, 0], data[0, 0]),  # Append first point to close the loop
                    np.append(data[:, 1], data[0, 1]), lw=1)[0]
# 'points' is a scatter plot of the particles themselves
points = ax.scatter(data[:, 0], data[:, 1],
                    c=[clr for clr, _ in zip(colours, range(NUMBER_OF_PARTICLES))], s=57)

# === ANIMATION FUNCTION ===
def update_frame(frame):
    """
    This function is called for each frame of the animation.
    It calculates the new state of the simulation and updates the plot.
    """
    for i, _position in enumerate(positions):
        # Get the current state for particle 'i'
        _velocity = velocities[i]
        
        # Create empty Vector2D objects to hold the C function results
        new_position = Vector2D(x=0, y=0)
        new_velocity = Vector2D(x=0, y=0)

        # --- RECTIFIED LOGIC ---
        
        # 1. Calculate the new position
        #    C signature: next_coordinate_2D(IN pos, IN vel, OUT new_pos, IN dt)
        next_coordinate_2D(byref(_position), byref(_velocity), byref(new_position), dt)
        
        # 2. Calculate the new velocity
        #    C signature: next_velocity_2D(IN new_pos, IN old_vel, OUT new_vel, IN dt)
        next_velocity_2D(byref(new_position), byref(_velocity), byref(new_velocity), dt)

        # 3. Update the master Python lists with the new state
        positions[i]  = new_position
        velocities[i] = new_velocity
        
        # 4. Update the NumPy plotting array
        new_position(data, i)

    # --- Update Matplotlib elements ---
    # Update the positions of the scattered points
    points.set_offsets(data)
    
    # Update the connecting lines (if they exist)
    if NUMBER_OF_PARTICLES > 1:
        lines.set_xdata(np.append(data[:, 0], data[0, 0]))
        lines.set_ydata(np.append(data[:, 1], data[0, 1]))

# === RUN ANIMATION ===
# Create the animation object
ani = animation.FuncAnimation(fig=fig, func=update_frame, frames=60, interval=30)
plt.show()
