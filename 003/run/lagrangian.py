from typing import List,Optional

import sympy as sp
from sympy.physics.mechanics import LagrangesMethod, dynamicsymbols
from sympy.printing.c import ccode

class LagrangianToC:
    vectorType: str = "float"
    def __init__(self, L: sp.Expr,
                 q: List[sp.Expr]) -> None:
        """
        Initialize the generator using sympy.physics.mechanics.

        Args:
            L (sympy.Expr): The Lagrangian expression (L = T - V).
            q (list): List of generalized coordinates (dynamicsymbols).
        """
        self.L = L
        self.q = q
        # We don't need to pass velocities explicitly; LagrangesMethod infers q_dot

    def generate_c_function(self, func_name="equations_of_motion", collapse_constants: bool=True) -> str:
        """
        Generates a C function string that computes accelerations.
        """
        # 1. Initialize LagrangesMethod
        # This automatically computes d/dt(dL/dqdot) - dL/dq = Forces
        LM = LagrangesMethod(self.L, self.q)

        # 2. Form the equations
        LM.form_lagranges_equations()

        # 3. Get the Right-Hand Side (RHS) of the equations of motion.
        # LM.rhs() returns a column vector of size 2N: [q_dot; q_ddot].
        # The top half is just velocities, the bottom half is accelerations.
        # This step implicitly solves M * q_ddot = F for q_ddot.
        full_rhs = LM.rhs()

        n = len(self.q)
        # Extract only the acceleration expressions (the bottom N rows)
        accel_exprs = full_rhs[n:, 0]

        # 4. Identify Constants
        # Get all free symbols from the expressions
        # We use the derived expressions to ensure we catch everything needed
        all_free = set()
        for expr in accel_exprs:
            all_free.update(expr.free_symbols)

        # Identify dynamic symbols (q, u, t) to exclude them from the constants list
        # LM.q contains coordinates, LM.u contains speeds (velocities)
        dynamic_vars = set(LM.q) | set(LM.u) | {dynamicsymbols._t}

        constants = sorted([s for s in all_free if s not in dynamic_vars], key=lambda x: x.name)

        # 5. Create Symbol Mapping for C-Array access
        # We substitute the sympy symbols with explicit C-string formatted symbols
        # e.g. theta(t) -> q[0], u_0 -> dq[0]

        subs_map = {}

        # Map coordinates q_i -> q[i]
        for i, q_sym in enumerate(LM.q):
            # We create a dummy symbol named "q[i]" so ccode prints it exactly so
            subs_map[q_sym] = sp.Symbol(f"q[{i}]")

        # Map speeds u_i -> dq[i]
        for i, u_sym in enumerate(LM.u):
            subs_map[u_sym] = sp.Symbol(f"dq[{i}]")

        # 6. Construct the C Function
        lines = []

        # Function Signature
        if collapse_constants:
            lines.append(f"void {func_name}({self.vectorType}* q, {self.vectorType}* dq, {self.vectorType}* _dq, {self.vectorType}* _ddq, float t, size_t N) {{")
        else:
            const_args = ", ".join([f"float {c.name}" for c in constants])
            sig_constants = f", {const_args}" if const_args else ""
            lines.append(f"void {func_name}({self.vectorType}* q, {self.vectorType}* dq, {self.vectorType}* _dq, {self.vectorType}* _ddq, float t, size_t N{sig_constants}) {{")
        lines.append("    // Auto-generated Euler-Lagrange Equations using sympy.physics.mechanics")

        if collapse_constants:
            lines.append("    // Constants have been collapsed into their values.")
            for i,c in enumerate(constants):
                lines.append(f"    float {c.name} = {i}.0{i+1} /* assign proper {c.name} value here */;")
        for i, expr in enumerate(accel_exprs):
            # Apply the substitution mapping
            mapped_expr = expr.subs(subs_map)

            # Generate C code
            c_str = ccode(mapped_expr)
            lines.append(f"    _dq[{i}] = dq[{i}];")
            lines.append(f"    _ddq[{i}] = {c_str};")

        lines.append("return;")
        lines.append("}")

        return "\n".join(lines)

# ==========================================
#                                                                        
#   ▄▄▄▄▄▄▄▄                                          ▄▄▄▄               
#   ██▀▀▀▀▀▀                                          ▀▀██               
#   ██        ▀██  ██▀   ▄█████▄  ████▄██▄  ██▄███▄     ██       ▄████▄  
#   ███████     ████     ▀ ▄▄▄██  ██ ██ ██  ██▀  ▀██    ██      ██▄▄▄▄██ 
#   ██          ▄██▄    ▄██▀▀▀██  ██ ██ ██  ██    ██    ██      ██▀▀▀▀▀▀ 
#   ██▄▄▄▄▄▄   ▄█▀▀█▄   ██▄▄▄███  ██ ██ ██  ███▄▄██▀    ██▄▄▄   ▀██▄▄▄▄█ 
#   ▀▀▀▀▀▀▀▀  ▀▀▀  ▀▀▀   ▀▀▀▀ ▀▀  ▀▀ ▀▀ ▀▀  ██ ▀▀▀       ▀▀▀▀     ▀▀▀▀▀  
#                                           ██                           
#                                                                        
# run as: python3 -m lagrangian
# ==========================================

if __name__ == "__main__":

    # --- Example 1: Simple Pendulum ---
    print("--- Generating Code for Simple Pendulum ---")

    # 1. Define Dynamics Symbols (Functions of time)
    theta = dynamicsymbols('theta')
    theta_dot = theta.diff()

    # 2. Define Constants
    m, g, l = sp.symbols('m g l')

    # 3. Define Energies
    # Kinetic T = 1/2 m (l * theta_dot)^2
    T = sp.Rational(1, 2) * m * (l * theta_dot)**2
    # Potential V = m g l (1 - cos(theta))
    V = m * g * l * (1 - sp.cos(theta))

    L = T - V

    # 4. Generate
    # Note: We only pass L and the coordinate list [theta]
    gen = LagrangianToC(L, [theta])
    print(gen.generate_c_function("pendulum_step"))
    print("\n")

    # --- Example 2: Double Pendulum (Demonstrating Matrix Solving Capability) ---
    print("--- Generating Code for Double Pendulum ---")

    # Coordinates
    q1, q2 = dynamicsymbols('q1 q2')
    q1d, q2d = q1.diff(), q2.diff()

    # Constants
    m1, m2, l1, l2 = sp.symbols('m1 m2 l1 l2')

    # Position of mass 1
    x1 = l1 * sp.sin(q1)
    y1 = -l1 * sp.cos(q1)

    # Position of mass 2
    x2 = x1 + l2 * sp.sin(q2)
    y2 = y1 - l2 * sp.cos(q2)

    # Kinetic Energy
    v1_sq = x1.diff(dynamicsymbols._t)**2 + y1.diff(dynamicsymbols._t)**2
    v2_sq = x2.diff(dynamicsymbols._t)**2 + y2.diff(dynamicsymbols._t)**2

    T_dp = 0.5 * m1 * v1_sq + 0.5 * m2 * v2_sq

    # Potential Energy
    V_dp = m1*g*y1 + m2*g*y2

    L_dp = T_dp - V_dp

    gen2 = LagrangianToC(L_dp, [q1, q2])
    print(gen2.generate_c_function("double_pendulum_step",collapse_constants=False))
