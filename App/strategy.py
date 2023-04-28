import tkinter.messagebox as mb
from abc import ABC, abstractmethod
from uuid import uuid4
import pandas as pd
import yfinance as yf

class BaseStrategy(ABC):
    """ An abstract class defining the methods needed for a strategy. """


    @property
    def __ticker(self):
        """ The Ticker """


    @property
    def __position(self):
        """ The Chosen Position """


    @property
    def __wins(self):
        """ Number of winning trades. """


    @property
    def __losses(self):
        """ Number of losing trades. """


    @property
    def __profit(self):
        """ Profit Amount. """


    @property
    def __strategy(self):
        """ The Chosen Strategy. """


    @abstractmethod
    def setup_data(self) -> pd.DataFrame:
        """ Setup the data to start the backtest. """


    @abstractmethod
    def process_backtest(self) -> None:
        """ Process the backtest with the stock's data and a chosen position type. Assumes the parameters set by the user are valid."""


    @abstractmethod
    def test_long(self) -> None:
        """ Test the strategy with long positions only. Assumes the parameters set by the user are valid. """

    
    @abstractmethod
    def test_short(self) -> None:
        """ Test the strategy with short positions only. Assumes the parameters set by the user are valid. """


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
    def get_position_type(self) -> str:
        """ Get the position type chosen for the strategy. """


    @abstractmethod
    def set_position_type(self, position: str) -> None:
        """ Set the position type chosen for the strategy. """

    
    @abstractmethod
    def get_profit(self) -> int:
        """ Get the profit amount. """


    @abstractmethod
    def set_profit(self, profit: int) -> None:
        """ Set the profit amount. """

    @abstractmethod
    def get_strategy(self) -> str:
        """ Get the strategy name """


    @abstractmethod
    def set_strategy(self, strategy: str) -> None:
        """ Set the strategy name. """


    @abstractmethod
    def calculate_win_percentage(self) -> float:
        """ Calculate the win rate for the strategy for this specific ticker. """

    
    @abstractmethod
    def check_trade_result(self, profit: int) -> None:
        """ Check if a trade was a winning trade or losing trade. Add it to the wins and losses. """



class Strategy(BaseStrategy):
    """ A base class that strategies inherit from. """


    def __init__(self, ticker: str, position: str) -> None:
        self.set_ticker(ticker)
        self.set_position_type(position)


    def setup_data(self) -> pd.DataFrame:
        return


    def process_backtest(self) -> None:
        data = self.setup_data()
        if data.empty:
            mb.showwarning(title="Internet Connection Error", message="There seems to be a problem with your network connection. Please reconnect and try again.")
            return

        self.file = open(self.get_ticker() + "_" + self.get_strategy().replace(" ", "_") + "_" + str(uuid4()) + ".csv", "w")
        self.file.write("Trade Number:,Date Open:,Date Close:,Position:,Entry Price:,Exit Price:,Trade Profit:\n")
        
        if self.get_position_type() == "Long": self.test_long(data)
        elif self.get_position_type() == "Short": self.test_short(data)
        else:
            mb.showerror(title="Position Type Not Known", message="There seems to be a problem with the specified position. Please restart the app.")
            return

        self.file.close()

        print(f"Strategy: {self.get_strategy()}")
        print("Ticker:", self.get_ticker())
        print("Position:", self.get_position_type())
        print("Profit:", self.get_profit())
        print("Wins:", self.get_wins())
        print("Losses:", self.get_losses())
        print("Winning %:", self.calculate_win_percentage())

        mb.showinfo(title="Back-Test Complete", message="The back-test has been completed. A CSV file has been saved logging all trades.")
        return


    def test_long(self) -> None:
        return


    def test_short(self) -> None:
        return


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

    def get_position_type(self) -> str:
        return self.__position


    def set_position_type(self, position: str) -> None:
        self.__position = position
        return


    def get_profit(self) -> int:
        return self.__profit


    def set_profit(self, profit: int) -> None:
        self.__profit = profit
        return


    def get_strategy(self) -> str:
        return self.__strategy


    def set_strategy(self, strategy: str) -> None:
        self.__strategy = strategy
        return


    def calculate_win_percentage(self) -> float:
        return round(self.get_wins() / (self.get_wins() + self.get_losses()), 4) * 100 if self.get_wins() != 0 else 0.0


    def check_trade_result(self, profit: int) -> int:
        if profit > 0: return 1
        else: return -1



