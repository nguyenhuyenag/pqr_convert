from sympy import Poly, symbols

from core.pqr import pqr
from util import messages


def uvw(poly: Poly):
    result, error_message = pqr(poly)
    if error_message:
        return None, error_message

    try:
        p, q, r, u, v, w = symbols("p q r u v w")
        subs = {p: 3 * u, q: 3 * v ** 2, r: w ** 3}
        return result.subs(subs), None
    except Exception as e:
        # print('Exception:', str(e))
        return None, messages.conversion_error
