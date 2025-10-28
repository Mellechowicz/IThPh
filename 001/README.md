# Preparing workspace

## Downloading repository
We start by cloning this git repository
```bash
git clone https://github.com/Mellechowicz/IThPh.git
```
Now we can move to the directory and check the branch (`master`)
```bash
cd IThPh && git branch
```
All files for this class are in directory "IThPh/001".

## Compliling C library to a shared one
In directory `IThPh/001/solver` we find te source file `solver.c`, containing functions we will work with. To compile the code we are using GCC (https://gcc.gnu.org/).

1. First we compile the source file `solve.c`:
```bash
gcc -pedantic -Wall -c -std=c23 -fPIC solver.c -o solver.o
```
then 
2. we create the shared library `libsolver.so`
```bash
gcc -std=c23 -shared -Wl,-soname,libsolver.so -o libsolver.so solver.o && cd -
```

## Python framework
In directory `IThPh/001/run` we find two Python files
 * `single_particle.py`
 * `particles.py`

# Instructions

## Oscillator
### Woriking with `IThPh/001/solver/solver.c` and `IThPh/001/run/single_particle.py`

1. Calculate Lagrangian of a material point with a spring attached in 0. Assume:
    * System has 1 dimension $x$.
    * Spring is attached in $x=0$.
    * $k$ - elastic constant.
    * Mass is equal to 1 ($m=1$).
2. Derive the equation of motion from 1.
3. Modify functions
    *
```c
float next_coordinate_1D(float coord, float vel, float dt);
float next_velocity_1D(float coord, float vel, float dt);
```
   so they are calculating new coordinates and velocities using Euler method.
4. Increase `dt` in `single_particle.py` and discuss the algorithm stability.
5. Change the integration method to:
    * Verlet
    * Runge-Kutta method (2nd or 4th order).

## Coupled oscillators
### Woriking with `IThPh/001/solver/solver.c` and `IThPh/001/run/particles.py`

1. Calculate Lagrangian of a series of material points attached with springs. Assume:
    * Material points are organized with indices $i \in \{0, 1, ..., N-1\}$.
    * Each point $i$ interacts with its neighbors - including first and last, i.e., $(i-1)~mod~N$ and $(i+1)~mod~N$.
    * System has 2 dimensions $x$ and $y$.
    * $k$ - elastic constant does not depend on the spring.
    * All masses are equal to 1 ($m=1$).
2. Derive the equation of motion from 1.
3. Modify functions
    *
```c
float next_coordinate_1D(float coord, float vel, float dt);
float next_velocity_1D(float coord, float vel, float dt);
```
4. Modify Lagrangian, Equations of motion, and `solver.c`, so that elastic constants $k_i$ and masses $m_i$ can be defined for each spring and material point respectively.

