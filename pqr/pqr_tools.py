from itertools import combinations_with_replacement
from typing import List

from sympy import Mul, Symbol, Expr
from sympy import Poly, S, symbols as sp_symbols


# from sympy.abc import a, b, c, p, q, r
# a, b, c, p, q, r = sp_symbols('a b c p q r')

def sort_alphabet(arr):
    return sorted(arr, key=str)


# Viết doc Todo
# monomials(['p', 'q', 'r'], 2) -> [1, p, r**2, q*r, q, p**2, p*r, p*q, q**2, r]
def monomials(symbols: List[str], max_degree: int) -> List[Expr]:
    monomial_list = {S.One}
    symbols = sp_symbols(symbols)

    for deg in range(1, 1 + max_degree):
        for comb in combinations_with_replacement(symbols, deg):
            term = Mul(*comb)
            monomial_list.add(term)

    return list(monomial_list)


# def poly_zero(poly: Poly, symbols: List[str] = []):
def poly_zero(poly: Poly):
    coeffs = poly.as_dict().values()
    eqs = {coeff for coeff in coeffs}

    eqs_vars = poly.free_symbols - set(poly.gens)
    eqs_vars = sort_alphabet(eqs_vars)

    return eqs, eqs_vars


# inext = 1

# Sinh ra đa thức pqr và biến số [m1,m2,...]
# [p = a + b + c, q = a*b + b*c + c*a, r = a*b*c]
def generate_pqr(degree: int, coeff_name: str = 'm'):
    global inext

    # Initialize inext if not exists
    if 'inext' not in globals():
        inext = 1

    poly = S.Zero
    coeffs = []
    symbols = ['p', 'q', 'r']

    a, b, c, p, q, r = sp_symbols("a b c p q r")
    L = {p: a + b + c, q: a * b + b * c + c * a, r: a * b * c}
    monomial_list = monomials(symbols, degree)

    for item in monomial_list:
        # Convert to Expr, substitute, expand, then back to Poly
        substituted_expr = Poly(item, p, q, r).as_expr().subs(L)
        expanded_expr = substituted_expr.expand()

        # Now compute degree in a, b, c
        degree_abc = Poly(expanded_expr, a, b, c).total_degree()

        if degree_abc <= degree:
            coeff = Symbol(f'{coeff_name}{inext}')
            poly += coeff * item
            coeffs.append(coeff)
            inext += 1

    return Poly(poly, sp_symbols(symbols)), coeffs


def create_pqr(degree: int):
    pass


##########################################################
g_pqr = generate_pqr(degree=1, coeff_name='t')
print(g_pqr[0].as_expr())
print(g_pqr[1])
