# Zajęcia laboratoryjne 001 - Równania ruchu w formalizmie Lagrange'a 
English version in [`README.md`](https://github.com/Mellechowicz/IThPh/blob/master/001/README.md).

## Przygotowanie środowiska pracy 

### Pobieranie repozytorium 
Zacznijmy od sklonowania tego repozytorium `git`:
```bash
git clone https://github.com/Mellechowicz/IThPh.git
```
Następnie przejdź do katalogu i sprawdź gałąź (`master`):
```bash
cd IThPh && git branch
```
Wszystkie pliki do tych zajęć znajdują się w katalogu "IThPh/001".

### Kompilacja biblioteki C do biblioteki współdzielonej 
W katalogu `IThPh/001/solver` znajdziesz plik źródłowy `solver.c`, który zawiera funkcje, nad którymi będziesz pracować. Do skompilowania kodu możesz użyć kompilatora GCC (<https://gcc.gnu.org/>).

1. Najpierw skompiluj plik źródłowy `solver.c`: 
```bash
gcc -pedantic -Wall -c -std=c23 -fPIC solver.c -o solver.o
```
2. Następnie utwórz bibliotekę współdzieloną `libsolver.so`: 
```bash
gcc -std=c23 -shared -Wl,-soname,libsolver.so -o libsolver.so solver.o
```

### Środowisko Python 
W katalogu `IThPh/001/run` znajdziesz dwa pliki w języku Python:
 * `single_particle.py` 
 * `particles.py` 

Wymagane zewnętrzne moduły to: `matplotlib` oraz `numpy`. Ponieważ `matplotlib` wymaga `numpy`, wystarczy zainstalować tylko ten pierwszy za pomocą `pip`:

#### Użycie modułu `venv`
```bash
python3 -m venv venv_matplotlib # Tworzy środowisko wirtualne
. venv_matplotlib/bin/activate  # Aktywuje powyższe środowisko wirtualne
pip3 install matplotlib         # Instaluje matplotlib w środowisku wirtualnym
```

#### Użycie `uv`
```bash
uv venv venv_matplotlib   # Tworzy środowisko wirtualne
cd venv_matplotlib        # Przechodzi do katalogu roboczego
. ./bin/activate          # Aktywuje powyższe środowisko wirtualne
uv pip install matplotlib # Instaluje matplotlib w środowisku wirtualnym
```
Jeśli w jakimkolwiek momencie zechcesz dezaktywować środowisko `venv_matplotlib`, po prostu wpisz:
```bash
deactivate
```

## Instrukcje 

### Oscylator 
#### Praca z plikami `IThPh/001/solver/solver.c` i `IThPh/001/run/single_particle.py` 

 1. Oblicz lagranżjan dla punktu materialnego na sprężynie, której stały koniec znajduje się w $x=0$. Załóż, że: 
    * Układ jest jednowymiarowy ($x$). 
    * Sprężyna jest przymocowana w punkcie $x=0$. 
    * $k$ to współczynnik sprężystości. 
    * Masa wynosi 1 ($m=1$). 
 2. Wyprowadź z (1) równanie ruchu. 
 3. Zmodyfikuj funkcje tak, aby reprezentowały równania z punktu (2):
   ```c
   float next_coordinate_1D(float coord, float vel, float dt);
   float next_velocity_1D(float coord, float vel, float dt);
   ```
   aby obliczały nowe współrzędne i prędkości przy użyciu [metody Eulera](https://pl.wikipedia.org/wiki/Metoda_Eulera). *Wskazówka*: Zastanów się, dlaczego do obliczenia nowej prędkości potrzebne są parametry $k$ i $m$. Zastanów się, jak do C przekazać stałą $k$, jeśli nie ma jej w parametrach, i poprawnie zaktualizuj sygnaturę

 4. Zwiększ wartość `dt` w pliku `single_particle.py` i przedyskutuj stabilność algorytmu (klasyczna, jawna metoda Eulera dla oscylatora harmonicznego jest bezwarunkowo niestabilna). 
 5. Zmień metodę całkowania na: 
    * [Algorytm Verlet](https://pl.wikipedia.org/wiki/Algorytm_Verleta) 
    * [Metodę Rungego-Kutty (2. lub 4. rzędu).](https://pl.wikipedia.org/wiki/Metody_Rungego-Kutty) 

### Sprzężone oscylatory 
#### Praca z plikami `IThPh/001/solver/solver.c` i `IThPh/001/run/particles.py` 

 1. Oblicz lagranżjan dla pierścienia punktów materialnych połączonych sprężynami. Załóż, że: 
    * Punkty materialne są indeksowane jako $i \in \{0, 1, ..., N-1\}$. 
    * Każdy punkt $i$ oddziałuje ze swoimi sąsiadami, wliczając pierwszego i ostatniego (tj. $(i-1)\\%N$ oraz $(i+1)\\%N$). 
    * Układ jest dwuwymiarowy ($x$ i $y$). 
    * Sprężyny posiadają określoną długość swobodną $l_0$.
    * $k$ to współczynnik sprężystości, który jest taki sam dla wszystkich sprężyn. 
    * Wszystkie masy są równe 1 ($m=1$). 
 2. Wyprowadź z (1) równanie ruchu. 
 3. Zmodyfikuj kod `particles.py` tak, żeby przekazywał położenie względne do `next_velocity_2D`, a ta z kolei reprezentowała równania z (2). 
 4. Zmodyfikuj lagranżjan, równania ruchu i plik `solver.c` tak, aby móc zdefiniować współczynniki sprężystości $k_i$ oraz masy $m_i$ odpowiednio dla każdej sprężyny i każdego punktu materialnego. 

### Przeniesienie obciążenia i zrównoleglenie (opcjonalnie) 
Zmodyfikuj kod w taki sposób, aby skrypt w Pythonie jedynie definiował układ i wyświetlał wyniki, podczas gdy cała pętla obliczająca równania ruchu (EoM) dla wszystkich punktów była zagnieżdżona i zrównoleglona w `libsolver.so`. Dobrym punktem wyjścia do zrównoleglenia w C jest <https://www.openmp.org/>.

## Wersje 
Kod był testowany na systemie Debian 13 przy użyciu:
 * GCC 14.2.0, 
 * Python 3.13.5, 
 * numpy 2.2.4, 
 * matplotlib 3.10.1+dfsg1.
