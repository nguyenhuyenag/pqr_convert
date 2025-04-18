import webbrowser

from util import config
from urllib import parse

from util.config import latex_view


def open_author_link():
    webbrowser.open_new(config.home_url)


def open_latex_svg_viewer(latex_code: str):
    if not latex_code:
        return

    encoded = parse.quote(latex_code)
    # url = f"{latex_view}?{encoded}"
    webbrowser.open_new(f'{latex_view}?{encoded}')
