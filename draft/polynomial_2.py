# from typing import List, Set, Tuple
#
# from sympy import Poly, Expr, S, IndexedBase, Symbol
#
# from core.polynomial import monomials
#
# # Biến đếm toàn cục cho hệ số
# _coeff_counter = 1
#
#
# def generate_polynomial(monomial_list: List[Expr], coeff_name: str = 'm') -> Tuple[Poly, List[Symbol]]:
#     """Tạo đa thức với hệ số duy nhất giữa các lần gọi"""
#     global _coeff_counter
#
#     m = IndexedBase(coeff_name)
#     poly = S.Zero
#     coeff_list = []
#
#     for mono in monomial_list:
#         coeff = m[_coeff_counter]
#         poly += coeff * mono
#         coeff_list.append(coeff)
#         _coeff_counter += 1  # Tăng chỉ số
#
#     # Trích xuất biến đa thức (loại bỏ hệ số)
#     pvars = set().union(*[mono.free_symbols for mono in monomial_list])
#
#     return Poly(poly, *pvars), coeff_list
#
#
# def poly_zero(poly: Poly) -> Set[Expr]:
#     """Extract coefficients from polynomial and set them to zero."""
#     return set(poly.as_dict().values())
#
#
# # Ví dụ sử dụng
# if __name__ == "__main__":
#     # Tạo đa thức 1 (bậc 1)
#     mono_list1 = monomials(['p', 'q'], degree=1)
#     poly1, coeffs1 = generate_polynomial(mono_list1)
#     print("Đa thức 1:", poly1.as_expr())
#     print("Hệ số 1:", coeffs1)
#
#     # Tạo đa thức 2 (bậc 2)
#     mono_list2 = monomials(['p', 'q'], degree=2)
#     poly2, coeffs2 = generate_polynomial(mono_list2)
#     print("\nĐa thức 2:", poly2.as_expr())
#     print("Hệ số 2:", coeffs2)
