import webbrowser

from util import config
from urllib import parse

def open_author_link(event):
    webbrowser.open_new(config.home_url)


def open_latex_svg_viewer(latex_code):
    encoded = parse.quote(latex_code)
    url = f"https://latex.codecogs.com/svg.image?{encoded}"
    webbrowser.open_new(url)
