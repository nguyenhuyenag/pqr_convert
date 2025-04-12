import tkinter as tk
import webbrowser
from tkinter import ttk, scrolledtext

from core.pqr import pqr
from util.tooltip import ToolTip
from util.validation import parse_input


# Hàm lấy dữ liệu từ ô Variables
def get_variables():
    return input_vars.get().strip() or ''


# Hàm lấy dữ liệu từ ô Input
def get_polynomial():
    return input_poly.get(1.0, tk.END).strip() or ''


def btn_pqr():
    ipoly = get_polynomial()
    ivars = get_variables()
    numer, denom, error_message = parse_input(ipoly, ivars)
    if error_message:
        set_output(error_message)
        return

    result, error_message = pqr(numer)
    set_output(result.as_expr() if result else error_message)


def btn_uvw():
    return None


# Hàm chèn kết quả vào ô Output
def set_output(data):
    output_text.delete(1.0, tk.END)  # Xóa nội dung cũ
    output_text.insert(tk.END, str(data))  # Chèn kết quả mới


#####################################################
# Tạo cửa sổ chính
root = tk.Tk()
root.title("PQR Convert")
root.geometry("900x600")

# Định nghĩa font với kích thước lớn hơn (vd: 12)
custom_font = ('Consolas', 11)

# Main container
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Phần TRÁI (Input/Output)
left_frame = ttk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Frame cho variables
variables_frame = ttk.Frame(left_frame)
variables_frame.pack(fill=tk.X, pady=(0, 10))

# Dòng 1: Label + Tooltip
var_label_frame = ttk.Frame(variables_frame)
var_label_frame.pack(fill=tk.X)
ttk.Label(var_label_frame, text="Variables:").pack(side=tk.LEFT)

# Tooltip
tooltip_label = ttk.Label(var_label_frame, text="(?)", foreground="blue")
tooltip_label.pack(side=tk.LEFT, padx=(5, 0))
ToolTip(tooltip_label,
        text="If there are multiple variables, enter the base variables separated by commas.\nFor example: a,b,c")

# Dòng 2: Ô nhập - Thêm font size
input_vars = ttk.Entry(variables_frame, font=custom_font)
input_vars.pack(fill=tk.X)
input_vars.insert(0, 'a,b,c')

# Ô nhập đa thức - Thêm font size
ttk.Label(left_frame, text="Input:").pack(anchor=tk.W)
input_poly = scrolledtext.ScrolledText(left_frame, height=8, wrap=tk.WORD, font=custom_font)
input_poly.pack(fill=tk.BOTH, expand=True, pady=5)
# input_poly.insert(tk.END, '(a^2 + b^2 + c^2)^2 - k*(a^3*b + b^3*c + c^3*a)')
input_poly.insert(tk.END, 'a/b+b/c+c/a-k*(a+b+c)')

# Ô kết quả - Thêm font size
ttk.Label(left_frame, text="Output:").pack(anchor=tk.W)
output_text = scrolledtext.ScrolledText(left_frame, height=8, wrap=tk.WORD, font=custom_font)
output_text.pack(fill=tk.BOTH, expand=True)

# Đường kẻ dọc phân cách
separator = ttk.Separator(main_frame, orient=tk.VERTICAL)
separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)

# Phần PHẢI (các nút chức năng)
right_frame = ttk.Frame(main_frame, width=120)
right_frame.pack(side=tk.LEFT, fill=tk.Y)


# Các nút chức năng (tạm thời dùng hàm giả định)
def dummy_command():
    print("Button clicked")


buttons = [
    ("pqr", btn_pqr),
    ("uvw", btn_uvw)
]

for text, cmd in buttons:
    btn = ttk.Button(
        right_frame,
        text=text,
        width=20,
        command=cmd,
        cursor="hand2"
    )
    btn.pack(pady=8, ipady=5)


# Thêm thông tin tác giả ở dưới cùng, bên phải
# author_label = ttk.Label(right_frame, text="@nguyenhuyenag", font=('Consolas', 10))
# author_label.pack(side=tk.BOTTOM, pady=(10, 0))

# Thêm thông tin tác giả dưới ô Output
# author_label = ttk.Label(left_frame, text="@nguyenhuyenag", font=('Consolas', 10), anchor='e')
# author_label.pack(fill=tk.X, pady=(5, 0))

# Thêm thông tin tác giả dưới ô Output (canh trái)
# author_label = ttk.Label(left_frame, text="@nguyenhuyenag", font=('Consolas', 10), anchor='w', cursor="hand2")
# author_label.pack(fill=tk.X, pady=(5, 0))

# Hàm mở URL
def open_author_link(event):
    webbrowser.open_new("https://nguyenhuyenag.wordpress.com/")


# Label có thể click mở link
author_label = ttk.Label(
    left_frame,
    text="@nguyenhuyenag",
    font=('Consolas', 10),
    anchor='w',
    cursor="hand2",
    foreground="blue"  # Tùy chọn: để giống hyperlink
)
author_label.pack(fill=tk.X, pady=(5, 0))

# Gắn sự kiện click chuột trái
author_label.bind("<Button-1>", open_author_link)

if __name__ == "__main__":
    root.mainloop()
