import webbrowser

from util import config


def open_author_link(event):
    webbrowser.open_new(config.home_url)
