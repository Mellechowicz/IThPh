# === IMPORTS ===
# Standard library imports
import os
import itertools as it
from sys import argv

# Numpy (https://numpy.org/)
# and ctypes (https://docs.python.org/3/library/ctypes.html)
import numpy as np 
from ctypes import c_float, c_int, Structure, POINTER, byref, cdll

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

class Vector3D(Structure):
    """
    A ctypes Structure to represent a 3D vector, allowing it
    to be passed to and from the C library.
    """
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("z", c_float)]

    def __repr__(self):
        """String representation for debugging."""
        return f"({self.x:.4f}, {self.y:.4f}), {self.z:.4f})"

    def __call__(self, data, i):
        """
        A helper method to update a numpy array (for plotting)
        with this vector's data at a specific index 'i'.
        """
        data[i, :] = np.array((self.x, self.y, self.z))

# === C LIBRARY LOADING ===
# Define the path to the compiled C library (.so file)
# This assumes 'libsolver.so' is in a 'solve' directory one level *up*
# from the directory containing this Python script.
__solver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'solver/libsolver.so'))
_libsolver    = cdll.LoadLibrary(__solver_path)

# === C FUNCTION PROTOTYPING ===
# Get the functions from the loaded library
#void next_1D(float* coord, float* vel, float* new_coord, float* new_vel, float dt, unsigned int N){
next_1D = _libsolver.next_1D
next_2D = _libsolver.next_2D
next_3D = _libsolver.next_3D

# Define the argument types (argtypes) for the C functions
# This tells ctypes how to interpret the Python arguments.
# The signature is:
# (IN coord, IN vel, OUT new_(pos|vel), IN dt)
c_vec1D_ptr = POINTER(c_float)  # Alias for pointer to Vector1D
c_vec2D_ptr = POINTER(Vector2D) # Alias for pointer to Vector2D
c_vec3D_ptr = POINTER(Vector3D) # Alias for pointer to Vector3D

next_1D.argtypes = [c_vec1D_ptr, c_vec1D_ptr, c_vec1D_ptr, c_vec1D_ptr, c_float, c_int]
next_2D.argtypes = [c_vec2D_ptr, c_vec2D_ptr, c_vec2D_ptr, c_vec2D_ptr, c_float, c_int]
next_3D.argtypes = [c_vec3D_ptr, c_vec3D_ptr, c_vec3D_ptr, c_vec3D_ptr, c_float, c_int]

c_vec1D_arr = c_float *NUMBER_OF_PARTICLES # Alias for pointer to an array of Vector1D
c_vec2D_arr = Vector2D*NUMBER_OF_PARTICLES # Alias for pointer to an array of Vector2D
c_vec3D_arr = Vector3D*NUMBER_OF_PARTICLES # Alias for pointer to an array of Vector3D

# Define the return types (restype) for the C functions
# 'None' corresponds to a 'void' return type in C.
next_1D.restype = None
next_2D.restype = None
next_3D.restype = None

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
    global positions,velocities

    # Create empty Vector2D objects to hold the C function results
    new_positions = [Vector2D(x=0, y=0) for i in range(NUMBER_OF_PARTICLES)]
    new_velocities= [Vector2D(x=0, y=0) for i in range(NUMBER_OF_PARTICLES)]

    c_positions       = c_vec2D_arr(*positions)
    c_velocities      = c_vec2D_arr(*velocities)
    c_new_positions   = c_vec2D_arr(*new_positions)
    c_new_velocities  = c_vec2D_arr(*new_velocities)

    # 1. Calculate the new positions and velocities
    #    C signature: next_coordinate_2D(IN pos, IN vel, OUT new_pos, OUT new_vel, IN dt, IN NUMBER_OF_PARTICLES)
    next_2D(c_positions,
            c_velocities,
            c_new_positions,
            c_new_velocities, dt, NUMBER_OF_PARTICLES)
    positions      = c_positions[:]
    velocities     = c_velocities[:]
    new_positions  = c_new_positions[:]
    new_velocities = c_new_velocities[:]

    for i,new_position in enumerate(new_positions):
        # 2. Update the master Python lists with the new state
        positions[i]  = new_position
        velocities[i] = new_velocities[i]
        
        # 3. Update the NumPy plotting array
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
