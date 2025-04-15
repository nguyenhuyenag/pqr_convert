from typing import List
from sympy import Symbol, Poly, S, symbols, solve, simplify
from core.polynomial import poly_zero, monomials, generate_polynomial
from util import messages

pqr_pools = {}
"""Cache for pqr polynomials"""

monomials_pools = {}
"""Cache for monomials of pqr polynomials"""

"""
    Define: [p = a + b + c, q = a*b + b*c + c*a, r = a*b*c]
"""

p, q, r = symbols("p q r")


def degree_of_pqr(pqr_expr) -> int:
    """
        Degree of pqr expression: degree p = 1, degree q = 2, degree r = 3

        The total degree is: 1*deg_p + 2*deg_q + 3*deg_r
    """
    # p, q, r = symbols("p q r")
    poly = Poly(pqr_expr, p, q, r)
    degrees = [1 * monom[0] + 2 * monom[1] + 3 * monom[2] for monom in poly.monoms()]
    return max(degrees) if degrees else 0


def pqr_polynomial(degree: int, coeff_name: str):
    """
        Sinh đa thức pqr
    """
    # Nếu đã có monomials cho degree này thì lấy ra, chưa có thì tạo và lưu vào pool
    if degree in monomials_pools:
        monomial_list = monomials_pools[degree]
    else:
        monomial_list = monomials(['p', 'q', 'r'], degree)
        monomial_list = [x for x in monomial_list if degree_of_pqr(x) <= degree]
        monomials_pools[degree] = monomial_list

    return generate_polynomial(monomial_list, coeff_name)


def pqr_generate(x1: Symbol, x2: Symbol, x3: Symbol, degree: int, coeff_name: str):
    """
        return f(p,q,r), f(a+b+c, a*b+b*c+c*a, a*b*c), [m1, m2, m3,...]
    """

    if degree in pqr_pools:
        return pqr_pools.get(degree)
    else:
        f1 = pqr_polynomial(degree, coeff_name)
        f2 = pqr_polynomial(degree - 3, coeff_name) if degree >= 3 else S.Zero

        # Extract coefficients
        coeffs = (f1.free_symbols | f2.free_symbols) - {x1, x2, x3, p, q, r, symbols(coeff_name)}

        # Create cyclic term
        f_cyclic = (x1 - x2) * (x2 - x3) * (x3 - x1)
        f_pqr = f1.as_expr() + f2.as_expr() * f_cyclic

        # Substitution rules for symmetric polynomials
        subs = {p: x1 + x2 + x3, q: x1 * x2 + x2 * x3 + x3 * x1, r: x1 * x2 * x3}
        f_abc = Poly(f_pqr.xreplace(subs).expand(), x1, x2, x3)

        # Save to pools
        pqr_pools[degree] = (f_pqr, f_abc, coeffs)
        return f_pqr, f_abc, coeffs


def pqr(poly: Poly):
    pvars = poly.gens

    if len(pvars) != 3:
        return None, messages.expression_variable_count_error

    try:
        a, b, c = pvars
        coeff_name = 'm_'

        f_pqr, f_abc, coeffs = pqr_generate(a, b, c, poly.total_degree(), coeff_name)

        # Đồng nhất hệ số của poly và f_abc
        eqs = poly_zero(f_abc - poly)
        root = solve(eqs, coeffs)
        if not root:
            return None, messages.conversion_error

        # Thay thế các hệ số vào f_pqr mẫu
        result = f_pqr.xreplace(root)

        return result, None
    except Exception as e:
        # print(f'Conversion error: {str(e)}')
        return None, messages.conversion_error


def pqr_from_expr(expr: str, pvars: List[str]):
    expr = simplify(expr)
    all_vars = symbols(pvars)
    poly = Poly(expr, all_vars)
    return pqr(poly)
