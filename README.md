# PQR Convert

<!-- BEGIN LATEST DOWNLOAD BUTTON -->
[![Download PQR Convert](https://custom-icon-badges.demolab.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Tải về PQR Convert")](https://github.com/nguyenhuyenag/pqr_convert/releases/)
<!-- END LATEST DOWNLOAD BUTTON -->

## Các tính năng chính
- `pqr/uvw`: Chuyển đổi biểu thức $f(a, b, c)$ (đối xứng, hoán vị) sang:
  + $f(p, q, r),$ với $p = a + b + c, \ q = ab + bc + ca, \ r = abc.$
  + $f(u, v, w),$ với $3u = a + b + c, \ 3u^2 = ab + bc + ca, \ w^3 = abc.$
- `factor`: Phân tích biểu thức thành các nhân tử.
- `expand`: Khai triển biểu thức.
- `discriminant`: Tính biệt thức ([discriminant](https://en.wikipedia.org/wiki/Discriminant)) của đa thức.
  + Ví dụ: Biệt thức của $(x) = ax^2+bx+c$ là $\Delta_{x}=b^2 - 4ac.$
- `collect`: Nhóm đa thức theo biến.
   + Ví dụ: $a^2 + b^2 + c^2 + ab + bc + ca$ sẽ được nhóm lại theo $a$ như sau: $a^2 + a(b + c) + b^2 + bc + c^2$.

## Lưu ý quan trọng
- **Biến số**: Giả sử biểu thức là $f(a,b,c)$ thì `Variables` là `a,b,c`.
- **Phép toán nhân**: Được biểu thị bằng dấu `*`.  
   Ví dụ: Biểu thức $ab + bc + ca$ sẽ được nhập dưới dạng `a*b + b*c + c*a`.

- **Phép toán lũy thừa**: Được biểu thị bằng dấu `^` hoặc `**`.  
   Ví dụ: Biểu thức $a^2 + b^2 + c^2$ có thể được nhập dưới dạng `a^2 + b^2 + c^2` hoặc `a**2 + b**2 + c**2`.
- **Phép toán chia**: Được biểu thị bằng dấu `/`.  
   Ví dụ: Biểu thức $\frac{a^2 + b^2 + c^2}{abc}$ sẽ được nhập dưới dạng `(a^2 + b^2 + c^2) / (a*b*c)`.

## Giao diện

![Giao diện Form](https://github.com/nguyenhuyenag/pqr_convert/blob/main/screenshots/pqr.png?raw=true)
