

# monomials(['p', 'q', 'r'], 2) = [1, p, q, r, q*r, r**2, p**2, q**2, p*q, p*r]
# def monomials(variables, n: int):
#     terms = set()
#     variables = symbols(variables)
#     poly = expand((1 + sum(variables)) ** n)  # (1 + a + b + c + ...)^n
#
#     for item in poly.as_ordered_terms():
#         # 2*p*q = (2, p*q)
#         coeff, term = item.as_independent(*variables, as_Add=False)
#         terms.add(term)
#
#     return list(terms)

# def poly_zero(poly: Poly):
#     eqs = set()
#     eqs_vars = set()
#
#     for coeff in poly.as_dict().values():
#         eqs.add(Eq(coeff, 0))  # coeff = 0
#         if isinstance(coeff, Symbol):
#             eqs_vars.add(coeff)
#         else:
#             eqs_vars.update(coeff.free_symbols)
#
#     return eqs, sorted(eqs_vars, key=str)

#############################################

# def pqr(expr):
#     # expr = 'a**2+b**2+c**2+k*(a*b+b*c+c*a)'
#     f = Poly(expr)
#     deg = f.total_degree()
#     # F = '_m1*p**2 + _m2*q'
#     F1 = generate_pqr(deg)
#     # print(F1.domain)
#     F = F1 + generate_pqr(deg, inext=len(F1.domain) + 1)
#
#     # Substitute symmetric polynomial definitions
#     F_subs = Poly(F.as_expr(), a, b, c, p, q, r).subs({
#         p: a + b + c,
#         q: a * b + b * c + c * a,
#         r: a * b * c
#     })
#     diff = Poly(f, a, b, c) - Poly(F_subs.__str__(), a, b, c)
#     eq, eq_vars = poly_zero(diff)
#     eq_vars = [_ for _ in eq_vars if str(_).startswith(gvar)]
#     root = solve(eq, eq_vars)
#     if root:
#         # print(root)
#         out = Poly(F, *eq_vars).subs(root)
#         print(out.as_expr())
#     else:
#         print('Not found')


# _test()
# F = createPqr(deg=2, var='m')
# print(F.as_expr())
# f = 'a**2+b**2+c**2+k*(a*b+b*c+c*a)'
# pqr(f)

# result = monomials(['p', 'q', 'r'], 2)
# print(result)
# print(create_pqr(deg=2, cvar='m').as_expr())

# f = Poly('(a+b+c)^2 + k', a, b, c)
# F = Poly('(m1+m2+m3)*(a^2+b^2+c^2)+m4*(a*b+b*c+c*a) + m2', a, b, c)
# res = poly_zero(F - f)
# print(res)
# s = solve(res[0], res[1])
# print(s)
