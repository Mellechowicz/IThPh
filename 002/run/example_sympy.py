import sympy as sp
from sympy import symbols, Function, diff, sin, cos, Eq, latex, ccode, simplify

def derive_pendulum_eom():
    """
    Derives the equation of motion for a 1D simple pendulum using
    the Lagrangian method with SymPy.
    """
    
    # --- 1. Define Symbols ---
    
    # t: time
    # m: mass
    # l: length of the pendulum
    # g: acceleration due to gravity
    t = symbols('t')
    m, l, g = symbols('m l g', positive=True, real=True)
    
    # theta: angle as a function of time
    # We use Function for 'theta' because it depends on 't'
    theta = Function('theta')(t)
    
    # --- 2. Define Derivatives ---
    
    # theta_dot: first time derivative of theta (angular velocity)
    # theta_ddot: second time derivative of theta (angular acceleration)
    theta_dot = diff(theta, t)
    theta_ddot = diff(theta_dot, t)
    
    # --- 3. Define Kinetic and Potential Energy ---
    
    # Position of the mass (assuming theta=0 is hanging straight down)
    # x = l * sin(theta)
    # y = -l * cos(theta)
    
    # Velocities
    # x_dot = diff(l * sin(theta), t)
    # y_dot = diff(-l * cos(theta), t)
    
    # Kinetic Energy (T)
    # T = 1/2 * m * (x_dot**2 + y_dot**2)
    # This simplifies to:
    T = sp.Rational(1, 2) * m * l**2 * theta_dot**2
    
    # Potential Energy (V)
    # V = m * g * y
    V = -m * g * l * cos(theta)
    
    # --- 4. Form the Lagrangian (L) ---
    L = T - V
    
    # --- 5. Apply the Euler-Lagrange Equation ---
    #
    # d/dt (dL / d(theta_dot)) - dL / d(theta) = 0
    #
    
    # dL / d(theta)
    dL_dtheta = diff(L, theta)
    
    # dL / d(theta_dot)
    dL_dtheta_dot = diff(L, theta_dot)
    
    # d/dt (dL / d(theta_dot))
    d_dt_dL_dtheta_dot = diff(dL_dtheta_dot, t)
    
    # The Euler-Lagrange equation
    eom_raw = d_dt_dL_dtheta_dot - dL_dtheta
    
    # Create a SymPy Equation object (set equal to 0)
    # We also simplify the result by dividing out common factors (m*l)
    eom = Eq(simplify(eom_raw / (m * l)), 0)
    
    # --- 6. Print the Results ---
    
    print("--- 1D Simple Pendulum Equation of Motion ---")
    
    print("\n[1] Lagrangian (L = T - V):")
    sp.pprint(L)
    
    print("\n[2] Equation of Motion (Standard Print):")
    sp.pprint(eom)
    
    print("\n[3] Equation of Motion (LaTeX):")
    # This format is perfect for reports or papers
    print(latex(eom))
    
    print("\n[4] Equation of Motion (C Code):")
    # This format is useful for numerical simulations
    eom_solved = sp.solve(eom, theta_ddot)[0]
    print(str(ccode(eom,strict=False)))

if __name__ == "__main__":
    # Use SymPy's init_printing for nicer console output
    sp.init_printing(use_unicode=True)
    derive_pendulum_eom()
