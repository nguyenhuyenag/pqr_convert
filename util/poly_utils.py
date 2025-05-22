import sympy as sp
from sympy import factor, expand, Poly, collect

from util import messages
from util.validation import parse_vars


def handle_factor(input_poly: str):
    if not input_poly:
        return None, messages.missing_input

    try:
        expr = sp.sympify(input_poly)
        expr = factor(expr)
        return expr, None
    except Exception as e:
        return None, messages.invalid_input_error


def handle_expand(input_poly: str):
    if not input_poly:
        return None, messages.missing_input

    try:
        expr = sp.sympify(input_poly)
        expr = expand(expr)
        return expr, None
    except Exception as e:
        return None, messages.invalid_input_error


def handle_discriminant(input_poly: str, input_vars: str):
    if not input_poly:
        return None, messages.missing_input

    try:
        pvars = parse_vars(input_vars)
        if len(pvars) != 1:
            return None, messages.invalid_variables_for_discriminant

        _x = next(iter(pvars))
        expr = sp.sympify(input_poly)
        if not expr.is_polynomial():
            return None, messages.invalid_variables_for_discriminant

        poly = Poly(expr, _x)
        discriminant = poly.discriminant()
        return discriminant, None
    except Exception as e:
        return None, str(e)


def handle_collect(input_poly: str, input_vars: str):
    if not input_poly:
        return None, messages.missing_input

    try:
        pvars = parse_vars(input_vars)
        expr = sp.sympify(input_poly)
        f = collect(expand(expr), list(pvars))
        terms = f.as_ordered_terms()
        result = sp.Add(*map(sp.factor, terms))
        return result, None
    except Exception as e:
        return None, str(e)


def handle_substitute(expr: str, vals: str):
    try:
        subs_vals = dict()
        expr = sp.sympify(expr)
        for item in vals.split(','):
            item = item.strip()
            if not item or '=' not in item:
                continue

            lhs, rhs = item.split('=', 1)
            lhs = sp.sympify(lhs.strip())
            rhs = sp.sympify(rhs.strip())
            subs_vals[lhs] = rhs

        if subs_vals:
            expr = expr.subs(subs_vals)

        return expr, None
    except Exception as e:
        return None, str(e)