class MovingAverageCrossoverStrategy(Strategy):
    """ Back-Test a Moving Average Crossover strategy. 
    
    A long is entered when the shorter moving average crosses up on the longer moving average.
    
    A short is entered when the shorter moving average crosses down on the longer moving average.

    The two moving average lengths must be passed in as integers. """


    def __init__(self, ticker: str, position: str, short_MA: int, long_MA: int, *args, **kwargs) -> None:
        self.set_ticker(ticker)
        self.set_position_type(position)
        self.set_strategy("MA Crossover")
        self.set_profit(0)
        self.set_wins(0)
        self.set_losses(0)

        self.__short_MA = short_MA
        self.__long_MA = long_MA


    def setup_data(self) -> pd.DataFrame:
        data = yf.Ticker(self.get_ticker()).history(period="max", interval="1d")
        if data.empty:
            return data

        data[str(self.__short_MA) + " Moving Average"] = data["Close"].rolling(self.__short_MA).mean()
        data[str(self.__long_MA) + " Moving Average"] = data['Close'].rolling(self.__long_MA).mean()
        data.dropna(inplace=True)
        return data


    def test_long(self, data: pd.DataFrame) -> None:
        position_open = False
        trade_count = 0
        date_open = ""
        date_close = ""
        entry_price = 0
        exit_price = 0
        trade_profit = 0

        for count in range(len(data)):
            if data[str(self.__long_MA) + ' Moving Average'][count] > data[str(self.__short_MA) + ' Moving Average'][count] and position_open == True:
                # Close Long Position
                date_close = data.index[count+1]
                exit_price = round(data['Open'][count+1], 2)
                trade_profit = exit_price - entry_price
                position_open = False
                self.set_profit(self.get_profit() + trade_profit)

                print("Profit:", trade_profit)
                print("Date Close:", date_close)
                print()

                self.file.write(str(trade_count) + "," + str(date_open) + "," + str(date_close) + "," + self.get_position_type() + "," + str(entry_price) + "," + str(exit_price) + "," + str(trade_profit) + "\n")

                if self.check_trade_result(trade_profit) == 1: self.set_wins(self.get_wins() + 1)
                else: self.set_losses(self.get_losses() + 1)

            elif data[str(self.__short_MA) + ' Moving Average'][count] > data[str(self.__long_MA) + ' Moving Average'][count] and position_open == False:
                # Open Long Position
                date_open = data.index[count+1]
                entry_price = round(data['Open'][count+1], 2)
                position_open = True
                trade_count += 1
                print()
                print("Trade Number:", trade_count)
                print("Date Open:", date_open)

        # Close open position if reached the last interval.
        if position_open:
            exit_price = data['Close'][count]
            trade_profit = exit_price - entry_price
            self.set_profit(self.get_profit() + (trade_profit))
            position_open = False
            
        return

    
    def test_short(self, data: pd.DataFrame) -> None:
        position_open = False
        trade_count = 0
        date_open = ""
        date_close = ""
        entry_price = 0
        exit_price = 0
        trade_profit = 0

        for count in range(len(data)):
            if data[str(self.__long_MA) + ' Moving Average'][count] > data[str(self.__short_MA) + ' Moving Average'][count] and position_open == False:
                # Open Short Position
                date_open = data.index[count+1]
                trade_count += 1
                entry_price = data['Open'][count+1]
                position_open = True

                print()
                print("Date Open:", data.index[count+1])
                print("Trade Number:", trade_count)


            elif data[str(self.__short_MA) + ' Moving Average'][count] > data[str(self.__long_MA) + ' Moving Average'][count] and position_open == True:
                # Close Short Position
                date_close = data.index[count+1]
                exit_price = data['Open'][count+1]
                trade_profit = entry_price - exit_price
                position_open = False
                self.set_profit(self.get_profit() + (trade_profit))

                print("Date Closed:", data.index[count+1])
                print("Trade Profit:", trade_profit)

                self.file.write(str(trade_count) + "," + str(date_open) + "," + str(date_close) + "," + self.get_position_type() + "," + str(entry_price) + "," + str(exit_price) + "," + str(trade_profit) + "\n")

                if self.check_trade_result(trade_profit) == 1: self.set_wins(self.get_wins() + 1)
                else: self.set_losses(self.get_losses() + 1)

        # Close open position if reached the last interval.
        if position_open:
            exit_price = data['Close'][count]
            trade_profit = entry_price - exit_price
            self.set_profit(self.get_profit() + (trade_profit))
            position_open = False

        return



class RSI_OverboughtOversoldStrategy(Strategy):
    """ Back-Test an RSI Overbought and Oversold strategy. 
    
    A long is entered when coming out of oversold level and a short is entered when coming down from an overbought level.
    
    These levels must be passed in as integers."""


    def __init__(self, ticker: str, position: str, oversold_level: int, overbought_level: int) -> None:
        self.set_ticker(ticker)
        self.set_position_type(position)
        self.set_strategy("RSI overbought/oversold")
        self.set_profit(0)
        self.set_wins(0)
        self.set_losses(0)

        self.__oversold_level = oversold_level
        self.__overbought_level = overbought_level


    def setup_data(self) -> pd.DataFrame:
        return


    def test_long(self) -> None:
        return


    def test_short(self) -> None:
        return


    
