import io
import threading
import time
import tkinter as tk
from tkinter import ttk, scrolledtext

import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from sympy import simplify, latex

from core.pqr import pqr
from core.uvw import uvw
from util.app_utils import open_author_link
from util.multithreading import run_parallel_on_fraction
from util.validation import parse_input


# Get data from the Variables box
def get_variables():
    return input_vars.get().strip() or ''


# Get data from the Input box
def get_polynomial():
    return input_poly.get(1.0, tk.END).strip() or ''


# Output setter
def set_output(data):
    output_raw_text.delete(1.0, tk.END)
    output_latex_text.delete(1.0, tk.END)
    output_canvas.config(image='')  # Remove the current image if any
    output_canvas.image = None

    try:
        raw_code = str(data)
        latex_code = latex(data)

        # Raw code
        output_raw_text.insert(tk.END, raw_code)

        # LaTeX code
        output_latex_text.insert(tk.END, latex_code)

        # Render LaTeX image
        fig, ax = plt.subplots(figsize=(8, 1))
        ax.axis('off')
        ax.text(0.5, 0.5, f"${latex_code}$", fontsize=14, ha='center', va='center')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        buf.seek(0)

        image = Image.open(buf)
        image = image.resize((min(image.width, 780), image.height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        output_canvas.config(image=photo, height=120)
        output_canvas.image = photo

    except Exception as e:
        output_raw_text.insert(tk.END, f"LaTeX rendering error:\n{e}")


# Clear input
def clear_input():
    input_poly.delete('1.0', tk.END)


def handle_btn_click(func):
    output_raw_text.delete('1.0', tk.END)
    output_latex_text.delete('1.0', tk.END)
    output_canvas.config(image='')  # Remove the current image if any
    output_canvas.image = None
    output_raw_text.insert(tk.END, "Processing...")

    ipoly = get_polynomial()
    ivars = get_variables()

    try:
        start_time = time.time()

        numer, denom, error_message = parse_input(ipoly, ivars)
        if error_message:
            output_raw_text.delete('1.0', tk.END)
            set_output(error_message)
            time_label.config(text="⏱ Time (s): --")
            return

        numer, denom, error_message = run_parallel_on_fraction(func, numer, denom)
        if error_message:
            output_raw_text.delete('1.0', tk.END)
            set_output(error_message)
            time_label.config(text="⏱ Time (s): --")
            return

        res = simplify(numer.as_expr() / denom.as_expr())
        output_raw_text.delete('1.0', tk.END)
        set_output(res)

        elapsed_time = time.time() - start_time
        time_label.config(text=f"⏱ Time (s): {elapsed_time:.2f}")
    except Exception as e:
        output_raw_text.delete('1.0', tk.END)
        set_output(f"Error: {e}")
        time_label.config(text="⏱ Time (s): --")


def btn_pqr():
    handle_btn_click(pqr)


def btn_uvw():
    handle_btn_click(uvw)


#
# def open_author_link(event=None):
#     import webbrowser
#     webbrowser.open("https://github.com/nguyenhuyenag")


#############################################
# Create the main window
#############################################
root = tk.Tk()
root.title("PQR Convert")
root.geometry("900x700")

# Font size
custom_font = ('Consolas', 11)

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

variables_frame = ttk.Frame(left_frame)
variables_frame.pack(fill=tk.X, pady=(0, 10))

# Label for variables
var_label_frame = ttk.Frame(variables_frame)
var_label_frame.pack(fill=tk.X)
ttk.Label(var_label_frame, text="Variables:").pack(side=tk.LEFT)

# Entry for Variables with placeholder
input_vars = ttk.Entry(variables_frame, font=custom_font)
input_vars.pack(fill=tk.X)
input_vars.insert(0, 'a,b,c')  # Default placeholder text

# Input: Polynomial
ttk.Label(left_frame, text="Input:").pack(anchor=tk.W)
input_poly = scrolledtext.ScrolledText(left_frame, height=4, wrap=tk.WORD, font=custom_font, undo=True)
input_poly.pack(fill=tk.BOTH, expand=False, pady=5)
input_poly.insert(tk.END, '(a^2 + b^2 + c^2)^2 - k*(a^3*b + b^3*c + c^3*a)')

same_height = 3

# Output: Raw Python code
ttk.Label(left_frame, text="Raw Python code:").pack(anchor=tk.W)
output_raw_text = scrolledtext.ScrolledText(left_frame, height=same_height, wrap=tk.WORD, font=custom_font)
output_raw_text.pack(fill=tk.BOTH, expand=False, pady=(0, 5))

# Output: LaTeX code
ttk.Label(left_frame, text="LaTeX code:").pack(anchor=tk.W)
output_latex_text = scrolledtext.ScrolledText(left_frame, height=same_height, wrap=tk.WORD, font=custom_font)
output_latex_text.pack(fill=tk.BOTH, expand=False, pady=(0, 5))

# Output: LaTeX image
ttk.Label(left_frame, text="LaTeX display:").pack(anchor=tk.W)
output_canvas = tk.Label(left_frame, background="white", height=120)
output_canvas.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)

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

buttons = [
    ("pqr", btn_pqr),
    ("uvw", btn_uvw),
    ("Clear input", clear_input)
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

# Time label
time_label = ttk.Label(right_frame, text="⏱ Time (s): --", font=('Consolas', 10))
time_label.pack(pady=(5, 10))

# Author label just above the time label
author_label = ttk.Label(
    right_frame,
    text="@nguyenhuyenag",
    font=('Consolas', 10),
    anchor='center',
    cursor='hand2',
    foreground="blue"
)
author_label.pack(fill=tk.X, pady=(10, 5))
author_label.bind("<Button-1>", open_author_link)

#############################################
# MAIN LOOP
#############################################
if __name__ == "__main__":
    root.mainloop()
