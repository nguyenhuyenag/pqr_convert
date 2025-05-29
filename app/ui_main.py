import threading
import time
import tkinter as tk
from tkinter import ttk, scrolledtext

from sympy import simplify, latex

from core.pqr import pqr
from core.uvw import uvw
from util import config, messages
from util.config import TIME_DEFAULT
from util.example import random_example
from util.image_utils import latex_to_img, get_icon
from util.multithreading import run_method_on_parallel
from util.poly_utils import handle_factor, handle_expand, handle_discriminant, handle_collect, handle_substitute
from util.validation import parse_input_for_pqr
from util.web_utils import open_author_link, open_latex_svg_viewer

COMMON_PADDING = 10
HEIGHT_INPUT = 10
HEIGHT_RAW_OUTPUT = 5
HEIGHT_TEX_OUTPUT = 5
WIDTH_FORM, HEIGHT_FORM = 1300, 700
LABEL_BOLD = ('Consolas', 10, 'bold')


def get_text_content(element):
    return element.get(1.0, tk.END).strip() or ''


# Get variables
def get_variables():
    return get_text_content(input_vars)


# Get expresstion
def get_expresstion():
    return get_text_content(input_expr)


## Get output raw tex
def get_output_tex():
    return get_text_content(output_tex)


def clear_output():
    output_raw.delete('1.0', tk.END)
    output_tex.delete('1.0', tk.END)
    output_canvas.image = None
    output_canvas.config(image='')


# Clear input
def clear_input():
    input_expr.delete('1.0', tk.END)


def reset_time():
    time_label.config(text=TIME_DEFAULT)


def processing():
    output_raw.insert(tk.END, "Processing...")


def set_output(data, error: bool):
    clear_output()

    # Insert raw code
    output_raw.insert(tk.END, str(data))

    if error:
        return  # Nếu có lỗi thì in lỗi ở ô raw, không cần xử lý tiếp

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


def handle_btn_click_for_pqr_uvw(method):
    clear_output()
    processing()

    start_time = time.time()
    try:
        numer, denom, error = parse_input_for_pqr(get_expresstion(), get_variables())
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
    handle_btn_click_for_pqr_uvw(pqr)


def btn_uvw():
    handle_btn_click_for_pqr_uvw(uvw)


def btn_factor():
    reset_time()
    clear_output()
    processing()

    result, error = handle_factor(get_expresstion())
    set_output(error or result, bool(error))


def btn_expand():
    reset_time()
    clear_output()
    processing()

    result, error = handle_expand(get_expresstion())
    set_output(error or result, bool(error))


def btn_discriminant():
    reset_time()
    clear_output()
    processing()

    result, error = handle_discriminant(get_expresstion(), get_variables())
    set_output(error or result, bool(error))


def btn_collect():
    reset_time()
    clear_output()
    processing()

    result, error = handle_collect(get_expresstion(), get_variables())
    set_output(error or result, bool(error))


def btn_substitute():
    reset_time()
    clear_output()
    processing()

    result, error = handle_substitute(get_expresstion(), get_variables())
    set_output(error or result, bool(error))


# Ctrl + A chỉ chọn phần có dữ liệu
def ctrlA_select(event):
    event.widget.tag_remove("sel", "1.0", "end")
    event.widget.tag_add("sel", "1.0", "end-1c")
    return "break"


def build_button():
    buttons = [
        ("pqr", btn_pqr),
        ("uvw", btn_uvw),
        ("substitute ", btn_substitute),
        ("discriminant", btn_discriminant),
        ("factor", btn_factor),
        ("expand", btn_expand),
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


#############################################
# Main window
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

# Variables
variables_frame = ttk.Frame(left_frame)
variables_frame.pack(fill=tk.X, pady=(0, 2))
ttk.Label(variables_frame, text="Variables / Values:", font=LABEL_BOLD).pack(anchor='w', padx=5)
input_vars = tk.Text(variables_frame, font=('Consolas', 11), undo=True, height=2)
input_vars.pack(fill=tk.X, padx=5, pady=(2, 0))
input_vars.insert('1.0', 'a,b,c')

# Expression
ttk.Label(left_frame, text="Expression:", font=LABEL_BOLD).pack(anchor=tk.W, pady=(2, 0), padx=5)
input_expr = scrolledtext.ScrolledText(left_frame, height=HEIGHT_INPUT, wrap=tk.WORD,
                                       font=('Consolas', 11), undo=True)
input_expr.pack(fill=tk.BOTH, expand=False, pady=(2, 0), padx=5)
input_expr.insert(tk.END, random_example())

# Label for Output
ttk.Label(left_frame, text="Output:", font=LABEL_BOLD).pack(anchor=tk.W, pady=5)

# Output: Raw
output_raw = scrolledtext.ScrolledText(left_frame, height=HEIGHT_RAW_OUTPUT, wrap=tk.WORD, font=('Consolas', 11))
output_raw.pack(fill=tk.BOTH, expand=False, pady=(0, 5))

# Output: TEX
output_tex = scrolledtext.ScrolledText(left_frame, height=HEIGHT_TEX_OUTPUT, wrap=tk.WORD, font=('Consolas', 11))
output_tex.pack(fill=tk.BOTH, expand=False, pady=(0, 5))

# Output: LaTeX
view_label = tk.Label(left_frame, text="Open LaTeX preview", fg="blue", cursor="hand2",
                      font=("Arial", 10, "underline"))
view_label.pack(anchor=tk.W)
view_label.bind("<Button-1>", lambda e: open_latex_svg_viewer(get_output_tex()))

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
author_label.bind("<Button-1>", lambda e: open_author_link())

# Danh sách các widget cần Ctrl + A
text_widgets = [input_expr, input_vars, output_raw, output_tex]

# Bind Ctrl + A cho tất cả widget trong danh sách
for widget in text_widgets:
    widget.bind("<Control-a>", ctrlA_select)
    widget.bind("<Control-A>", ctrlA_select)

#############################################
# MAIN LOOP
#############################################
if __name__ == "__main__":
    root.mainloop()
