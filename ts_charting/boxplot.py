import numpy as np
from pandas.core.series import remove_na

from ts_charting import Figure, Grapher
from ts_charting.monkey import mixin

@mixin(Figure)
class BoxPlotFigure(object):

    def boxplot(self, df, axis=0, *args, **kwargs):
        self.figure.autofmt_xdate()
        self.grapher.boxplot(df, axis=axis, *args, **kwargs)

@mixin(Grapher)
class BoxPlotGrapher(object):
    def boxplot(self, df, axis=0, secondary_y=False, *args, **kwargs):
        """
            Currently supports plotting DataFrames.

            Downside is that this only works for data that has equal columns. 
            For something like plotting groups with varying sizes, you'd
            need to use boxplot(list()). Example is creating a SeriesGroupBy.boxplot
        """
        if axis == 1:
            df = df.T
        index = df.columns 
        self.set_index(index)
        clean_values = [remove_na(x) for x in df.values.T]

        ax = self.find_ax(secondary_y, kwargs)

        # positions need to start at 0 to align with TimestampLocator
        ax.boxplot(clean_values, positions=np.arange(len(index)))
        self.setup_datetime(index)
        self.set_formatter()

    def boxplot_list(self, data, secondary_y=False, *args, **kwargs):
        pass

# TODO SeriesByGroupBy.boxplot
"""
import matplotlib.ticker as ticker

labels = []
data = []
for label, group in grouped:
        labels.append(label)
            data.append(group)
r = labels
N = len(r)
ind = np.arange(N)  # the evenly spaced plot indices
def format_date(x, pos=None):
        thisind = np.clip(int(x+0.5), 0, N-1)
            return r[thisind].strftime('%Y-%m-%d')

        fig = gcf()
        ax = gca()
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        _ = boxplot(data) 
        fig.autofmt_xdate()
"""
