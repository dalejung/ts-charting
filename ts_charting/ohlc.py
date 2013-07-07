from itertools import izip

import pandas as pd
import numpy as np

from matplotlib.finance import candlestick

from ts_charting import Figure, Grapher, gcf
from ts_charting.monkey import mixin

def _match_col(col, columns):
    """
    Match column name by the following process:
        1. col == 'open'
        2. col == 'Open'
        3. 'open' in col.lower()
    """
    for test in columns:
        # merged 1 and 2, assuming one won't have 'open' and 'Open'
        if col == test.lower():
            return test
        if col in test.lower():
            return test

def normalize_ohlc(df):
    """
    Return an OHLC where the column names are single word lower cased

    This is support dataframes like ones from quantmod whihc have the 
    symbol embedded in the column name. i.e. SPY.Close
    """
    cols = ['open', 'high', 'low', 'close']
    matched = []
    for col in cols:
        match = _match_col(col, df.columns)
        if match:
            matched.append(match)
            continue

        raise Exception("{col} not found".format(col=col))
    res = df.ix[:, matched]
    res.columns = cols
    return res

@mixin(Figure)
class OHLCFigure(object):
    def candlestick(self, *args, **kwargs):
        if self.ax is None:
            print('NO AX set')
            return
        self.figure.autofmt_xdate()
        self.grapher.candlestick(*args, **kwargs)

    def ohlc(self, *args, **kwargs):
        if self.ax is None:
            print('NO AX set')
            return
        self.figure.autofmt_xdate()
        self.grapher.ohlc(*args, **kwargs)

@mixin(Grapher)
class OHLCGrapher(object):

    def candlestick(self, index, open, high, low, close, width=0.3, secondary_y=False,
                   *args, **kwargs):
        """
            Takes a df and plots a candlestick. 
            Will auto search for proper columns
        """
        data = {}
        data['open'] = open
        data['high'] = high
        data['low'] = low
        data['close'] = close
        df = pd.DataFrame(data, index=index)

        if self.index is None:
            self.index = index

        # grab merged data
        xax = np.arange(len(self.index))
        quotes = izip(xax, df['open'], df['close'], df['high'], df['low'])

        ax = self.find_ax(secondary_y, kwargs)

        self.setup_datetime(index)
        candlestick(ax, quotes, width=width, colorup='g')

    def ohlc(self, df, width=0.3, *args, **kwargs):
        ohlc_df = normalize_ohlc(df)
        self.candlestick(df.index, ohlc_df.open, ohlc_df.high, ohlc_df.low, ohlc_df.close, *args, **kwargs)

def ohlc_plot(self, width=0.3, *args, **kwargs):
    fig = gcf()
    fig.ohlc(self, width=width, *args, **kwargs)
    return fig

pd.DataFrame.ohlc_plot = ohlc_plot

