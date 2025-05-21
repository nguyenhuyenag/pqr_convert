# PQR Convert

<!-- BEGIN LATEST DOWNLOAD BUTTON -->
[![Download PQR Convert](https://custom-icon-badges.demolab.com/badge/-Download-blue?style=for-the-badge&logo=download&logoColor=white "Tải về PQR Convert")](https://github.com/nguyenhuyenag/pqr_convert/releases/)
<!-- END LATEST DOWNLOAD BUTTON -->

- **Lưu ý:** Có hai phiên bản có thể sử dụng: `pqr_convert.zip` và `pqr_convert.exe`. Cả hai đều giống nhau, tuy nhiên `pqr_convert.exe` khởi động chậm hơn `pqr_convert.zip`.

## [English Version](README.en.md)

## Các tính năng chính

- `pqr/uvw`: Chuyển đổi biểu thức $f(a, b, c)$ (đối xứng, hoán vị) sang:
    + $f(p, q, r),$ với $p = a + b + c, \ q = ab + bc + ca, \ r = abc.$
    + $f(u, v, w),$ với $3u = a + b + c, \ 3u^2 = ab + bc + ca, \ w^3 = abc.$
- `Factor`: Phân tích biểu thức thành các nhân tử.
- `Expand`: Khai triển biểu thức.
- [`Discriminant`](https://en.wikipedia.org/wiki/Discriminant): Tính biệt thức của đa thức.
    + Ví dụ: Biệt thức của $(x) = ax^2+bx+c$ là $\Delta_{x}=b^2 - 4ac.$
- `Collect`: Nhóm đa thức theo biến.
    + Ví dụ: $a^2 + b^2 + c^2 + ab + bc + ca$ sẽ được nhóm lại theo $a$ như sau: $a^2 + a(b + c) + b^2 + bc + c^2$.
- `Substitute`: Tính giá trị biểu thức tại các giá trị của biến.

## Lưu ý quan trọng

- **Phép toán nhân**: Được biểu thị bằng dấu `*`.  
  Ví dụ: Biểu thức $ab + bc + ca$ sẽ được nhập dưới dạng `a*b + b*c + c*a`.

- **Phép toán lũy thừa**: Được biểu thị bằng dấu `^` hoặc `**`.  
  Ví dụ: Biểu thức $a^2 + b^2 + c^2$ có thể được nhập dưới dạng `a^2 + b^2 + c^2` hoặc `a**2 + b**2 + c**2`.
- **Phép toán chia**: Được biểu thị bằng dấu `/`.  
  Ví dụ: Biểu thức $\frac{a^2 + b^2 + c^2}{abc}$ sẽ được nhập dưới dạng `(a^2 + b^2 + c^2) / (a*b*c)`.

## Warning
- Hiện tại chương trình bị 4 cảnh báo trên [VirusTotal](https://www.virustotal.com/gui/file/d44439e4a08e59fb7f0e0daf647db1bda5485c97e842382f47b13141d306cb17), tuy nhiên mã nguồn của chương hoàn toàn sạch và an toàn.

## Giao diện

- **pqr / uvw:** Chương trình cần xác định $3$ biến số của biểu thức mới thể chuyển đổi. Ví dụ, biểu thức cần chuyển đổi là $f(a,b,c)$ thì `Variables` là `a,b,c`.
<img src='https://github.com/nguyenhuyenag/pqr_convert/blob/main/resources/pqr.png'>
<img src='https://github.com/nguyenhuyenag/pqr_convert/blob/main/resources/uvw.png'>

- **Expand:** Khai triển biểu thức.
<img src='https://github.com/nguyenhuyenag/pqr_convert/blob/main/resources/expand.png'>

- **Factor:** Phân tích đa thức thành nhân tử.
<img src='https://github.com/nguyenhuyenag/pqr_convert/blob/main/resources/factor.png'>

- **Discriminant:** Chương trình cần xác định biến số của đa thức mới có thể tính được biệt thực. Ví dụ, với đa thức cần tính biệt thức là $f(x) = ax^2 + bx + c$, thì `Variables` là `x`.
<img src='https://github.com/nguyenhuyenag/pqr_convert/blob/main/resources/discriminant.png'>

- **Collect:** Ví dụ ta cần nhóm biểu thức theo biến $x.$
<img src='https://github.com/nguyenhuyenag/pqr_convert/blob/main/resources/collect.png'>

- **Subtitute:** Ví dụ ta cần tính giá trị của $-4p^3r + p^2q^2 + 18pqr - 4q^3 - 27r^2$ với $p=a+b+c, \, q = ab+bc+ca, \, r = abc.$
<img src='https://github.com/nguyenhuyenag/pqr_convert/blob/main/resources/substitute.png'>
