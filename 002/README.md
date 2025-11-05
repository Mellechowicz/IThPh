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
All files for this class are in the directory "IThPh/002".

### Compiling the C library to a shared one 
In directory `IThPh/002/solver` you can find the source file `solver.c`, which contains functions you will work with. To compile the code you can use GCC (<https://gcc.gnu.org/>).

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
python3 -m venv venv_matplotlib # Create a virtual environment
. venv_matplotlib/bin/activate  # Activate the virtual environment above
pip3 install matplotlib         # Install matplotlib in the virtual environment
```
If, at any point, you wish to deactivate this `venv`, just run
```bash
deactivate
```

## Instructions 

### Coupled oscillators 
#### Working with [`IThPh/002/solver/solver.c`](https://github.com/Mellechowicz/IThPh/blob/master/002/solver/solver.c) and [`IThPh/002/run/particles.py`](https://github.com/Mellechowicz/IThPh/blob/master/002/run/particles.py).

 1. Design a lagrangian for a system of N material points, satisfying
    * Material points are indexed $i \in \{0, 1, ..., N-1\}$. 
    * Each point $i$ interacts with its neighbors, including the first and last (i.e., $(i-1)\\%N$ and $(i+1)\\%N$). 
    * The system has 2 dimensions, $x$ and $y$. 
    * $k$ is the elastic constant and is the same for all springs.
    * Each spring has (the same) equilibruim length $l$.
    * All masses are equal to 1 ($m=1$).
 2. Using [SymPy](https://docs.sympy.org/latest/tutorials/physics/mechanics/index.html) calculate the equation of motion. Example for a pendulum is in [`IthPh/002/run/example_sympy.py`](https://github.com/Mellechowicz/IThPh/blob/master/002/run/example_sympy.py).
 3. Modify functions so that they represent the equations in (2). 
```c
void next_2D(Vector2D* coord, Vector2D* vel, Vector2D* new_coord, Vector2D* new_vel, float dt, size_t N);
float dxdt(float t, float x);
float dydt(float t, float x);
```
 4. Modify the Lagrangian, the equations of motion, and `solver.c`, so that elastic constants $k_i$ and masses $m_i$ can be defined for each spring and each material point, respectively. 
 5. Create a function **in Python** so that file `solver.c` is being rewritten, and the dunctions
```c
float dxdt(float t, float x);
float dydt(float t, float x);
```
updated.

### Transfer workload and parallelization (optional) 
Modify the code so that Python code only defines the system, while the bulk of the code calculating EoM will be embedded in `libsolver.so`. Good starting point is <https://www.openmp.org/>.

## Versions 
This code was tested on Debian 13 using
 * GCC 14.2.0, 
 * Python 3.13.5, 
 * numpy 2.2.4, 
 * matplotlib 3.10.1+dfsg1. 
 * SymPy 1.13.3

