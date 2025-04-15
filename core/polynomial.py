from itertools import combinations_with_replacement
from typing import List, Union, Set, Tuple

# import sympy as sp
from sympy import Poly, Expr, S, Mul, Symbol, IndexedBase, symbols

_coeff_index_ = 1
"""A global counter used to assign unique indices to coefficients."""


def monomials(variables: Union[List[str], List[Symbol]], degree: int, is_homogeneous: bool = False) -> List[Expr]:
    """
        Generate a list of monomials up to a given total degree using specified variables.

        Example:
        > monomials(['a', 'b', 'c'], 2)

            [1, a, b, c, a*b, a**2, a*c, b**2, b*c, c**2]

        > monomials(['a', 'b', 'c'], 2, is_homogeneous=True)

            [a*b, b**2, c**2, b*c, a**2, a*c]
    """
    result = set() if is_homogeneous else {S.One}
    variables = [symbols(x) if isinstance(x, str) else x for x in variables]

    for deg in range(1, 1 + degree):
        for comb in combinations_with_replacement(variables, deg):
            term = Mul(*comb)
            result.add(term)

    if is_homogeneous:
        return [x for x in result if degree == Poly(x, variables).total_degree()]

    return list(result)


def generate_polynomial(monomial_list: List[Expr], coeff_name: str = 'm') -> Tuple[Poly, List[Symbol]]:
    """
        Generate a symbolic polynomial with indexed coefficients from a list of monomials.

        Example:
        > mons = monomials(['x', 'y'], 2)
        > poly = generate_polynomial(mons, 'm')

            m[6]*x + m[5]*x**2 + m[4]*y + m[3]*y**2 + m[2]*x*y + m[1]
    """
    global _coeff_index_

    coeffs = []
    poly = S.Zero
    pvars = set()
    cname = IndexedBase(coeff_name)

    for mono in monomial_list:
        coeff = cname[_coeff_index_]
        poly += coeff * mono
        coeffs.append(coeff)
        pvars.union(mono.free_symbols)
        _coeff_index_ += 1

    return Poly(poly, *pvars)


def poly_zero(poly: Poly) -> Set[Expr]:
    """Extract the set of constant terms (coefficients) from a sympy polynomial."""
    return set(poly.as_dict().values())
