# Laboratory class 001 - Equations of Motion in Lagrange's Formalism 

## Preparing workspace 

### Downloading repository 
Let's start by cloning this `git` repository:
```bash
git clone https://github.com/Mellechowicz/IThPh.git
```
Now move to the directory and check the branch (`master`)
```bash
cd IThPh && git branch
```
All files for this class are in the directory "IThPh/001".

### Compiling the C library to a shared one 
In directory `IThPh/001/solver` you can find the source file `solver.c`, which contains functions you will work with. To compile the code you can use GCC (<https://gcc.gnu.org/>).

1. First compile the source file `solver.c`: 
```bash
gcc -pedantic -Wall -c -std=c23 -fPIC solver.c -o solver.o
```
then 
2. Then create the shared library `libsolver.so`: 
```bash
gcc -std=c23 -shared -Wl,-soname,libsolver.so -o libsolver.so solver.o
```

### Python framework 
In directory `IThPh/001/run` you will find two Python files
 * `single_particle.py` 
 * `particles.py` 

Required external module are: `matplotlib` and `numpy`. As `matplotlib` requires `numpy`, you need only to install the first one using `pip`:
```bash
uv venv venv_matplotlib   # Create a virtual environment
cd venv_matplotlib        # Enter working directory
ov pip install matplotlib # Install matplotlib in the virtual environment
. ./bin/activate          # Activate the virtual environment above
```
If, at any point, you wish to deactivate this `venv_matplotlib`, just run
```bash
deactivate
```

## Instructions 

### Oscillator 
#### Working with [`IThPh/001/solver/solver.c`](https://github.com/Mellechowicz/IThPh/blob/master/001/solver/solver.c) and [`IThPh/001/run/single_particle.py`](https://github.com/Mellechowicz/IThPh/blob/master/001/run/single_particle.py) 

 1. Calculate the Lagrangian of a material point with a spring whose fixed end is at $x=0$. Assume: 
    * The system has one dimension $x$. 
    * The spring is attached at $x=0$. 
    * $k$ is the elastic constant. 
    * The mass is 1 ($m=1$). 
 2. Derive the equation of motion from (1). 
 3. Modify functions so that they represent the equations in (2).
   ```c
   float next_coordinate_1D(float coord, float vel, float dt);
   float next_velocity_1D(float coord, float vel, float dt);
   ```
   so they calculate new coordinates and velocities using [Euler method](https://en.wikipedia.org/wiki/Euler_method). 

 4. Increase `dt` in `single_particle.py` and discuss the algorithm's stability. 
 5. Change the integration method to: 
    * [Verlet](https://en.wikipedia.org/wiki/Verlet_integration) 
    * [Runge-Kutta method (2nd or 4th order).](https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods) 

### Coupled oscillators 
#### Working with [`IThPh/001/solver/solver.c`](https://github.com/Mellechowicz/IThPh/blob/master/001/solver/solver.c) and [`IThPh/001/run/particles.py`](https://github.com/Mellechowicz/IThPh/blob/master/001/run/particles.py) 

 1. Calculate the Lagrangian of a ring of material points connected by springs. Assume: 
    * Material points are indexed $i \in \{0, 1, ..., N-1\}$. 
    * Each point $i$ interacts with its neighbors, including the first and last (i.e., $(i-1)\\%N$ and $(i+1)\\%N$). 
    * The system has 2 dimensions, $x$ and $y$. 
    * $k$ is the elastic constant and is the same for all springs. 
    * All masses are equal to 1 ($m=1$). 
 2. Derive the equation of motion from (1). 
 3. Modify functions so that they represent the equations in (2). 
```c
void next_coordinate_2D(Vector2D* coord, Vector2D* vel, Vector2D* new_coord, float dt); 
void next_velocity_2D(Vector2D* coord, Vector2D* vel, Vector2D* new_vel, float dt);
```
 4. Modify the Lagrangian, the equations of motion, and `solver.c`, so that elastic constants $k_i$ and masses $m_i$ can be defined for each spring and each material point, respectively. 

### Transfer workload and parallelization (optional) 
Modify the code so that Python code only defines the system, while the bulk of the code calculating EoM will be embedded in `libsolver.so`. Good starting point is <https://www.openmp.org/>.

## Versions 
This code was tested on Debian 13 using
 * GCC 14.2.0, 
 * Python 3.13.5, 
 * numpy 2.2.4, 
 * matplotlib 3.10.1+dfsg1. 

