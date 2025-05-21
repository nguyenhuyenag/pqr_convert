# PQR Convert

<!-- BEGIN LATEST DOWNLOAD BUTTON -->
[![Download PQR Convert](https://custom-icon-badges.demolab.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Download PQR Convert")](https://github.com/nguyenhuyenag/pqr_convert/releases/)
<!-- END LATEST DOWNLOAD BUTTON -->

- **Note:** There are two available versions: `pqr_convert.zip` and `pqr_convert.exe`. Both are identical, however `pqr_convert.exe` takes longer to start than `pqr_convert.zip`.

## Main Features

- `pqr/uvw`: Convert expressions of the form $f(a, b, c)$ (symmetric, permutation) into:
    + $f(p, q, r),$ where $p = a + b + c, \ q = ab + bc + ca, \ r = abc.$
    + $f(u, v, w),$ where $3u = a + b + c, \ 3u^2 = ab + bc + ca, \ w^3 = abc.$
- `Factor`: Factorize expressions.
- `Expand`: Expand algebraic expressions.
- [`Discriminant`](https://en.wikipedia.org/wiki/Discriminant): Compute the discriminant of a polynomial.
    + Example: The discriminant of $(x) = ax^2+bx+c$ is $\Delta_{x}=b^2 - 4ac.$
- `Collect`: Group polynomial terms by variable.
    + Example: $a^2 + b^2 + c^2 + ab + bc + ca$ grouped by $a$ becomes: $a^2 + a(b + c) + b^2 + bc + c^2$.
- `Substitute`: Evaluate the expression at given variable values

## Important Notes

- **Multiplication**: Use the `*` symbol.  
  Example: The expression $ab + bc + ca$ should be entered as `a*b + b*c + c*a`.

- **Exponentiation**: Use `^` or `**`.  
  Example: The expression $a^2 + b^2 + c^2$ can be entered as `a^2 + b^2 + c^2` or `a**2 + b**2 + c**2`.
- **Division**: Use the `/` symbol.  
  Example: The expression $\frac{a^2 + b^2 + c^2}{abc}$ should be entered as `(a^2 + b^2 + c^2) / (a*b*c)`.

## Warning

- Currently, the program has 4 warnings on [VirusTotal](https://www.virustotal.com/gui/file/d44439e4a08e59fb7f0e0daf647db1bda5485c97e842382f47b13141d306cb17), however, the source code of the program is completely clean and safe.

## Interface

- **pqr / uvw:** The program needs to identify $3$ variables in the expression before it can be converted. For example, if the expression to be converted is $f(a,b,c),$ then `Variables` should be `a,b,c`.
<img src='https://github.com/nguyenhuyenag/pqr_convert/blob/main/resources/pqr.png'>
<img src='https://github.com/nguyenhuyenag/pqr_convert/blob/main/resources/uvw.png'>

- **Expand**
<img src='https://github.com/nguyenhuyenag/pqr_convert/blob/main/resources/expand.png'>

- **Factor**
<img src='https://github.com/nguyenhuyenag/pqr_convert/blob/main/resources/factor.png'>

- **Discriminant**
<img src='https://github.com/nguyenhuyenag/pqr_convert/blob/main/resources/discriminant.png'>

- **Collect**
<img src='https://github.com/nguyenhuyenag/pqr_convert/blob/main/resources/collect.png'>
