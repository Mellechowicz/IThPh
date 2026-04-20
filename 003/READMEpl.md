# Zajęcia laboratoryjne 003 – Równania ruchu w formalizmie Lagrange'a w SymPy
Wersja angielska w pliku [`README.md`](https://github.com/Mellechowicz/IThPh/blob/master/003/README.md).

## Przygotowanie środowiska pracy

### Pobieranie repozytorium
Jeśli jeszcze tego nie zrobiłeś/aś, zacznij od sklonowania repozytorium `git`:
```bash
git clone https://github.com/Mellechowicz/IThPh.git
```
Teraz przejdź do katalogu i sprawdź gałąź (`master`):
```bash
cd IThPh && git branch
```

### Aktualizacja
Jeżeli repozytorium jest już _ściągnięte_, wystarczy przejść do katalogu i wykonać polecenie
```bash
git pull
```
Jeżeli polecenie zakończy się błędem (nie będzie mogła zsynchronizować się gałąź główna), można albo sklonować repozytorium ponownie (jak wyżej), wrzucić zmiany do schowka i wrócić na gałąź główną
```bash
git stash && git switch master
```
zapisać zmiany na nowej gałęzi
```bash
git checkout -b nowa_galaz && git add -A . && git commit -m "Moj opis" && git switch master && git reset --hard && git pull
```
lub usunąć wszystkie zmiany
```bash
git switch master && git reset --hard && git pull
```
Wszystkie pliki na te zajęcia znajdują się w katalogu `IThPh/003`.

### Środowisko Python
W katalogu `IThPh/003/run` znajdziesz pliki Pythona:
 - `particles.py`
 - `animation.py`
 - `ccompiler.py`
 - `cprototype.py`
 - `lagrangian.py`

**Poniższe polecenia mają zastosowanie tylko przy pracy na stanowiskach niepracownianych.**
Wymagane zewnętrzne moduły to: `matplotlib` i `numpy`. Ponieważ `matplotlib` wymaga `numpy`, wystarczy zainstalować tylko ten pierwszy za pomocą `pip`:

#### Używając modułu `venv`
```bash
python3 -m venv venv_matplotlib # Utwórz środowisko wirtualne
. venv_matplotlib/bin/activate  # Aktywuj powyższe środowisko wirtualne
pip3 install matplotlib         # Zainstaluj matplotlib w środowisku wirtualnym
```

#### Używając `uv`
```bash
uv venv venv_matplotlib          # Utwórz środowisko wirtualne
. ./venv_matplotlib/bin/activate # Aktywuj powyższe środowisko wirtualne
uv pip install matplotlib        # Zainstaluj matplotlib w środowisku wirtualnym
```
Jeśli w dowolnym momencie chcesz dezaktywować to środowisko `venv_matplotlib`, uruchom po prostu:
```bash
deactivate
```

## Instrukcje

### Lagranżjan i równania ruchu
#### Praca z [`IThPh/003/run/lagrangian.py`](https://github.com/Mellechowicz/IThPh/blob/master/003/run/lagrangian.py).
 1. Zapoznaj się z kodem w `lagrangian.py`, a w szczególności z metodą `generate_c_function()`.
 2. Uruchom kod ładując moduł (wykonuje się `__main__`): `python3 -m lagrangian`
 3. Porównaj dwie wygenerowane funkcje.
 4. Dodaj własny lagranżjan (np. wahadło sferyczne) i wygeneruj odpowiadające mu funkcje C.

### Środowisko do rozwiązywania równań ruchu
#### Praca z [`IThPh/003/solver/solver.c`](https://github.com/Mellechowicz/IThPh/blob/master/003/solver/solver.c), [`IThPh/003/run/particles.py`](https://github.com/Mellechowicz/IThPh/blob/master/003/run/particles.py).
 1. Zapoznaj się z kodem w `003/run/particles.py`.
    Zwróć uwagę, że od ostatnich zajęć kod został zrefaktoryzowany w celu rozdzielenia na odrębne logiczne moduły Pythona. Teraz `animation.py` zawiera jedynie kod związany z wizualizacją, a `cprototype.py` zawiera kod związany z prototypami funkcji C.
 W `ccompiler.py` znajdziemy klasę umożliwiającą kompilację kodu C z poziomu Pythona.
 2. Uruchom skrypt `particles.py`: `python3 particles.py`.
 3. Zapoznaj się z kodem w `003/solver/solver.c`.
    Zwróć uwagę, że pętla symulacji jest w funkcjach wykonywanych w obiekcie klasy `animation2D`. Ponadto nowe funkcje:
    * `void RK4_1D(float* x, float* v, float* dx, float* dv, float t, float dt,
       void(*dfdx)(float*,float*,float*,float*,float,size_t), size_t N);`
    * `void RK4_2D(Vector2D* x, Vector2D* v, Vector2D* dx, Vector2D* dv, float t, float dt,
       void(*dfdx)(Vector2D*,Vector2D*,Vector2D*,Vector2D*,float,size_t), size_t N);`
    * `void RK4_3D(Vector3D* x, Vector3D* v, Vector3D* dx, Vector3D* dv, float t, float dt,
       void(*dfdx)(Vector3D*,Vector3D*,Vector3D*,Vector3D*,float,size_t), size_t N);`
    implementują metodę Rungego-Kutty 4. rzędu odpowiednio dla układów 1D, 2D i 3D.
    Ponadto funkcje `next_1D()`, `next_2D()` i `next_3D()` **nie** wywołują odpowiadających im funkcji RK4.
 4. Zmodyfikuj funkcję `next_2D()` tak, aby wywoływała odpowiednie funkcje RK4. Dodaj funkcję z prototypem `void(*f)(Vector2D*,Vector2D*,Vector2D*,Vector2D*,float,size_t);`, która będzie obliczać pochodne na podstawie równań ruchu wyprowadzonych z lagranżjanu.
 5. Zmodyfikuj kod w `003/run/particles.py` tak, aby używał klasy `LagrangianToC` do generowania funkcji z poprzedniego kroku i kompilował ją „w locie".

### Przeniesienie obciążenia obliczeniowego i zrównoleglenie (opcjonalne)
Zmodyfikuj kod tak, aby kod Pythona jedynie definiował układ, natomiast zasadnicza część kodu obliczającego równania ruchu była osadzona w `libsolver.so`. Dobrym punktem wyjścia jest <https://www.openmp.org/>.

## Wersje
Ten kod był testowany na Debianie 13 przy użyciu:
 - GCC 14.2.0,
 - Python 3.13.5,
 - numpy 2.2.4,
 - matplotlib 3.10.1+dfsg1,
 - SymPy 1.13.3
