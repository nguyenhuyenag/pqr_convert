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

        # Chỉ có thể tính discriminant cho đa thức Todo
        poly = Poly(expr, _x);
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
        # Sort by degree Todo
        grouped = collect(expand(expr), list(pvars))
        return grouped, None
    except Exception as e:
        return None, str(e)
