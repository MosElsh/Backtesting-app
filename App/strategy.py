from abc import ABC, abstractmethod
import pandas as pd

class BaseStrategy(ABC):
    """ An abstract class defining the methods needed for a strategy. """


    @property
    def __ticker(self):
        """ The Ticker """


    @property
    def __wins(self):
        """ Number of winning trades. """


    @property
    def __losses(self):
        """ Number of losing trades. """


    @abstractmethod
    def test_long(self) -> int:
        """ Test the strategy with long positions only and return profits. Assumes the parameters set by the user are valid. """

    
    @abstractmethod
    def test_short(self) -> int:
        """ Test the strategy with short positions only and return profits. Assumes the parameters set by the user are valid. """


    @abstractmethod
    def get_ticker(self) -> str:
        """ Return the Ticker for the strategy being back-tested. """


    @abstractmethod
    def set_ticker(self, ticker: str) -> None:
        """ Set the ticker that the strategy should be tested on. """


    @abstractmethod
    def get_wins(self) -> int:
        """Return the number of wins for the strategy on this symbol."""


    @abstractmethod
    def set_wins(self, wins: int) -> None:
        """ Set the number of wins for the startegy and ticker. """


    @abstractmethod
    def get_losses(self) -> int:
        """ Return the number of losing trades for the strategy on this symbol. """


    @abstractmethod
    def set_losses(self, losses: int) -> None:
        """ Set the number of losing trades for the strategy and ticker. """


    @abstractmethod
    def calculate_win_percentage(self) -> float:
        """ Calculate the win rate for the strategy for this specific ticker. """





class Strategy(BaseStrategy):
    """ A base class that strategies inherit from. """


    def __init__(self, ticker: str) -> None:
        self.set_ticker(ticker)


    def test_long(self) -> int:
        return 0


    def test_short(self) -> int:
        return 0


    def get_ticker(self) -> str:
        return self.__ticker


    def set_ticker(self, ticker: str) -> None:
        self.__ticker = ticker
        return


    def get_wins(self) -> int:
        return self.__wins


    def set_wins(self, wins: int) -> None:
        self.__wins = wins
        return


    def get_losses(self) -> int:
        return self.__losses


    def set_losses(self, losses: int) -> None:
        self.__losses = losses
        return


    def calculate_win_percentage(self) -> float:
        return round(self.get_wins() / (self.get_wins() + self.get_losses()), 2)



class MovingAverageCrossoverStrategy(Strategy):
    """ Back-Test a Moving Average Crossover strategy. 
    
    A long is entered when the shorter moving average crosses up on the longer moving average.
    
    A short is entered when the shorter moving average crosses down on the longer moving average.

    The two moving average lengths must be passed in as integers. """


    def __init__(self, ticker: str, short_MA: int, long_MA: int, *args, **kwargs) -> None:
        super().__init__(ticker)

        self.__short_MA = short_MA
        self.__long_MA = long_MA

    def test_long(self, data: pd.DataFrame) -> int:
        return 0

    
    def test_short(self) -> int:
        return 0



class RSI_OverboughtOversoldStrategy(Strategy):
    """ Back-Test an RSI Overbought and Oversold strategy. 
    
    A long is entered when coming out of oversold level and a short is entered when coming down from an overbought level.
    
    These levels must be passed in as integers."""


    def __init__(self, ticker: str, oversold_level: int, overbought_level: int) -> None:
        super().__init__(ticker)

        self.__oversold_level = oversold_level
        self.__overbought_level = overbought_level


    def test_long(self) -> int:
        return 0


    def test_short(self) -> int:
        return 0


    
class BollingerBandsStrategy(Strategy):
    """ Back-Test a Bollinger Bands strategy.
    
    A long is entered when the price touches the lower band and a short is entered when the price touches the upper band.  """


    def __init__(self, ticker: str) -> None:
        super().__init__(ticker)


    def test_long(self) -> int:
        return 0


    def test_short(self) -> int:
        return 0