import sympy as sp
from sympy import Symbol, Poly, S
from sympy import symbols as sp_symbols

from core.polynomial import poly_zero, monomials, generate_polynomial


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
    coeffs = (f1.free_symbols | f2.free_symbols) - {x1, x2, x3, p, q, r}

    # Create cyclic term
    f_cyclic = (x1 - x2) * (x2 - x3) * (x3 - x1)
    # Combine expressions
    expr = f1.as_expr() + f2.as_expr() * f_cyclic

    return expr, coeffs


# def pqr(expr: str, symbols: List[str] = []):
#     expr = sp.simplify(expr)
#     poly = Poly(expr)
#
#     if not symbols:
#         symbols = poly.gens
#     else:
#         symbols = sp_symbols(symbols)
#         poly = Poly(expr, symbols)
#
#     return pqr(poly)

# if len(symbols) != 3:
#     return 'The number of variables must be 3'
#
# deg = poly.total_degree()
# pqr_template, coeffs = create_pqr(symbols=symbols, degree=deg)
#
# a, b, c = symbols
# p, q, r = sp_symbols(['p', 'q', 'r'])
#
# subs_list = {p: a + b + c, q: a * b + b * c + c * a, r: a * b * c}
# F = pqr_template.xreplace(subs_list).expand()
#
# F = Poly(str(F), symbols)
# eqs = poly_zero(F - poly)
# eqs = sp.solve(eqs, coeffs)
# if eqs:
#     return pqr_template.xreplace(eqs)
# else:
#     return "Unable to convert. Please check the input expression."


def pqr(poly: Poly):
    pvars = poly.gens

    if len(pvars) != 3:
        return None, "The polynomial must have exactly 3 variables"

    try:
        a, b, c = pvars
        p, q, r = sp.symbols("p q r")
        coefficient_prefix = 'm_'
        # Substitution rules for symmetric polynomials
        subs = {p: a + b + c, q: a * b + b * c + c * a, r: a * b * c}
        # Generate the general pqr-form template
        pqr_template, coeffs = generate_pqr_cyclic(a, b, c, poly.total_degree(), coefficient_prefix)
        # Convert back to polynomial form
        poly_subs = Poly(pqr_template.xreplace(subs).expand(), pvars)
        # Solve for coefficients
        eqs = poly_zero(poly_subs - poly)
        solution = sp.solve(eqs, coeffs)
        if not solution:
            return None, "Unable to convert"

        return pqr_template.xreplace(solution)
    except Exception as e:
        return None, f'Conversion error: {str(e)}'


################################
# f1 = generate_pqr(2)
# f2 = generate_pqr(3)
# print(f1)
# print(f2)
# print(f1.coeffs() + f2.coeffs())
# a, b, c = sp_symbols(['x', 'y', 'z'])
# ff = create_pqr(a, b, c, 4)
# print(ff[0])

# f = Poly('(a^2 + b^2 + c^2)^2-k*(a^3+b^3+c^3)*(a+b+c)', sp_symbols("a b c"))
f = Poly('a+b+c')
res = pqr(f)
if res:
    print(res)
