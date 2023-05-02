import tkinter as tk
import tkinter.messagebox as mb
from abc import ABC, abstractmethod
from styles import Theme


class BaseStrategyParameters(ABC):

    @property
    def __lower_value(self) -> tk.IntVar:
        """ The parameter's lower value (may be named as minimum, short, oversold etc). """


    @property
    def __higher_value(self) -> tk.IntVar:
        """ The parameter's higher value (may be named as maximum, long, overbought etc). This will store the value if there's only one parameter value needed. """

    
    @property
    def __strategy_name(self):
        """ The name of the strategy. """


    @abstractmethod
    def get_lower_value(self) -> int:
        """ Get the lower parameter value """


    @abstractmethod
    def get_higher_value(self) -> int:
        """ Get the higher parameter value. """



class StrategyParameters(BaseStrategyParameters):


    def __init__(self) -> None:
        self.__higher_value = tk.IntVar()
        self.__lower_value = tk.IntVar()


    def __MA_strategy_parameter_inputs(self, theme: Theme) -> None:
        """ Moving Average Crossover Strategy Parameters: Long Moving Average and Short Moving Average. """

        self.__higher_value = tk.IntVar()
        self.__lower_value = tk.IntVar()

        short_MA_frame = tk.Frame(self.__params_frame, background=theme.background)
        short_MA_frame.grid(row=0, column=0, padx=10)

        short_MA_label = tk.Label(short_MA_frame, text="Short MA:", background=theme.background, foreground=theme.foreground, font=("tkDefaultFont", 16))
        short_MA_label.grid(row=0, column=0)

        short_MA_entry = tk.Entry(
            short_MA_frame,
            textvariable=self.__lower_value,
            background=theme.background,
            foreground=theme.foreground,
            highlightbackground=theme.foreground,
            highlightthickness=1,
            insertbackground=theme.foreground,
            font=("tkDefaultFont", 14),
            width=6,
            relief="flat"
        )
        short_MA_entry.grid(row=0, column=1)

        long_MA_frame = tk.Frame(self.__params_frame, background=theme.background)
        long_MA_frame.grid(row=0, column=1, padx=10)

        long_MA_label = tk.Label(long_MA_frame, text="Long MA:", background=theme.background, foreground=theme.foreground, font=("tkDefaultFont", 16))
        long_MA_label.grid(row=0, column=0)

        long_MA_entry = tk.Entry(
            long_MA_frame,
            textvariable=self.__higher_value,
            background=theme.background,
            foreground=theme.foreground,
            highlightbackground=theme.foreground,
            highlightthickness=1,
            insertbackground=theme.foreground,
            font=("tkDefaultFont", 14),
            width=6,
            relief="flat"
        )
        long_MA_entry.grid(row=0, column=1)

        return


    def __RSI_strategy_params_inputs(self, theme: Theme) -> None:
        """ RSI Overbought/Oversold Strategy Parameters: Overbought Level and Oversold Level """

        self.__higher_value = tk.IntVar(value=None)
        self.__lower_value = tk.IntVar(value=None)

        oversold_level_frame = tk.Frame(self.__params_frame, background=theme.background)
        oversold_level_frame.grid(row=0, column=0, padx=5)

        oversold_level_label = tk.Label(oversold_level_frame, text="Oversold Level:", background=theme.background, foreground=theme.foreground, font=("tkDefaultFont", 12))
        oversold_level_label.grid(row=0, column=0)

        oversold_level_entry = tk.Entry(
            oversold_level_frame,
            textvariable=self.__lower_value,
            background=theme.background,
            foreground=theme.foreground,
            highlightbackground=theme.foreground,
            highlightthickness=1,
            insertbackground=theme.foreground,
            font=("tkDefaultFont", 14),
            width=6,
            relief="flat"
        )
        oversold_level_entry.grid(row=0, column=1)

        overbought_level_frame = tk.Frame(self.__params_frame, background=theme.background)
        overbought_level_frame.grid(row=0, column=1, padx=5)

        overbought_level_label = tk.Label(overbought_level_frame, text="Overbought Level:", background=theme.background, foreground=theme.foreground, font=("tkDefaultFont", 12))
        overbought_level_label.grid(row=0, column=0)

        overbought_level_entry = tk.Entry(
            overbought_level_frame,
            textvariable=self.__higher_value,
            background=theme.background,
            foreground=theme.foreground,
            highlightbackground=theme.foreground,
            highlightthickness=1,
            insertbackground=theme.foreground,
            font=("tkDefaultFont", 14),
            width=6,
            relief="flat"
        )
        overbought_level_entry.grid(row=0, column=1)

        return


    def __bollinger_bands_strategy_params_inputs(self) -> None:
        """ Bollinger Bands Strategy: No Parameters """
        self.__higher_value = tk.IntVar()
        self.__lower_value = tk.IntVar()


    def get_higher_value(self) -> int:
        return self.__higher_value.get()


    def get_lower_value(self) -> int:
        return self.__lower_value.get()


    def update_display(self, params_container: tk.Frame, strategy_name: str, theme: Theme) -> None:
        """ Display the new set of parameter inputs when the chosen strategy changes. """

        self.__params_frame = tk.Frame(params_container, background=theme.background)
        self.__params_frame.pack(pady=10)

        if strategy_name == "MA Crossover": self.__MA_strategy_parameter_inputs(theme)
        elif strategy_name == "RSI Overbought Oversold": self.__RSI_strategy_params_inputs(theme)            
        elif strategy_name == "Bollinger Bands": self.__bollinger_bands_strategy_params_inputs()
        else: mb.showwarning(title="Unidentified Strategy", message="This strategy does not exist here just yet. Please choose a strategy from the list.")
        return