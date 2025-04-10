import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

import sympy as sp

from gui.tooltip import ToolTip
from pqr.pqr_tools import pqr


# Hàm lấy dữ liệu từ ô Input
def get_input():
    return sp.simplify(input_poly.get(1.0, tk.END).strip())


def get_variables():
    """Lấy giá trị từ ô variables và trả về danh sách các biến đã được chuẩn hóa"""
    # Lấy nội dung từ ô nhập
    var_text = var_entry.get().strip()

    # Nếu ô trống, trả về danh sách mặc định
    if not var_text:
        return ['a', 'b', 'c']

    # Tách các biến bằng dấu phẩy và loại bỏ khoảng trắng thừa
    variables = [v.strip() for v in var_text.split(',')]

    # Lọc bỏ các biến rỗng (nếu có)
    variables = [v for v in variables if v]

    return variables


# Hàm chèn kết quả vào ô Output
def output(poly):
    output_text.delete(1.0, tk.END)  # Xóa nội dung cũ
    output_text.insert(tk.END, str(poly))  # Chèn kết quả mới


def pqr_convert():
    try:
        poly = get_input()
        pvars = get_variables()
        output(pqr(poly, pvars))
    except Exception as e:
        messagebox.showerror("Error", str(e))


def uvw_convert():
    try:
        poly = get_input()
        result = f"{poly}"
        output(result)
    except Exception as e:
        messagebox.showerror("Error", str(e))


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
var_entry = ttk.Entry(variables_frame, font=custom_font)
var_entry.pack(fill=tk.X)
var_entry.insert(0, 'a,b,c')

# Ô nhập đa thức - Thêm font size
ttk.Label(left_frame, text="Input:").pack(anchor=tk.W)
input_poly = scrolledtext.ScrolledText(left_frame, height=8, wrap=tk.WORD, font=custom_font)
input_poly.pack(fill=tk.BOTH, expand=True, pady=5)
input_poly.insert(tk.END, '(a^2 + b^2 + c^2)^2 - k*(a^3*b + b^3*c + c^3*a)')

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
    ("pqr", pqr_convert),
    ("uvw", dummy_command),
    ("Clear", dummy_command)
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

root.mainloop()
