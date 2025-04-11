from itertools import combinations_with_replacement
from typing import List, Union, Set, Tuple

import sympy as sp
from sympy import Poly, Expr, S, Mul, Symbol, IndexedBase

# Global polynomial index
_coeff_counter = 1


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


def generate_polynomial(monomial_list: List[Expr], coeff_name: str = 'idx') -> Tuple[Poly, List[Symbol]]:
    """Tạo đa thức với hệ số duy nhất giữa các lần gọi"""
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


# Tạo hệ phương trình với tất cả các hệ số của đa thức đều = 0
# def poly_zero(poly: Poly):
#     coeffs = poly.as_dict().values()
#     return {coeff for coeff in coeffs}
def poly_zero(poly: Poly) -> Set[Expr]:
    """Extract coefficients from polynomial and set them to zero."""
    return set(poly.as_dict().values())
