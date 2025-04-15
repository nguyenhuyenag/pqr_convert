# import io
# import threading
# import time
# import tkinter as tk
# from tkinter import ttk, scrolledtext
#
# import matplotlib.pyplot as plt
# from PIL import Image, ImageTk
# from sympy import simplify, latex
#
# from core.pqr import pqr
# from core.uvw import uvw
# from util.app_utils import open_author_link
# from util.multithreading import run_parallel_on_fraction
# from util.tooltip import ToolTip
# from util.validation import parse_input
#
#
# # Get data from the Variables box
# def get_variables():
#     return input_vars.get().strip() or ''
#
#
# # Get data from the Input box
# def get_polynomial():
#     return input_poly.get(1.0, tk.END).strip() or ''
#
#
# # Output setter
# def set_output(data):
#     output_text.delete(1.0, tk.END)
#
#     if format_as_latex.get():
#         output_text.pack_forget()
#         output_canvas.pack(fill=tk.BOTH, expand=True)
#
#         try:
#             fig, ax = plt.subplots(figsize=(8, 1))
#             ax.axis('off')
#             ax.text(0.5, 0.5, f"${latex(data)}$", fontsize=14, ha='center', va='center')
#
#             buf = io.BytesIO()
#             plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
#             plt.close(fig)
#             buf.seek(0)
#
#             image = Image.open(buf)
#             photo = ImageTk.PhotoImage(image)
#             output_canvas.config(image=photo)
#             output_canvas.image = photo  # Keep reference!
#         except Exception as e:
#             output_canvas.config(image='')
#             output_text.pack(fill=tk.BOTH, expand=True)
#             output_text.insert(tk.END, f"LaTeX rendering error:\n{e}")
#     else:
#         output_canvas.pack_forget()
#         output_text.pack(fill=tk.BOTH, expand=True)
#         output_canvas.config(image='')
#         output_text.insert(tk.END, str(data))
#
#
# # Clear input
# def clear_input():
#     input_poly.delete('1.0', tk.END)
#
#
# def handle_btn_click(func):
#     ipoly = get_polynomial()
#     ivars = get_variables()
#     try:
#         start_time = time.time()
#
#         numer, denom, error_message = parse_input(ipoly, ivars)
#         if error_message:
#             set_output(error_message)
#             time_label.config(text="⏱ Time: --")
#             return
#
#         numer, denom, error_message = run_parallel_on_fraction(func, numer, denom)
#         if error_message:
#             set_output(error_message)
#             time_label.config(text="⏱ Time: --")
#             return
#
#         res = simplify(numer.as_expr() / denom.as_expr())
#         set_output(res)
#
#         elapsed_time = time.time() - start_time
#         time_label.config(text=f"⏱ Time: {elapsed_time:.4f} s")
#     except Exception as e:
#         set_output(f"Error: {e}")
#         time_label.config(text="⏱ Time: --")
#
#
# def btn_pqr():
#     handle_btn_click(pqr)
#
#
# def btn_uvw():
#     handle_btn_click(uvw)
#
#
# # Loading wrapper
# def run_with_loading(task_func):
#     def wrapper():
#         output_text.delete('1.0', tk.END)
#         output_text.insert(tk.END, "Processing...")
#
#         def thread_target():
#             try:
#                 task_func()
#             except Exception as e:
#                 output_text.delete('1.0', tk.END)
#                 output_text.insert(tk.END, f"Error: {e}")
#
#         threading.Thread(target=thread_target).start()
#
#     return wrapper
#
#
# #############################################
# # Create the main window
# #############################################
# root = tk.Tk()
# root.title("PQR Convert")
# root.geometry("900x600")
#
# # Font size
# custom_font = ('Consolas', 11)
#
# # Main container
# main_frame = ttk.Frame(root)
# main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
#
# # ================= Left side ================= #
# left_frame = ttk.Frame(main_frame)
# left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#
# variables_frame = ttk.Frame(left_frame)
# variables_frame.pack(fill=tk.X, pady=(0, 10))
#
# # Label + Tooltip
# var_label_frame = ttk.Frame(variables_frame)
# var_label_frame.pack(fill=tk.X)
# ttk.Label(var_label_frame, text="Variables:").pack(side=tk.LEFT)
#
# tooltip_label = ttk.Label(var_label_frame, text="(?)", foreground="blue")
# tooltip_label.pack(side=tk.LEFT, padx=(5, 0))
# ToolTip(tooltip_label, text="If the polynomial to be converted is f(a,b,c), then please input a,b,c.")
#
# input_vars = ttk.Entry(variables_frame, font=custom_font)
# input_vars.pack(fill=tk.X)
# input_vars.insert(0, 'a,b,c')
#
# ttk.Label(left_frame, text="Input:").pack(anchor=tk.W)
# input_poly = scrolledtext.ScrolledText(left_frame, height=8, wrap=tk.WORD, font=custom_font)
# input_poly.pack(fill=tk.BOTH, expand=True, pady=5)
# input_poly.insert(tk.END, '(a^2 + b^2 + c^2)^2 - k*(a^3*b + b^3*c + c^3*a)')
#
# # Frame chứa label Output và checkbox LaTeX
# output_label_frame = ttk.Frame(left_frame)
# output_label_frame.pack(fill=tk.X, pady=(0, 5))
# ttk.Label(output_label_frame, text="Output:").pack(side=tk.LEFT)
#
# format_as_latex = tk.BooleanVar(value=True)
# latex_checkbox = ttk.Checkbutton(
#     output_label_frame,
#     text="Display as LaTeX",
#     variable=format_as_latex,
#     cursor="hand2"
# )
# latex_checkbox.pack(side=tk.RIGHT)
#
# # Output widgets
# output_text = scrolledtext.ScrolledText(left_frame, height=8, wrap=tk.WORD, font=custom_font)
# output_canvas = tk.Label(left_frame, background="white")
#
# # Initial output display
# if format_as_latex.get():
#     output_canvas.pack(fill=tk.BOTH, expand=True)
# else:
#     output_text.pack(fill=tk.BOTH, expand=True)
#
# # Separator
# separator = ttk.Separator(main_frame, orient=tk.VERTICAL)
# separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)
#
# # ================= Right side ================= #
# right_frame = ttk.Frame(main_frame, width=120)
# right_frame.pack(side=tk.LEFT, fill=tk.Y)
#
# buttons = [
#     ("pqr", run_with_loading(btn_pqr)),
#     ("uvw", run_with_loading(btn_uvw)),
#     ("Clear input", clear_input)
# ]
#
# for text, cmd in buttons:
#     btn = ttk.Button(
#         right_frame,
#         text=text,
#         width=20,
#         command=cmd,
#         cursor="hand2"
#     )
#     btn.pack(pady=8, ipady=5)
#
# # Time label
# time_label = ttk.Label(right_frame, text="⏱ Time: --", font=('Consolas', 10))
# time_label.pack(pady=(20, 0))
#
# # Author label
# author_label = ttk.Label(
#     left_frame,
#     text="@nguyenhuyenag",
#     font=('Consolas', 10),
#     anchor='w',
#     cursor="hand2",
#     foreground="blue"
# )
# author_label.pack(fill=tk.X, pady=(5, 0))
# author_label.bind("<Button-1>", open_author_link)
#
# if __name__ == "__main__":
#     root.mainloop()
