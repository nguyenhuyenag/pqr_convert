import sympy as sp
from sympy import Poly

from util import messages


# def simplify_expression(expr):
#     return sp.simplify(expr)


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

        # if len(pvars) == 0 or len(pvars) > 3:
        #     return None, None, messages.invalid_variables
        #
        # if expr.free_symbols and len(pvars) != 3:
        #     return None, None, messages.expression_variable_count_error

        # Nếu pvars không có trong biểu thức đa thức???? Trường hợp này sẽ là hằng số
        # if expr.free_symbols and not pvars.issubset(expr.free_symbols):
        #     return None, None, messages.variable_mismatch_error

        factor = sp.together(expr)
        numer, denom = factor.as_numer_denom()
        return Poly(numer, *pvars), Poly(denom, *pvars), None
    except Exception as e:
        return None, None, messages.invalid_input_error
