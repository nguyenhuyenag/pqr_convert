import random


def random_input():
    data = [
        '(a - b)^2*(b - c)^2*(c - a)^2',
        'a/(b + c^2) + b/(c + a^2) + c/(a + b^2) - 3/2',
        '(2 + a^2)*(2 + b^2)*(2 + c^2) - 3*(a + b + c)^2',
        '4*(a + b + c)^3 - 27*(a^2*b + b^2*c + c^2*a + a*b*c)',
        '(a^2 + b^2 + c^2)^2 / (a^4 + b^4 + c^4 + k*(a^3*b + b^3*c + c^3*a))',
    ]
    return random.choice(data)
