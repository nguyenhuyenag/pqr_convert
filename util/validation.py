import sympy as sp
from sympy import Poly

from util import messages


def parse_vars(str_vars):
    return {sp.symbols(v.strip()) for v in str_vars.split(",") if v.strip()}


def sympify_expression(input_expr: str):
    return sp.sympify(input_expr)


# Validate input and variables
def parse_input_for_pqr(input_poly: str, input_vars: str):
    """
        Parse the input polynomial & variables for

        Returns: numerator, denominator, error_message.
    """
    if not input_vars:
        return None, None, messages.missing_variables

    if not input_poly:
        return None, None, messages.missing_input

    try:
        pvars = parse_vars(input_vars)
        if len(pvars) != 3:
            return None, None, messages.invalid_variables_pqr_uvw

        expr = sp.sympify(input_poly)
        factor = sp.together(expr)
        numer, denom = factor.as_numer_denom()
        return Poly(numer, *pvars), Poly(denom, *pvars), None
    except Exception as e:
        return None, None, messages.invalid_input_error
