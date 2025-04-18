import io
import os
import sys

import matplotlib.pyplot as plt
from PIL import Image, ImageTk

from util.config import WIDTH_OUTPUT_CANVAS


def latex_to_img(latex_code):
    plt.rcParams.update({
        "text.usetex": False,
        "mathtext.fontset": "stix",
        "font.family": "STIXGeneral"
    })
    fig, ax = plt.subplots(figsize=(9, 3))
    ax.axis('off')
    ax.text(0.5, 0.5, f'${latex_code}$', fontsize=25, ha='center', va='center')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    buf.seek(0)

    image = Image.open(buf)
    image = image.resize((min(image.width, WIDTH_OUTPUT_CANVAS), image.height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)


def get_icon():
    if hasattr(sys, "_MEIPASS"):
        icon_path = os.path.join(sys._MEIPASS, "assets", "icon.png")
    else:
        icon_path = 'assets/icon.png'
    img = Image.open(icon_path)
    return ImageTk.PhotoImage(img)
