from typing import List

from sympy import Symbol, Poly, S, symbols, solve, simplify

from core.polynomial import poly_zero, monomials, generate_polynomial
from util import messages

pools_monomials = {}


def degree_of_pqr(pqr_expr) -> int:
    """
        Degree of pqr expression:
        [p = a + b + c, q = a*b + b*c + c*a, r = a*b*c]
        degree p = 1, degree q = 2, degree r = 3
        Total degree of pqr = degree of p + 2 * degree of q + 3 * degree of r
    """
    p, q, r = symbols("p q r")
    # Chuyển biểu thức về dạng đa thức theo p, q, r
    poly = Poly(pqr_expr, p, q, r)
    # poly.gens = (p, q, r)
    # Tính tổng: 1 * (số mũ của p) + 2*(số mũ của q) + 3*(số mũ của r)
    degrees = [1 * monom[0] + 2 * monom[1] + 3 * monom[2] for monom in poly.monoms()]
    return max(degrees) if degrees else 0


def pqr_polynomial(degree: int, coeff_name: str):
    """
        Sinh đa thức pqr
    """
    key = degree  # Chỉ dùng degree vì biến luôn là ['p', 'q', 'r']

    # Nếu đã có monomials cho degree này thì lấy ra, chưa có thì tạo và lưu vào pool
    if key in pools_monomials:
        monomial_list = pools_monomials[key]
    else:
        monomial_list = monomials(['p', 'q', 'r'], degree)
        monomial_list = [x for x in monomial_list if degree_of_pqr(x) <= degree]
        pools_monomials[key] = monomial_list

    return generate_polynomial(monomial_list, coeff_name)


def generate_pqr_cyclic(x1: Symbol, x2: Symbol, x3: Symbol, degree: int, coeff_name: str):
    # Generate pqr polynomials
    f1 = pqr_polynomial(degree, coeff_name)
    f2 = pqr_polynomial(degree - 3, coeff_name) if degree >= 3 else S.Zero
    # Extract coefficients
    p, q, r = symbols("p q r")
    coeffs = (f1.free_symbols | f2.free_symbols) - {x1, x2, x3, p, q, r, symbols(coeff_name)}
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
        p, q, r = symbols("p q r")
        coeff_name = 'm'

        # Substitution rules for symmetric polynomials
        subs = {p: a + b + c, q: a * b + b * c + c * a, r: a * b * c}

        # Generate the generalized pqr polynomial
        pqr_general, coeffs = generate_pqr_cyclic(a, b, c, poly.total_degree(), coeff_name)

        # Convert back to polynomial form
        poly_template = Poly(pqr_general.xreplace(subs).expand(), pvars)

        # Solve for coefficients
        eqs = poly_zero(poly_template - poly)
        root = solve(eqs, coeffs)
        if not root:
            return None, messages.conversion_error

        result = pqr_general.xreplace(root)

        return result, None
    except Exception as e:
        # print(f'Conversion error: {str(e)}')
        return None, messages.conversion_error


def pqr_from_expr(expr: str, pvars: List[str]):
    expr = simplify(expr)
    all_vars = symbols(pvars)
    poly = Poly(expr, all_vars)
    return pqr(poly)
