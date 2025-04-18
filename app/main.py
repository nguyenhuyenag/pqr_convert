import os
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk, scrolledtext

from PIL import Image, ImageTk
from sympy import simplify, latex

from core.pqr import pqr
from core.uvw import uvw
from util import config, messages
from util.latex_utils import latex_to_img
from util.multithreading import run_method_on_parallel
from util.poly_utils import handle_factor, handle_expand, handle_discriminant, handle_collect
from util.random import random_input
from util.validation import parse_input_for_pqr
from util.web_utils import open_author_link

COMMON_PADDING = 10
RAW_OUTPUT_HEIGHT = 5
TEX_OUTPUT_HEIGHT = 3

LABEL_BOLD = ('Consolas', 11, 'bold')

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # For .exe
else:
    # For project
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


# Get data from the Variables box
def get_variables():
    return input_vars.get().strip() or ''


# Get data from the Input box
def get_input():
    return input_poly.get(1.0, tk.END).strip() or ''


def clear_output():
    output_raw.delete('1.0', tk.END)
    output_tex.delete('1.0', tk.END)
    output_canvas.config(image='')
    output_canvas.image = None


# Clear input
def clear_input():
    input_poly.delete('1.0', tk.END)


def processing():
    output_raw.insert(tk.END, "Processing...")


def set_output(data, error: bool):
    clear_output()

    # Insert raw code
    raw_code = str(data)
    output_raw.insert(tk.END, raw_code)

    if error:
        return  # Nếu có lỗi thì không in kết quả của output_raw và output_tex

    try:
        # Insert TeX code
        latex_code = latex(data)
        output_tex.insert(tk.END, latex_code)

        # Render LaTeX image
        photo = latex_to_img(latex_code)

        if photo:
            output_canvas.config(image=photo)
            output_canvas.image = photo
        else:
            output_raw.insert(tk.END, messages.error_generating_latex)

    except Exception as e:
        output_raw.insert(tk.END, messages.error_generating_latex)


def handle_btn_click(method):
    clear_output()
    processing()

    ipoly = get_input()
    ivars = get_variables()

    start_time = time.time()
    try:
        numer, denom, error = parse_input_for_pqr(ipoly, ivars)
        if error:
            set_output(error, error=True)
            return

        numer, denom, error = run_method_on_parallel(method, numer, denom)
        if error:
            set_output(error, error=True)
            return

        result = simplify(numer.as_expr() / denom.as_expr())
        set_output(result, error=False)

        elapsed = time.time() - start_time
        time_label.config(text=f"⏱ Time (s): {elapsed:.2f}")
    except Exception as e:
        set_output(f"Error: {e}", error=True)
        time_label.config(text="⏱ Time (s): --")


def btn_pqr():
    handle_btn_click(pqr)


def btn_uvw():
    handle_btn_click(uvw)


def btn_factor():
    clear_output()
    processing()

    result, error = handle_factor(get_input())
    set_output(error or result, bool(error))


def btn_expand():
    clear_output()
    processing()

    result, error = handle_expand(get_input())
    set_output(error or result, bool(error))


def btn_discriminant():
    clear_output()
    processing()

    result, error = handle_discriminant(get_input(), get_variables())
    set_output(error or result, bool(error))


def btn_group_by():
    clear_output()
    processing()

    result, error = handle_collect(get_input(), get_variables())
    set_output(result if result else error, result is None)


def build_button():
    buttons = [
        ("pqr", btn_pqr),
        ("uvw", btn_uvw),
        ("expand", btn_expand),
        ("factor", btn_factor),
        ("discriminant", btn_discriminant),
        ("collect ", btn_group_by),
        ("clear input", clear_input)
    ]

    for text, cmd in buttons:
        btn = ttk.Button(
            right_frame,
            text=text,
            width=20,
            command=lambda c=cmd: threading.Thread(target=c).start(),
            cursor="hand2"
        )
        btn.pack(pady=8, ipady=5)


#############################################
# Create the main window
#############################################
root = tk.Tk()
root.title("PQR Convert")
root.geometry("1300x700")

# Set icon
icon_path = os.path.join(base_path, 'resources', 'icon.png')
icon_image = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(False, icon_photo)

