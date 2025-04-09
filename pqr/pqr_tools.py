from sympy import solve, Eq, Symbol, expand
from sympy import symbols, Poly, S
from sympy.abc import a, b, c, p, q, r

inext = 1
gvar = '_m_'


# generateAllTerms(['p', 'q', 'r'], 2) = [q*r, r, 1, r**2, q, p**2, q**2, p*q, p, p*r]
def generate_all_terms(variables, degree: int):
    variables = symbols(variables)
    poly_expr = (1 + sum(variables)) ** degree  # (a + b + c + ... + 1)^deg
    expanded = expand(poly_expr)

    terms = set()
    for term in expanded.as_ordered_terms():
        term_without_coeff = term.as_independent(*variables, as_Add=False)[1]
        terms.add(term_without_coeff)

    return list(terms)


def create_pqr(deg: int, cvar: str = '') -> Poly:
    global inext  # Init inext where?

    if not cvar:
        cvar = gvar

    _a, _b, _c, p, q, r = symbols('_a _b _c p q r')
    poly = S.Zero  # Khởi tạo kết quả bằng 0

    for term in generate_all_terms(['p', 'q', 'r'], deg):
        F = Poly(f'{cvar}{inext}') * term
        poly += F
        inext += 1

    return Poly(poly, p, q, r)


def poly_zero(poly: Poly):
    eqs = set()
    eqs_vars = set()

    for coeff in poly.as_dict().values():
        eqs.add(Eq(coeff, 0))
        if isinstance(coeff, Symbol):
            eqs_vars.add(coeff)
        else:
            eqs_vars.update(coeff.free_symbols)

    return eqs, sorted(eqs_vars, key=str)


#############################################
# print(getAllTerms(['p', 'q', 'r'], 3))


def pqr(expr):
    # expr = 'a**2+b**2+c**2+k*(a*b+b*c+c*a)'
    f = Poly(expr)
    deg = f.total_degree()
    # F = '_m1*p**2 + _m2*q'
    F1 = create_pqr(deg)
    print(F1.domain)
    F = F1 + create_pqr(deg, inext=len(F1.domain) + 1)

    # Substitute symmetric polynomial definitions
    F_subs = Poly(F.as_expr(), a, b, c, p, q, r).subs({
        p: a + b + c,
        q: a * b + b * c + c * a,
        r: a * b * c
    })
    diff = Poly(f, a, b, c) - Poly(F_subs.__str__(), a, b, c)
    eq, eq_vars = poly_zero(diff)
    eq_vars = [_ for _ in eq_vars if str(_).startswith(gvar)]
    root = solve(eq, eq_vars)
    if root:
        # print(root)
        out = Poly(F, *eq_vars).subs(root)
        print(out.as_expr())
    else:
        print('Not found')


# =================
# _test()
# F = createPqr(deg=2, var='m')
# print(F.as_expr())
f = 'a**2+b**2+c**2+k*(a*b+b*c+c*a)'
# pqr(f)

# print(generateAllTerms(['p', 'q', 'r'], 2))
print(create_pqr(deg=2, cvar='m').as_expr())
