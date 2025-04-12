import sympy as sp
from sympy import Poly


def parse_symbols(str_vars):
    variables = str_vars.split(",")
    variables = [v.strip() for v in variables if v.strip()]
    return {sp.symbols(v) for v in variables}


def parse_input_to_poly(input_poly: str, input_vars: str):
    pvars = parse_symbols(input_vars)
    if len(pvars) != 3:
        return None, "Please enter exactly 3 variables"

    poly = Poly(sp.sympify(input_poly))

    # Nếu pvars không có trong biểu thức đa thức
    if not pvars.issubset(poly.free_symbols):
        return None, f"Variables {pvars} not found in polynomial"

    poly = Poly(poly.as_expr(), *pvars)
    return poly, None