# Main container
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

#############################################
# LEFT SIDE
#############################################
left_frame = ttk.Frame(main_frame)
left_frame.grid(row=0, column=0, sticky="nsew")
main_frame.grid_columnconfigure(0, weight=3)
main_frame.grid_rowconfigure(0, weight=1)

# Frame label and input
variables_frame = ttk.Frame(left_frame)
variables_frame.pack(fill=tk.X, pady=(0, 2))  # Giảm khoảng cách phía dưới

label_input_frame = ttk.Frame(variables_frame)
label_input_frame.pack(fill=tk.X, padx=5, pady=2)  # Padding bên trái/phải

# Label for variables
ttk.Label(label_input_frame, text="Variables:", font=LABEL_BOLD).grid(row=0, column=0, sticky='w')

# Input for Variables
input_vars = ttk.Entry(label_input_frame, font=('Consolas', 11), width=20)
input_vars.grid(row=0, column=1, sticky='w', padx=(10, 0))
input_vars.insert(0, 'a,b,c')

# Input expression
ttk.Label(left_frame, text="Expression / Polynomial:", font=LABEL_BOLD).pack(
    anchor=tk.W, pady=(2, 0), padx=5)  # Thêm padx=5 để thẳng hàng với "Variables:"
input_poly = scrolledtext.ScrolledText(left_frame, height=7, wrap=tk.WORD, font=('Consolas', 11), undo=True)
input_poly.pack(fill=tk.BOTH, expand=False, pady=(2, 0), padx=5)  # Cũng thêm padx cho đồng bộ
input_poly.insert(tk.END, random_input())  # Default input

# Label for Output above the output sections
ttk.Label(left_frame, text="Output:", font=LABEL_BOLD).pack(anchor=tk.W, pady=5)

# Output: Raw Python code
ttk.Label(left_frame, text="Raw").pack(anchor=tk.W)
output_raw = scrolledtext.ScrolledText(left_frame, height=RAW_OUTPUT_HEIGHT, wrap=tk.WORD,
                                       font=('Consolas', 11))  # Use variable for height
output_raw.pack(fill=tk.BOTH, expand=False, pady=(0, 5))

# Output: LaTeX code
ttk.Label(left_frame, text="TeX").pack(anchor=tk.W)
output_tex = scrolledtext.ScrolledText(left_frame, height=TEX_OUTPUT_HEIGHT, wrap=tk.WORD,
                                       font=('Consolas', 11))
output_tex.pack(fill=tk.BOTH, expand=False, pady=(0, 5))

# Output: LaTeX image
ttk.Label(left_frame, text="LaTeX").pack(anchor=tk.W)
output_canvas = tk.Label(left_frame, background="white")
output_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

#############################################
# SEPARATOR (Vertical line between left and right side)
#############################################
separator = ttk.Separator(main_frame, orient=tk.VERTICAL)
separator.grid(row=0, column=1, sticky="ns", padx=10)

#############################################
# RIGHT SIDE
#############################################
right_frame = ttk.Frame(main_frame, width=500)
right_frame.grid(row=0, column=2, sticky="ns")
main_frame.grid_columnconfigure(2, weight=0)

# Version label placed above the buttons
version_label = ttk.Label(
    right_frame,
    text=f"Build: {config.version}",
    font=('Consolas', 10),
    anchor='center',
    foreground="gray"
)
version_label.pack(fill=tk.X, pady=(5, COMMON_PADDING))  # Đặt trên các button

# Add buttons
build_button()

# Time label
time_label = ttk.Label(right_frame, text="⏱ Time (s): --", font=('Consolas', 10))
time_label.pack(pady=(COMMON_PADDING, 5))  # Sử dụng common_padding cho khoảng cách phía trên

# Author label just above the time label
author_label = ttk.Label(
    right_frame,
    text="@nguyenhuyenag",
    font=('Consolas', 10),
    anchor='center',
    foreground="blue",
    cursor='hand2',
)
author_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, COMMON_PADDING))  # Đặt dưới cùng
author_label.bind("<Button-1>", open_author_link)

#############################################
# MAIN LOOP
#############################################
if __name__ == "__main__":
    root.mainloop()
