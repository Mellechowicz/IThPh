# Instructions

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
