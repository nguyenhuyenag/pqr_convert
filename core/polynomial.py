from itertools import combinations_with_replacement
from typing import List, Union

import sympy as sp
from sympy import Poly, Expr, S, Mul, Symbol

# Global polynomial index
_index = 1


# Sinh các đơn thức từ danh sách các biến
def monomials(symbols: Union[List[str], List[Symbol]], degree: int, is_homogeneous: bool = False) -> List[Expr]:
    # Convert List[str] to List[Symbol]
    symbols = [sp.symbols(x) if isinstance(x, str) else x for x in symbols]

    # Initialize with 1 only for non-homogeneous case
    monomial_list = set() if is_homogeneous else {S.One}

    for deg in range(1, 1 + degree):
        for comb in combinations_with_replacement(symbols, deg):
            term = Mul(*comb)
            monomial_list.add(term)

    if is_homogeneous:
        return [x for x in monomial_list if degree == Poly(x, symbols).total_degree()]

    return list(monomial_list)


# Tạo đa thức từ danh sách các đơn thức
def generate_polynomial(monomial_list: List[Expr], coeff_name: str = 'm') -> Poly:
    global _index

    coeffs = []
    poly = S.Zero
    for mono in monomial_list:
        coeff = Symbol(f'{coeff_name}{_index}')
        poly += coeff * mono
        coeffs.append(coeff)
        _index += 1

    poly = Poly(poly)
    pvars = poly.free_symbols.difference(coeffs)

    return Poly(poly, *pvars)


# Tạo hệ phương trình với tất cả các hệ số của đa thức đều = 0
def poly_zero(poly: Poly):
    coeffs = poly.as_dict().values()
    return {coeff for coeff in coeffs}
