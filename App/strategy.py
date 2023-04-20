from abc import ABC, abstractmethod

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
        """ Test the strategy with long positions only and return profits. """

    
    @abstractmethod
    def test_short(self) -> int:
        """ Test the strategy with short positions only and return profits. """


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