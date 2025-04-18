# PQR Convert

<!-- BEGIN LATEST DOWNLOAD BUTTON -->
[![Download PQR Convert](https://custom-icon-badges.demolab.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Download PQR Convert")](https://github.com/nguyenhuyenag/pqr_convert/releases/)
<!-- END LATEST DOWNLOAD BUTTON -->

## Main Features

- `pqr/uvw`: Convert expressions of the form $f(a, b, c)$ (symmetric, permutation) into:
    + $f(p, q, r),$ where $p = a + b + c, \ q = ab + bc + ca, \ r = abc.$
    + $f(u, v, w),$ where $3u = a + b + c, \ 3u^2 = ab + bc + ca, \ w^3 = abc.$
- `factor`: Factorize expressions into products.
- `expand`: Expand algebraic expressions.
- [`discriminant`](https://en.wikipedia.org/wiki/Discriminant): Compute the discriminant of a polynomial.
    + Example: The discriminant of $(x) = ax^2+bx+c$ is $\Delta_{x}=b^2 - 4ac.$
- `collect`: Group polynomial terms by variable.
    + Example: $a^2 + b^2 + c^2 + ab + bc + ca$ grouped by $a$ becomes: $a^2 + a(b + c) + b^2 + bc + c^2$.

## Important Notes

- **Variables**: If the expression is $f(a,b,c)$, then `Variables` should be `a,b,c`.
- **Multiplication**: Use the `*` symbol.  
  Example: The expression $ab + bc + ca$ should be entered as `a*b + b*c + c*a`.

- **Exponentiation**: Use `^` or `**`.  
  Example: The expression $a^2 + b^2 + c^2$ can be entered as `a^2 + b^2 + c^2` or `a**2 + b**2 + c**2`.
- **Division**: Use the `/` symbol.  
  Example: The expression $\frac{a^2 + b^2 + c^2}{abc}$ should be entered as `(a^2 + b^2 + c^2) / (a*b*c)`.

## Warning

- Currently, the program has 4 warnings on [VirusTotal](https://www.virustotal.com/gui/file/d44439e4a08e59fb7f0e0daf647db1bda5485c97e842382f47b13141d306cb17), but it is open source and does not contain malicious code. Trust me bro.

## Interface

- **pqr / uvw**
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
