# Laboratorium 002 – Równania ruchu w formalizmie Lagrange'a z użyciem SymPy

## Przygotowanie środowiska pracy 
Jeżeli repozytorium istnieje, przejdź do kroku aktualizacja.

### Pobieranie repozytorium 
Zacznijmy od sklonowania tego repozytorium `git`:
```bash
git clone https://github.com/Mellechowicz/IThPh.git
```
Następnie przejdź do katalogu i sprawdź aktywną gałąź (`master`):
```bash
cd IThPh && git branch
```

### Aktualizacja
Jeżeli repozytorum jest już _ściągnięte_, wystarczy przejść do katalogu i wykonać polecenie
```bash
git pull
```
Jeżeli polecenie zakończy się błędem (nie będzie mogła zsynchronizować się gałąź główna), można albo sklonować repozytorium ponownie (jak wyżej), wrzucić zmiany do schowka i wrócić na gałąź główną
```bash
git stash && git switch master
```
zapisać zmiany na nowej gałęzi
```bash
git checkout -b nowa_galaz && git add . -A && git commit -m "Moj opis" && git switch master && git reset --hard && git pull
```
lub usunąć wszystkie zmiany
```bash
git switch master && git reset --hard && git pull
```
Wszystkie pliki do tych zajęć znajdują się w katalogu `IThPh/002`.

### Kompilacja biblioteki C jako współdzielonej (shared library)
W katalogu `IThPh/002/solver` znajdziesz plik źródłowy `solver.c`, który zawiera funkcje, z którymi będziesz pracować. Do skompilowania kodu możesz użyć kompilatora GCC (<https://gcc.gnu.org/>).
1. Najpierw skompiluj plik źródłowy `solver.c`: 
```bash
gcc -pedantic -Wall -c -fPIC solver.c -o solver.o
```
2. Następnie utwórz bibliotekę współdzieloną `libsolver.so`: 
```bash
gcc -shared -Wl,-soname,libsolver.so -o libsolver.so solver.o
```

### Środowisko Python 
W katalogu `IThPh/002/run` znajdziesz dwa pliki w języku Python:
 * `single_particle.py` 
 * `particles.py` 

Wymagane zewnętrzne moduły to: `matplotlib` oraz `numpy`. Ponieważ `matplotlib` wymaga do działania modułu `numpy`, wystarczy zainstalować tylko ten pierwszy, używając `pip`:

Jeżeli **nie** pracujesz na maszynie pracownianej, zalecane jest korzystanie z środowisk wirtualnych:
#### Użycie modułu `venv`
```bash
python3 -m venv venv_matplotlib # Utworzenie wirtualnego środowiska
. venv_matplotlib/bin/activate  # Aktywacja środowiska wirtualnego
pip3 install matplotlib         # Instalacja matplotlib w środowisku
```

#### Użycie narzędzia `uv`
```bash
uv venv venv_matplotlib   # Utworzenie wirtualnego środowiska
cd venv_matplotlib        # Przejście do katalogu roboczego
. ./bin/activate          # Aktywacja środowiska wirtualnego
uv pip install matplotlib # Instalacja matplotlib w środowisku
```
Jeśli w którymś momencie zechcesz dezaktywować środowisko `venv_matplotlib`, po prostu uruchom:
```bash
deactivate
```

## Instrukcje 

### Sprzężone oscylatory 
#### Praca z plikami [`IThPh/002/solver/solver.c`](https://github.com/Mellechowicz/IThPh/blob/master/002/solver/solver.c) oraz [`IThPh/002/run/particles.py`](https://github.com/Mellechowicz/IThPh/blob/master/002/run/particles.py).

 1. Zapisz lagrangian (funkcję Lagrange'a) dla układu $N$ punktów materialnych, spełniający następujące założenia:
    * Punkty materialne są indeksowane jako $i \in \{0, 1, ..., N-1\}$. 
    * Każdy punkt $i$ oddziałuje ze środkiem układu współrzędnych (0,0).
    * Układ jest dwuwymiarowy ($x$ oraz $y$). 
    * $k$ to stała sprężystości, która jest identyczna dla wszystkich sprężyn.
    * Każda sprężyna ma taką samą długość równowagową $l$.
    * Wszystkie masy są równe 1 ($m=1$).
 2. Używając biblioteki [SymPy](https://docs.sympy.org/latest/tutorials/physics/mechanics/index.html) wyznacz równania ruchu. Przykład dla wahadła znajduje się w pliku [`IThPh/002/run/example_sympy.py`](https://github.com/Mellechowicz/IThPh/blob/master/002/run/example_sympy.py).
 3. Zmodyfikuj poniższe funkcje, aby reprezentowały równania z punktu (1): 
```c
void next_2D(Vector2D* coord, Vector2D* vel, Vector2D* new_coord, Vector2D* new_vel, float dt, size_t N);
float dxdt(float t, float x);
float dydt(float t, float x);
```
 4. Zmodyfikuj lagrangian, równania ruchu oraz plik `solver.c` w taki sposób, aby stałe sprężystości $k_i$, długości spoczynkowe $l_i$ oraz masy $m_i$ mogły być zdefiniowane niezależnie, odpowiednio dla każdej sprężyny i każdego punktu materialnego. 
 5. Utwórz funkcję **w Pythonie**, która automatycznie nadpisze plik `solver.c` i zaktualizuje w nim poniższe funkcje:
```c
float dxdt(float t, float x);
float dydt(float t, float x);
```

### Przeniesienie obciążenia i zrównoleglenie obliczeń (opcjonalne) 
Zmodyfikuj kod w taki sposób, aby kod w Pythonie jedynie definiował układ, podczas gdy główna część pracy polegająca na obliczaniu równań ruchu (EoM) została osadzona i wykonywana w bibliotece `libsolver.so`. Dobrym punktem startowym jest <https://www.openmp.org/>.

## Wersje oprogramowania 
Powyższy kod był testowany w systemie Debian 13 przy użyciu:
 * GCC 14.2.0
 * Python 3.13.5
 * NumPy 2.2.4
 * Matplotlib 3.10.1+dfsg1
 * SymPy 1.13.3

