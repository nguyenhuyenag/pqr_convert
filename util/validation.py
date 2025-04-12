import sympy as sp
from sympy import Poly


def parse_symbols(str_vars):
    variables = str_vars.split(",")
    variables = {v.strip() for v in variables if v.strip()}
    return {sp.symbols(v) for v in variables}


# Validate input polynomial and variables
def parse_input(input_poly: str, input_vars: str):
    pvars = parse_symbols(input_vars)
    if len(pvars) != 3:
        return None, None, "Please enter exactly 3 variables"

    try:
        expr = sp.sympify(input_poly)

        # Nếu pvars không có trong biểu thức đa thức
        if not pvars.issubset(expr.free_symbols):
            return None, None, f"Variables {pvars} not found in polynomial"

        factor = sp.together(expr)
        numer, denom = factor.as_numer_denom()
        return Poly(numer, *pvars), Poly(denom, *pvars), None
    except Exception as e:
        return None, f"Invalid polynomial: {e}"
