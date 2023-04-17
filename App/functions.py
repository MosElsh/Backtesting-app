import tkinter as tk
from styles import Theme


def find_longest_value(data: list) -> int:
    highest = 0
    for value in data:
        if len(str(value)) > highest:
            highest = len(str(value))
    return highest


def list_all_widgets(widget: tk.Widget) -> list[tk.Widget]:
    """ List all widgets visible on the app recursively. """

    l = []
    for w in widget.winfo_children():
        [l.append(another_w) for another_w in list_all_widgets(w)]
        l.append(w)
    return l


def change_image_theme(image_label: tk.Label, theme: Theme, photo_image_combos: list[tk.Widget]) -> None:
    """ Switch the logo between its dark and light theme because it' an image. """

    image_to_display = photo_image_combos[0]
    if image_label.cget("image") == photo_image_combos[0].name:
        image_to_display = photo_image_combos[1]
    

    image_label.config(image=image_to_display)
    image_label.image = image_to_display
    return


def perform_theme_change(app: tk.Tk, theme: Theme) -> None:
    """ Perform a change in the theme. """

    theme.change_theme()
    widget_list = list_all_widgets(app)
    app.config(background=theme.background)
    for widget in widget_list:
        if "background" in widget.keys():
            widget.configure(background=theme.background)

        if "foreground" in widget.keys():
            widget.configure(foreground=theme.foreground)

        if "highlightbackground" in widget.keys():
            widget.configure(highlightbackground=theme.foreground)

        if "insertbackground" in widget.keys():
            widget.configure(insertbackground=theme.foreground)
    return

        