from itertools import combinations_with_replacement
from typing import List, Union, Set, Tuple

import sympy as sp
from sympy import Poly, Expr, S, Mul, Symbol, IndexedBase

_coeff_counter = 1
"""A global counter used to assign unique indices to coefficients."""


def monomials(symbols: Union[List[str], List[Symbol]], degree: int, is_homogeneous: bool = False) -> List[Expr]:
    """
        Generate a list of monomials up to a given total degree using specified variables.

        Example:
        > monomials(['a', 'b', 'c'], 2)

            [1, a*b, a**2, a*c, a, b**2, b*c, c**2, c, b]

        > monomials(['a', 'b', 'c'], 2, is_homogeneous=True)

            [a*b, b**2, c**2, b*c, a**2, a*c]
    """
    symbols = [sp.symbols(x) if isinstance(x, str) else x for x in symbols]

    monomial_list = set() if is_homogeneous else {S.One}

    for deg in range(1, 1 + degree):
        for comb in combinations_with_replacement(symbols, deg):
            term = Mul(*comb)
            monomial_list.add(term)

    if is_homogeneous:
        return [x for x in monomial_list if degree == Poly(x, symbols).total_degree()]

    return list(monomial_list)


def generate_polynomial(monomial_list: List[Expr], coeff_name: str = 'm') -> Tuple[Poly, List[Symbol]]:
    """
        Generate a symbolic polynomial with indexed coefficients from a list of monomials.

        Example:
        > mons = monomials(['x', 'y'], 2)
        > poly = generate_polynomial(mons, 'm')

            x**2*m[5] + x*y*m[2] + x*m[6] + y**2*m[3] + y*m[4] + m[1]
    """
    global _coeff_counter

    idx = IndexedBase(coeff_name)

    poly = S.Zero
    pvars = set()
    coeffs = []

    for mono in monomial_list:
        coeff = idx[_coeff_counter]
        poly += coeff * mono
        coeffs.append(coeff)
        pvars.union(mono.free_symbols)
        _coeff_counter += 1  # Tăng chỉ số

    return Poly(poly, *pvars)


def poly_zero(poly: Poly) -> Set[Expr]:
    """Extract the set of constant terms (coefficients) from a sympy polynomial."""
    return set(poly.as_dict().values())


mons = monomials(['x', 'y'], 2)
poly = generate_polynomial(mons, 'm')
print(poly.as_expr())
# Unresolved attribute reference 'as_expr' for class '(Poly, list)'
