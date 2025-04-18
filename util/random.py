import random


def random_input():
    data = [
        '(a - b)^2*(b - c)^2*(c - a)^2',
        'a/(b + c^2) + b/(c + a^2) + c/(a + b^2) - 3/2',
        '(2 + a^2)*(2 + b^2)*(2 + c^2) - 3*(a + b + c)^2',
        '4*(a + b + c)^3 - 27*(a^2*b + b^2*c + c^2*a + a*b*c)',
        '(a^2 + b^2 + c^2)^2 - k*(a^3*b + b^3*c + c^3*a)',
        '(a*b  + b*c + c*a) * (1/(a + b)^2 + 1/(b + c)^2 + 1/(c + a)^2) - 9/4',
        'a^2*(a - b)*(a - c) + b^2*(b - c)*(b - a) + c^2*(c - a)*(c - b)',
    ]
    # return data[-1]
    return random.choice(data)