class BollingerBandsStrategy(Strategy):
    """ Back-Test a Bollinger Bands strategy.
    
    A long is entered when the price touches the lower band and a short is entered when the price touches the upper band.  """


    def __init__(self, ticker: str, position: str) -> None:
        self.set_ticker(ticker)
        self.set_position_type(position)
        self.set_strategy("Bollinger Bands")
        self.set_profit(0)
        self.set_wins(0)
        self.set_losses(0)


    def setup_data(self) -> pd.DataFrame:
        data = yf.Ticker(self.get_ticker()).history(period="max", interval="1d")
        if data.empty:
            return data

        data['20 Moving Average'] = data['Close'].rolling(20).mean()
        rate = data['Close'].rolling(20).std()
        data['Upper Band'] = data["20 Moving Average"] + (2 * rate)
        data['Lower Band'] = data["20 Moving Average"] - (2 * rate)

        data.dropna(inplace=True)
        return data


    def test_long(self, data: pd.DataFrame) -> None:
        date_open = ""
        date_close = ""
        trade_count = 0
        entry_price = 0
        exit_price = 0
        trade_profit = 0
        position_open = False

        for count in range(len(data) - 1):
            if position_open == False and data['Close'][count-1] < data['Lower Band'][count-1] and data['Close'][count] > data['Lower Band'][count]:
                # Open Long Position
                position_open = True
                entry_price = data['Open'][count+1]
                date_open = data.index[count+1]
                trade_count += 1

                print()
                print("Hit Lower Band")
                print("Entry Price:", entry_price)
                print("Date Opened:", date_open)

            elif position_open == True and data['Close'][count-1] > data['Upper Band'][count-1] and data['Close'][count] < data['Upper Band'][count]:
                # Close Long Position
                position_open = False
                exit_price = data['Open'][count+1]
                date_close = data.index[count+1]
                trade_profit = exit_price - entry_price
                self.set_profit(self.get_profit() + trade_profit)

                if trade_profit > 0: self.set_wins(self.get_wins() + 1)
                else: self.set_losses(self.get_losses() + 1)

                self.file.write(str(trade_count) + "," + str(date_open) + "," + str(date_close) + "," + self.get_position_type() + "," + str(entry_price) + "," + str(exit_price) + "," + str(trade_profit) + "\n")

                print("Hit Upper Band")
                print("Exit Price:", exit_price)
                print("Date Close", date_close)
                print("Trade Profit:", trade_profit)
                print()

        # Close last trade if it was open.
        if position_open == True:
            position_open = False
            exit_price = data['Open'][count+1]
            trade_profit = exit_price - entry_price

            if trade_profit > 0: self.set_wins(self.get_wins() + 1)
            else: self.set_losses(self.get_losses() + 1)

            print("Closing Last Trade")
            print("Exit Price:", exit_price)
            print("Trade Profit:", trade_profit)
            print()

        return


    def test_short(self, data: pd.DataFrame) -> None:
        date_open = ""
        date_close = ""
        trade_count = 0
        entry_price = 0
        exit_price = 0
        trade_profit = 0
        position_open = False

        for count in range(len(data)):
            if position_open == False and data['Close'][count-1] > data['Upper Band'][count-1] and data['Close'][count] < data['Upper Band'][count]:
                # Open Short Position
                position_open = True
                entry_price = data['Open'][count+1]
                date_open = data.index[count+1]
                trade_count += 1

                print()
                print("Hit Upper Band")
                print("Entry Price:", entry_price)
                print("Date Opened:", date_open)

            elif position_open == True and data['Close'][count-1] < data['Lower Band'][count-1] and data['Close'][count] > data['Lower Band'][count]:
                # Close Short Position
                position_open = False
                exit_price = data['Open'][count+1]
                date_close = data.index[count+1]
                trade_profit = entry_price - exit_price
                self.set_profit(self.get_profit() + trade_profit)

                if trade_profit > 0: self.set_wins(self.get_wins() + 1)
                else: self.set_losses(self.get_losses() + 1)

                self.file.write(str(trade_count) + "," + str(date_open) + "," + str(date_close) + "," + self.get_position_type() + "," + str(entry_price) + "," + str(exit_price) + "," + str(trade_profit) + "\n")

                print("Hit Lower Band")
                print("Exit Price:", exit_price)
                print("Date Close", date_close)
                print("Trade Profit:", trade_profit)
                print()


        if position_open == True:
            position_open = False
            exit_price = data['Close'][count]
            trade_profit = entry_price - exit_price

            if trade_profit > 0: self.set_wins(self.get_wins() + 1)
            else: self.set_losses(self.get_losses() + 1)

            print("Closing Last Trade")
            print("Exit Price:", exit_price)
            print("Trade Profit:", trade_profit)
            print()

        return