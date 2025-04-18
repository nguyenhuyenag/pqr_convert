import threading
import time
import tkinter as tk
import webbrowser
from tkinter import ttk, scrolledtext
from urllib import parse

from sympy import simplify, latex

from core.pqr import pqr
from core.uvw import uvw
from util import config, messages
from util.config import TIME_DEFAULT
from util.image_utils import latex_to_img, get_icon
from util.multithreading import run_method_on_parallel
from util.poly_utils import handle_factor, handle_expand, handle_discriminant, handle_collect
from util.random import random_input
from util.validation import parse_input_for_pqr
from util.web_utils import open_author_link

COMMON_PADDING = 10

HEIGHT_INPUT = 10
HEIGHT_RAW_OUTPUT = 5
HEIGHT_TEX_OUTPUT = 5

WIDTH_FORM = 1300
HEIGHT_FORM = 700

LABEL_BOLD = ('Consolas', 11, 'bold')


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


def reset_time():
    time_label.config(text=TIME_DEFAULT)


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

    start_time = time.time()
    try:
        numer, denom, error = parse_input_for_pqr(get_input(), get_variables())
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
        reset_time()


def btn_pqr():
    handle_btn_click(pqr)


def btn_uvw():
    handle_btn_click(uvw)


def btn_factor():
    reset_time()
    clear_output()
    processing()

    result, error = handle_factor(get_input())
    set_output(error or result, bool(error))


def btn_expand():
    reset_time()
    clear_output()
    processing()

    result, error = handle_expand(get_input())
    set_output(error or result, bool(error))


def btn_discriminant():
    reset_time()
    clear_output()
    processing()

    result, error = handle_discriminant(get_input(), get_variables())
    set_output(error or result, bool(error))


def btn_collect():
    reset_time()
    clear_output()
    processing()

    result, error = handle_collect(get_input(), get_variables())
    set_output(error or result, bool(error))


# Ctrl + A chỉ phần có dữ liệu
def ctrl_a_select(event):
    event.widget.tag_remove("sel", "1.0", "end")
    event.widget.tag_add("sel", "1.0", "end-1c")
    return "break"


def build_button():
    buttons = [
        ("pqr", btn_pqr),
        ("uvw", btn_uvw),
        ("expand", btn_expand),
        ("factor", btn_factor),
        ("discriminant", btn_discriminant),
        ("collect ", btn_collect),
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


def open_latex_svg_viewer():
    latex_code = output_tex.get("1.0", tk.END).strip()
    if not latex_code:
        return

    encoded = parse.quote(latex_code)
    url = f"https://latex.codecogs.com/svg.image?{encoded}"
    webbrowser.open_new(url)


#############################################
# Create the main window
#############################################
root = tk.Tk()
root.title("PQR Convert")
root.geometry(f"{WIDTH_FORM}x{HEIGHT_FORM}")

# Set icon
root.iconphoto(False, get_icon())

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
variables_frame.pack(fill=tk.X, pady=(0, 2))

label_input_frame = ttk.Frame(variables_frame)
label_input_frame.pack(fill=tk.X, padx=5, pady=2)

# Label for variables
ttk.Label(label_input_frame, text="Variables:", font=LABEL_BOLD).grid(row=0, column=0, sticky='w')

# Input for Variables
input_vars = ttk.Entry(label_input_frame, font=('Consolas', 11), width=20)
input_vars.grid(row=0, column=1, sticky='w', padx=(10, 0))
input_vars.insert(0, 'a,b,c')

# Input expression
ttk.Label(left_frame, text="Expression / Polynomial:", font=LABEL_BOLD).pack(anchor=tk.W, pady=(2, 0), padx=5)
input_poly = scrolledtext.ScrolledText(left_frame, height=HEIGHT_INPUT, wrap=tk.WORD, font=('Consolas', 11), undo=True)
input_poly.pack(fill=tk.BOTH, expand=False, pady=(2, 0), padx=5)
input_poly.insert(tk.END, random_input())  # Default input

# Label for Output
ttk.Label(left_frame, text="Output:", font=LABEL_BOLD).pack(anchor=tk.W, pady=5)

# Output: Raw
# ttk.Label(left_frame, text="Raw").pack(anchor=tk.W)
output_raw = scrolledtext.ScrolledText(left_frame, height=HEIGHT_RAW_OUTPUT, wrap=tk.WORD, font=('Consolas', 11))
output_raw.pack(fill=tk.BOTH, expand=False, pady=(0, 5))

# Output: TEX
# ttk.Label(left_frame, text="TeX").pack(anchor=tk.W)
output_tex = scrolledtext.ScrolledText(left_frame, height=HEIGHT_TEX_OUTPUT, wrap=tk.WORD, font=('Consolas', 11))
output_tex.pack(fill=tk.BOTH, expand=False, pady=(0, 5))

# Output: LaTeX
# ttk.Label(left_frame, text="LaTeX").pack(anchor=tk.W)
# output_canvas = tk.Label(left_frame, background="white")
# output_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

view_label = tk.Label(left_frame, text="Open LaTeX preview", fg="blue", cursor="hand2", font=("Arial", 10, "underline"))
view_label.pack(anchor=tk.W)
view_label.bind("<Button-1>", lambda e: open_latex_svg_viewer())

# Output: LaTeX image
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

# Version label
version_label = ttk.Label(
    right_frame,
    text=f"Version: {config.version}",
    font=('Consolas', 10),
    anchor='center',
    foreground="gray"
)
version_label.pack(fill=tk.X, pady=(5, COMMON_PADDING))

# Add buttons
build_button()

# Time label
time_label = ttk.Label(right_frame, text=TIME_DEFAULT, font=('Consolas', 10))
time_label.pack(pady=(COMMON_PADDING, 5))

# Author label
author_label = ttk.Label(
    right_frame,
    text="@nguyenhuyenag",
    font=('Consolas', 10),
    anchor='center',
    foreground="blue",
    cursor='hand2',
)
author_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, COMMON_PADDING))

# Bind click cho author_label
author_label.bind("<Button-1>", open_author_link)

# Danh sách các widget cần Ctrl + A
text_widgets = [input_poly, output_raw, output_tex]

# Bind Ctrl + A cho tất cả widget trong danh sách
for widget in text_widgets:
    widget.bind("<Control-a>", ctrl_a_select)
    widget.bind("<Control-A>", ctrl_a_select)

#############################################
# MAIN LOOP
#############################################
if __name__ == "__main__":
    root.mainloop()
