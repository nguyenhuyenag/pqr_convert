import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

import sympy as sp


# Hàm lấy dữ liệu từ ô Input
def get_input():
    return sp.simplify(input_poly.get(1.0, tk.END).strip())


# Hàm chèn kết quả vào ô Output
def output(poly):
    output_text.delete(1.0, tk.END)  # Xóa nội dung cũ
    output_text.insert(tk.END, str(poly))  # Chèn kết quả mới


def pqr_convert():
    try:
        poly = get_input()
        # TODO: xử lý đa thức ở đây nếu cần
        result = f"{poly}"
        output(result)
    except Exception as e:
        messagebox.showerror("Error", str(e))


def uvw_convert():
    try:
        poly = get_input()
        result = f"{poly}"
        output(result)
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Tạo cửa sổ
root = tk.Tk()
root.title("PQR Convert")
root.geometry("800x600")

# Main container (chia làm 2 phần: trái + phải)
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Phần TRÁI (Input/Output)
left_frame = ttk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Ô nhập bậc
h = 12
ttk.Label(left_frame, text="Input:").pack(anchor=tk.W)
input_poly = scrolledtext.ScrolledText(left_frame, height=h, wrap=tk.WORD)
input_poly.pack(fill=tk.X, pady=5)
input_poly.insert(tk.END, "a^2+b^2+c^2")  # default value

# Ô kết quả
ttk.Label(left_frame, text="Output:").pack(anchor=tk.W)
output_text = scrolledtext.ScrolledText(left_frame, height=15 - h, wrap=tk.WORD)
output_text.pack(fill=tk.BOTH, expand=True)

# Đường kẻ DỌC phân cách
separator = ttk.Separator(main_frame, orient=tk.VERTICAL)
separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)

# Phần PHẢI (3 nút)
right_frame = ttk.Frame(main_frame, width=100)
right_frame.pack(side=tk.LEFT, fill=tk.Y)

# Các nút xếp DỌC từ trên xuống
btn_pqr = ttk.Button(right_frame, text="pqr", width=10, command=pqr_convert)
btn_pqr.pack(pady=10)

btn_uvw = ttk.Button(right_frame, text="uvw", width=10, command=uvw_convert)
btn_uvw.pack(pady=10)

root.mainloop()
