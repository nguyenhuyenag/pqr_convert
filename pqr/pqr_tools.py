from itertools import combinations_with_replacement
from typing import List

import sympy as sp
from sympy import Mul, Symbol, Expr, UnevaluatedExpr, Poly
from sympy import S, symbols as sp_symbols


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

    # eqs_vars = poly.free_symbols - set(poly.gens)
    # eqs_vars = sort_alphabet(eqs_vars)
    # return eqs, eqs_vars
    return eqs


def degree_of_pqr(item):
    a, b, c, p, q, r = sp_symbols("a b c p q r")
    subs_list = {p: a + b + c, q: a * b + b * c + c * a, r: a * b * c}
    f_abc = Poly(item, p, q, r).as_expr().xreplace(subs_list).expand()
    return Poly(f_abc, a, b, c).total_degree()


# Sinh ra đa thức pqr và biến số [m1,m2,...]
# [p = a + b + c, q = a*b + b*c + c*a, r = a*b*c]
def generate_pqr(degree: int, coeff_name: str = 'm'):
    global inext

    # Initialize inext if not exists
    if 'inext' not in globals():
        inext = 1

    poly = S.Zero  # This is an Expr (not Poly)
    coeffs = []

    monomial_list = monomials(['p', 'q', 'r'], degree)
    for item in monomial_list:
        if degree_of_pqr(item) <= degree:
            coeff = Symbol(f'{coeff_name}{inext}')
            poly += coeff * item
            coeffs.append(coeff)
            inext += 1

    return sp.simplify(poly), coeffs  # Returns Expr (not Poly)


def create_pqr(symbols: List[Symbol], degree: int):
    if degree < 3:
        return generate_pqr(degree)

    coeff_name = 'm'
    a, b, c = symbols

    f1, c1 = generate_pqr(degree, coeff_name=coeff_name)
    f2, c2 = generate_pqr(degree - 3, coeff_name=coeff_name)
    f_cyc = UnevaluatedExpr((a - b) * (b - c) * (c - a))
    poly = f1 + f2 * f_cyc

    return poly, c1 + c2


def pqr(expr: str, symbols: List[str] = []):
    expr = sp.simplify(expr)
    poly = Poly(expr)

    if not symbols:
        symbols = poly.gens
    else:
        symbols = sp_symbols(symbols)
        poly = Poly(expr, symbols)

    if len(symbols) != 3:
        return 'The number of variables must be 3'

    deg = poly.total_degree()
    pqr_template, coeffs = create_pqr(symbols=symbols, degree=deg)

    a, b, c = symbols
    p, q, r = sp_symbols(['p', 'q', 'r'])

    subs_list = {p: a + b + c, q: a * b + b * c + c * a, r: a * b * c}
    F = pqr_template.xreplace(subs_list).expand()

    F = Poly(str(F), symbols)
    eqs = poly_zero(F - poly)
    eqs = sp.solve(eqs, coeffs)
    if eqs:
        return pqr_template.xreplace(eqs)
        # return subs
    else:
        return "Unable to convert. Please check the input expression."
