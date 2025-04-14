from typing import List

import sympy as sp
from sympy import Symbol, Poly, S
from sympy import symbols as sp_symbols

from core.polynomial import poly_zero, monomials, generate_polynomial
from util import messages


# Degree of pqr expression:
# [p = a + b + c, q = a*b + b*c + c*a, r = a*b*c]
# degree p = 1, degree q = 2, degree r = 3
# Total degree of pqr = degree of p + 2 * degree of q + 3 * degree of r
def degree_of_pqr(pqr_expr) -> int:
    p, q, r = sp_symbols("p q r")
    # Chuyển biểu thức về dạng đa thức theo p, q, r
    poly = Poly(pqr_expr, p, q, r)
    # poly.gens = (p, q, r)
    # Tính tổng: 1 * (số mũ của p) + 2*(số mũ của q) + 3*(số mũ của r)
    degrees = [1 * monom[0] + 2 * monom[1] + 3 * monom[2] for monom in poly.monoms()]
    return max(degrees) if degrees else 0


# Sinh ra đa thức core và biến số [m1,m2,...]
# [p = a + b + c, q = a*b + b*c + c*a, r = a*b*c]
def pqr_polynomial(degree: int, coeff_name: str):
    monomial_list = monomials(['p', 'q', 'r'], degree)
    # Filter the monomials that are degree_item <= degree
    monomial_list = [x for x in monomial_list if degree_of_pqr(x) <= degree]
    return generate_polynomial(monomial_list, coeff_name)


def generate_pqr_cyclic(x1: Symbol, x2: Symbol, x3: Symbol, degree: int, coeff_name: str):
    # Generate pqr polynomials
    f1 = pqr_polynomial(degree, coeff_name)
    f2 = pqr_polynomial(degree - 3, coeff_name) if degree >= 3 else S.Zero
    # Extract coefficients
    p, q, r = sp.symbols("p q r")
    coeffs = (f1.free_symbols | f2.free_symbols) - {x1, x2, x3, p, q, r, sp.symbols(coeff_name)}
    # Create cyclic term
    f_cyclic = (x1 - x2) * (x2 - x3) * (x3 - x1)
    # Combine expressions
    expr = f1.as_expr() + f2.as_expr() * f_cyclic
    return expr, coeffs


def pqr(poly: Poly):
    pvars = poly.gens
    
    if len(pvars) != 3:
        return None, messages.expression_variable_count_error

    try:
        a, b, c = pvars
        p, q, r = sp.symbols("p q r")
        coeff_name = 'm'

        # Substitution rules for symmetric polynomials
        subs = {p: a + b + c, q: a * b + b * c + c * a, r: a * b * c}

        # Generate the generalized pqr polynomial
        pqr_general, coeffs = generate_pqr_cyclic(a, b, c, poly.total_degree(), coeff_name)

        # Convert back to polynomial form
        poly_template = Poly(pqr_general.xreplace(subs).expand(), pvars)

        # Solve for coefficients
        eqs = poly_zero(poly_template - poly)
        root = sp.solve(eqs, coeffs)
        if not root:
            return None, messages.conversion_error

        result = pqr_general.xreplace(root)

        return result, None
    except Exception as e:
        # print(f'Conversion error: {str(e)}')
        return None, messages.conversion_error


def pqr_from_expr(expr: str, symbols: List[str]):
    expr = sp.simplify(expr)
    symbols = sp_symbols(symbols)
    poly = Poly(expr, symbols)
    return pqr(poly)
