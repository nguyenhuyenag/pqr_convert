import io

import matplotlib.pyplot as plt
from PIL import Image, ImageTk


def latex_to_img(latex_code):
    fig, ax = plt.subplots(figsize=(8, 1))
    ax.axis('off')
    ax.text(0.5, 0.5, f'${latex_code}$', fontsize=14, ha='center', va='center')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    buf.seek(0)

    image = Image.open(buf)
    image = image.resize((min(image.width, 780), image.height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)
