# Laboratory class 003 - Equations of Motion in Lagrange's Formalism in SymPy

## Preparing workspace 

### Downloading repository 
If you have not done so yet, please start by cloning this `git` repository:
```bash
git clone https://github.com/Mellechowicz/IThPh.git
```
Now move to the directory and check the branch (`master`)
```bash
cd IThPh && git branch
```

Otherwise, just pull the latest changes:
```bash
git pull origin master
```

If you have any conflicts: either move changes to a separate branch or stash them:
```bash
git stash
```
All files for this class are in the directory "IThPh/003".

### Compiling the C library to a shared one 
In directory `IThPh/003/solver` you can find the source file `solver.c`, which contains functions you will work with. To compile the code you can use GCC (<https://gcc.gnu.org/>).

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
In directory `IThPh/003/run` you will find the Python files
 - `particles.py` 
 - `animation.py` 
 - `ccompiler.py` 
 - `cprototype.py` 
 - `lagrangian.py` 

Required external module are: `matplotlib` and `numpy`. As `matplotlib` requires `numpy`, you need only to install the first one using `pip`:
#### Using `venv` module
```bash
python3 -m venv venv_matplotlib # Create a virtual environment
. venv_matplotlib/bin/activate  # Activate the virtual environment above
pip3 install matplotlib         # Install matplotlib in the virtual environment
```

#### Using `uv`
```bash
uv venv venv_matplotlib   # Create a virtual environment
cd venv_matplotlib        # Enter working directory
. ./bin/activate          # Activate the virtual environment above
uv pip install matplotlib # Install matplotlib in the virtual environment
```
If, at any point, you wish to deactivate this `venv_matplotlib`, just run
```bash
deactivate
```

## Instructions 

### Lagrangian and Equations of Motion
#### Working with [`IThPh/003/run/lagrangian.py`](https://github.com/Mellechowicz/IThPh/blob/master/003/run/lagrangian.py).
 1. Familiarize yourself with the code in `lagrangian.py`, especially method `generate_c_function()`.
 2. Run the code by loading the module (it executes `__main__`): `python3 -m lagrangian`
 3. Compare the two generated functions.
 4. Add your own Lagrangian (e.g., a spherical pendulum) and generate the corresponding C functions.

### Framework for solving EoM
#### Working with [`IThPh/003/solver/solver.c`](https://github.com/Mellechowicz/IThPh/blob/master/003/solver/solver.c), [`IThPh/003/run/particles.py`](https://github.com/Mellechowicz/IThPh/blob/master/003/run/particles.py), [`IThPh/003/run/animation.py`](https://github.com/Mellechowicz/IThPh/blob/master/003/run/animation.py), [`IThPh/003/run/ccompiler.py`](https://github.com/Mellechowicz/IThPh/blob/master/003/run/ccompiler.py), [`IThPh/003/run/cprototype.py`](https://github.com/Mellechowicz/IThPh/blob/master/003/run/cprototype.py).
 1. Familiarize yourself with the code in `003/run/particles.py`.
    Note, that since the last class, the code has been refactored to separate logical Python modules. Now `animation.py` contains only code related to visualization and `cprototype.py` contains code related to creating C function prototypes.
 In `ccompiler.py` we can find a class that allows us to compile C code from Python.
 2. Run the script `particles.py`: `python3 particles.py`.
 3. Familiarize yourself with the code in `003/solver/solver.c`.
    Note that the simulation loop is in the functions are executed in object of class `animation2D`. Also, the new functions
    * `void RK4_1D(float* x, float* v, float* dx, float* dv, float t, float dt,
	   void(*dfdx)(float*,float*,float*,float*,float,size_t), size_t N);`
    * `void RK4_2D(Vector2D* x, Vector2D* v, Vector2D* dx, Vector2D* dv, float t, float dt,
	   void(*dfdx)(Vector2D*,Vector2D*,Vector2D*,Vector2D*,float,size_t), size_t N);`
    * `void RK4_3D(Vector3D* x, Vector3D* v, Vector3D* dx, Vector3D* dv, float t, float dt,
	   void(*dfdx)(Vector3D*,Vector3D*,Vector3D*,Vector3D*,float,size_t), size_t N);`
    implement the 4th order Runge-Kutta method for 1D, 2D, and 3D systems, respectively.
    Also, functions `next_1D()`, `next_2D()`, and `next_3D()` do **not** call the corresponding RK4 functions.
 4. Modify the function `next_2D()` to call the corresponding RK4 functions. Add a function with prototype `void(*f)(Vector2D*,Vector2D*,Vector2D*,Vector2D*,float,size_t);` that will compute the derivatives of position and velocity for a 2D system.
 5. Modify code in `003/run/particles.py` so it uses the `Lagrangian_ToM` class to generate function from previous step and compile it "on-fly".

### Transfer workload and parallelization (optional) 
Modify the code so that Python code only defines the system, while the bulk of the code calculating EoM will be embedded in `libsolver.so`. Good starting point is <https://www.openmp.org/>.

## Versions 
This code was tested on Debian 13 using
 - GCC 14.2.0, 
 - Python 3.13.5, 
 - numpy 2.2.4, 
 - matplotlib 3.10.1+dfsg1. 
 - SymPy 1.13.3

