from sympy import Rational
from sympy import symbols, simplify, cos, acos, sqrt, pi, Poly


def solve_cubic_trig_expr_exact(expr):
    """
    Giải phương trình bậc ba tổng quát bằng công thức lượng giác nếu có 3 nghiệm thực.
    Trả về nghiệm chính xác dưới dạng căn, cos, v.v.
    """
    x = symbols('x')
    poly = Poly(expr, x)

    if poly.degree() != 3:
        return "Phương trình không phải bậc 3."

    # Hệ số: ax^3 + bx^2 + cx + d
    a, b, c, d = poly.all_coeffs()

    # Đổi biến x = t - b/(3a) để triệt tiêu hệ số bậc 2
    p = (3 * a * c - b ** 2) / (3 * a ** 2)
    q = (2 * b ** 3 - 9 * a * b * c + 27 * a ** 2 * d) / (27 * a ** 3)
    delta = (q / 2) ** 2 + (p / 3) ** 3

    if delta >= 0:
        return "Không có 3 nghiệm thực (delta ≥ 0), không dùng công thức lượng giác."

    r = sqrt(-p / 3)
    cos_theta = -q / (2 * r ** 3)
    theta = acos(cos_theta)

    # Nghiệm ẩn phụ t
    t_roots = [
        simplify(2 * r * cos((theta + 2 * k * pi) / 3)) for k in range(3)
    ]

    # Đổi biến lại về x
    shift = b / (3 * a)
    x_roots = [simplify(t - shift) for t in t_roots]

    return x_roots


x = symbols('x')
# expr = x ** 3 - x ** 2 + x / 12 + Rational(1, 216)
expr = x ** 3 - 3 * x + 1

roots = solve_cubic_trig_expr_exact(expr)
for i, r in enumerate(roots):
    print(f"x{i + 1} =", r)
