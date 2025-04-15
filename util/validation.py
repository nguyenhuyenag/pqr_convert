import sympy as sp
from sympy import Poly

from util import messages


def parse_symbols(str_vars):
    variables = str_vars.split(",")
    variables = {v.strip() for v in variables if v.strip()}
    return {sp.symbols(v) for v in variables}


# Validate input polynomial and variables
def parse_input(input_poly: str, input_vars: str):
    if not input_poly:
        return None, None, messages.expression_input_prompt

    try:
        expr = sp.sympify(input_poly)
        pvars = parse_symbols(input_vars)

        if len(pvars) != 3:
            return None, None, messages.invalid_variables

        factor = sp.together(expr)
        numer, denom = factor.as_numer_denom()
        return Poly(numer, *pvars), Poly(denom, *pvars), None
    except Exception as e:
        return None, None, messages.invalid_input_error
