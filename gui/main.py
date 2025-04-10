import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

import sympy as sp

from pqr.pqr_tools import pqr


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
        output(pqr(poly))
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
import tkinter as tk
from tkinter import ttk, scrolledtext


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tip_window, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=('Arial', 10))
        label.pack()

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None


# Tạo cửa sổ chính
root = tk.Tk()
root.title("PQR Convert")
root.geometry("800x600")

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
ToolTip(tooltip_label, text="Nhập các biến, cách nhau bằng dấu phẩy\nVí dụ: a,b,c,x,y,z")

# Dòng 2: Ô nhập
var_entry = ttk.Entry(variables_frame)
var_entry.pack(fill=tk.X)
var_entry.insert(0, 'a,b,c')

# Ô nhập đa thức
ttk.Label(left_frame, text="Biểu thức đa thức:").pack(anchor=tk.W)
input_poly = scrolledtext.ScrolledText(left_frame, height=12, wrap=tk.WORD)
input_poly.pack(fill=tk.BOTH, expand=True, pady=5)
input_poly.insert(tk.END, 'a^5 + b^5 + c^5 + k*(a^4*b + b^4*c + c^4*a)')

# Ô kết quả
ttk.Label(left_frame, text="Kết quả:").pack(anchor=tk.W)
output_text = scrolledtext.ScrolledText(left_frame, height=8, wrap=tk.WORD)
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
    ("PQR", dummy_command),
    ("UVW", dummy_command),
    ("Simplify", dummy_command),
    ("Clear", dummy_command)
]

for text, cmd in buttons:
    btn = ttk.Button(right_frame, text=text, width=12, command=cmd)
    btn.pack(pady=8, ipady=5)

root.mainloop()

