import tkinter as tk
import tkinter.messagebox as mb
from styles import Theme
from strategy import *


def get_ticker_list(filename: str) -> list[str]:
    """ Retrieve all the tickers within the CSV file. """

    ticker_list = []
    file = open(filename, "r")
    for line in file:
        line = line.replace("\n", "")
        ticker_list.append(line)
    file.close()
    return ticker_list


def strategy_list() -> list[str]:
    return ["MA Crossover", "RSI overbought/oversold", "Bollinger Bands"]


def validate_positive_integer(num: int):
    """ Check that a number is of type int and larger than 0. """
    if not isinstance(num, int): return False
    return num > 0


def check_higher_lower_values_valid(lower_value: int, higher_value: int) -> bool:
    """ Check that the smaller number is smaller than the larger number. """
    return lower_value < higher_value


def process_backtest(backtest_results_container: tk.Frame, ticker: str, position: str, strategy_name: str, **kwargs) -> None:
    """ Carry out the backtest. Any strategy parameters are passed as keyword arguments. """

    if ticker == "" or position == "" or strategy_name == "": mb.showwarning(title="Empty Inputs", message="There must not be any inputs. Please fill in all the inputs.")
    elif position != "Long" and position != "Short": mb.showwarning(title="Invalid Position Chosen", message='Position must be "Long" or "Short".')
    elif ticker not in get_ticker_list("SPX Ticker List.csv"): mb.showwarning(title="Invalid Ticker", message="Please choose a valid ticker.")
    elif strategy_name not in strategy_list(): mb.showwarning(title="Invalid Strategy", message="Please choose a valid strategy.") 

    if strategy_name != "Bollinger Bands":
        if not check_higher_lower_values_valid(kwargs["lower_value"], kwargs["higher_value"]):
            mb.showwarning(title="Invalid Parameters", message="Your parameters are invalid. Please check them before submitting.")
            return

        print("Higher Value:", kwargs['higher_value'])
        print("Lower Value:", kwargs['lower_value'])

    else:
        print("Bollinger Bands!")
        
    return


def find_longest_value(data: list[str]) -> int:
    """ Find the value with the longest length in a list. """

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
    """ Switch the icon from light theme to dark theme and vice versa. Requires the label that the icon is inside. Also requires the combination of icon themes in a list. """

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

        if "activebackground" in widget.keys():
            widget.configure(activebackground=theme.foreground)

        if "activeforeground" in widget.keys():
            widget.configure(activeforeground=theme.background)
    return

        