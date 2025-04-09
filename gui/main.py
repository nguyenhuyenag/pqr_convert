import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from sympy import symbols
from itertools import combinations_with_replacement


def get_terms(variables, max_deg):
    vars = symbols(variables)
    terms = [1]  # Hằng số 1

    for deg in range(1, max_deg + 1):
        for combo in combinations_with_replacement(vars, deg):
            term = 1
            for var in combo:
                term *= var
            terms.append(term)

    return terms


def generate_terms(vars):
    try:
        max_deg = int(input_deg.get("1.0", tk.END).strip())
        if max_deg < 0:
            raise ValueError("Bậc phải ≥ 0")

        terms = get_terms(vars, max_deg)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "\n".join(map(str, terms)))

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


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
h = 8
ttk.Label(left_frame, text="Input:").pack(anchor=tk.W)
input_deg = scrolledtext.ScrolledText(left_frame, height=h, wrap=tk.WORD)
input_deg.pack(fill=tk.X, pady=5)
input_deg.insert(tk.END, "2")  # default value

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
btn_pqr = ttk.Button(right_frame, text="pqr", width=10, command=lambda: generate_terms("p q r"))
btn_pqr.pack(pady=10)

btn_uvw = ttk.Button(right_frame, text="uvw", width=10, command=lambda: generate_terms("u v w"))
btn_uvw.pack(pady=10)

# btn_pRr = ttk.Button(right_frame, text="pRr", width=10, command=lambda: generate_terms("p R r"))
# btn_pRr.pack(pady=10)

root.mainloop()
