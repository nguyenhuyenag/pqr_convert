from sympy import symbols, sympify

# Define symbols
p, q, r, a, b, c = symbols('p q r a b c')

# Original polynomial as string
f = '-4*p**3*r + p**2*q**2 + 18*p*q*r - 4*q**3 - 27*r**2'

# Convert string to sympy expression
f = sympify(f)

# Substitute expressions
f = f.subs({p: a + b + c, q: a * b + b * c + c * a, r: a * b * c})

# Output result
print(f)

print(f.factor())
