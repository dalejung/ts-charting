import math

import numpy as np
import matplotlib.ticker as ticker
from pandas import datetools, DatetimeIndex
from pandas.tseries.resample import _get_range_edges
import pandas.lib as lib

class TimestampLocator(ticker.Locator):
    """  
    Place a tick on every multiple of some base number of points
    plotted, eg on every 5th point.  It is assumed that you are doing
    index plotting; ie the axis is 0, len(data).  This is mainly
    useful for x ticks.
    """
    def __init__(self, index, min_ticks=5):
        """
        place ticks on the i-th data points where (i-offset)%base==0

        Parameters
        ----------
        index : DatetimeIndex
        min_ticks : int
            Minimum number of ticks before jumping up to a lower frequency
        """
        self.index = index
        self.min_ticks = min_ticks
        self.index_type = None

    def __call__(self):
        'Return the locations of the ticks'
        vmin, vmax = self.axis.get_view_interval() 
        xticks = self._process(vmin, vmax)
        return self.raise_if_exceeds(xticks)

    def _process(self, vmin, vmax):
        vmin = int(math.ceil(vmin))
        vmax = int(math.floor(vmax)) or len(self.index) - 1
        vmax = min(vmax, len(self.index) -1)

        dmin = self.index[vmin] 
        dmax = self.index[vmax] 

        byIndex = self.infer_scale(dmin, dmax)
        self.index_type = byIndex

        sub_index = self.index[vmin:vmax]
        
        xticks = self.generate_xticks(sub_index, byIndex)
        return xticks

    def infer_scale(self, dmin, dmax):
        delta = datetools.relativedelta(dmax, dmin)

        numYears = (delta.years * 1.0) 
        numMonths = (numYears * 12.0) + delta.months
        numDays = (numMonths * 31.0) + delta.days
        numWeeks = numDays // 7
        numHours = (numDays * 24.0) + delta.hours
        numMinutes = (numHours * 60.0) + delta.minutes
        nums = [('AS', numYears), ('M', numMonths), ('W', numWeeks), ('D', numDays), ('H', numHours), 
                ('15min', numMinutes)] 
        byIndex = None
        for key, num in nums:
            if num > self.min_ticks:
                byIndex = key
                break

        return byIndex

    def generate_xticks(self, index, freq):
        """
            Ticks are really just the bin edges.
        """
        start = index[0]
        end = index[-1]
        start, end = _get_range_edges(index, offset=freq, closed='right')
        ind = DatetimeIndex(start=start, end=end, freq=freq)
        bins = lib.generate_bins_dt64(index.asi8, ind.asi8, closed='right')
        bins = np.unique(bins)
        return bins

class TimestampFormatter(object):
    def __init__(self, index):
        self.index = index
        self._locator = None

    def format_date(self, x, pos=None):
        thisind = np.clip(int(x+0.5), 0, len(self.index)-1)
        date = self.index[thisind]
        index_type = self._locator.index_type
        if index_type == 'T':
            return date.strftime('%H:%M %m/%d/%y')
        if index_type == 'H':
            return date.strftime('%H:%M %m/%d/%y')
        if index_type in ['D', 'W']:
            return date.strftime('%m/%d/%Y')
        if index_type == 'M':
            return date.strftime('%m/%d/%Y')
        return date.strftime('%m/%d/%Y %H:%M')

    def set_formatter(self, ax):
        self._locator = TimestampLocator(self.index)
        ax.xaxis.set_major_locator(self._locator)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date))
        ax.xaxis.grid(True)

