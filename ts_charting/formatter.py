import math

import numpy as np
import pandas as pd
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
    def __init__(self, index, freq=None, xticks=None, min_ticks=5):
        """
        place ticks on the i-th data points where (i-offset)%base==0

        Parameters
        ----------
        index : DatetimeIndex
        freq : pd.Offset (optional)
            Fixed frequency
        xticks : pd.DateTimeIndex or bool array
            Either an Index of datetimes representing ticks or a boolean
            array where True denotes a tick
        min_ticks : int
            Minimum number of ticks before jumping up to a lower frequency

        """
        self.index = index
        self.min_ticks = min_ticks
        self.freq = freq
        xticks = self._init_xticks(xticks)
        self.xticks = xticks

    def _init_xticks(self, xticks):
        if xticks is None:
            return xticks

        if isinstance(xticks, (list, tuple)):
            xticks = pd.DatetimeIndex(xticks)

        if isinstance(xticks, pd.DatetimeIndex):
            xticks = pd.Series(1, index=xticks).reindex(self.index, fill_value=0)
            return xticks.astype(bool)

        if xticks.dtype == bool:
            return xticks

        raise Exception("xticks must be DatetimeIndex or bool Series")

    def __call__(self):
        'Return the locations of the ticks'
        vmin, vmax = self.axis.get_view_interval() 
        xticks = self._process(vmin, vmax)
        return self.raise_if_exceeds(xticks)

    def _process(self, vmin, vmax):
        vmin = int(math.ceil(vmin))
        vmax = int(math.floor(vmax)) or len(self.index) - 1
        vmax = min(vmax, len(self.index) -1)

        if self.xticks is None:
            xticks = self._xticks_from_freq(vmin, vmax)
        else:
            if self.xticks.dtype != bool:
                raise Exception("xticks must be a bool series")
            sub_xticks = self.xticks[vmin:vmax]
            xticks = np.where(sub_xticks)[0]
        return xticks

    def _xticks_from_freq(self, vmin, vmax):
        dmin = self.index[vmin] 
        dmax = self.index[vmax] 

        freq = self.freq
        if freq is None:
            freq = self.infer_scale(dmin, dmax)

        self.gen_freq = freq

        sub_index = self.index[vmin:vmax]
        
        xticks = self.generate_xticks(sub_index, freq)
        return xticks

    def infer_scale(self, dmin, dmax):
        delta = datetools.relativedelta(dmax, dmin)

        numYears = (delta.years * 1.0) 
        numMonths = (numYears * 12.0) + delta.months
        numDays = (numMonths * 31.0) + delta.days
        numWeeks = numDays // 7
        numHours = (numDays * 24.0) + delta.hours
        numMinutes = (numHours * 60.0) + delta.minutes
        nums = [('AS', numYears), ('MS', numMonths), ('W', numWeeks), ('D', numDays), ('H', numHours), 
                ('15min', numMinutes)] 
        freq = None
        for key, num in nums:
            if num > self.min_ticks:
                freq = key
                break

        return freq

    def generate_xticks(self, index, freq):
        """
        grab the xticks from 
        """
        binlabels = pd.Series(1, index=index).resample(freq).index
        ticks = index.get_indexer(binlabels)
        # -1 is a sentinel for out of index range
        ticks = ticks[ticks != -1]
        return ticks

class TimestampFormatter(object):
    def __init__(self, index, locator):
        self.index = index
        self.locator = locator

    def format_date(self, x, pos=None):
        thisind = np.clip(int(x+0.5), 0, len(self.index)-1)
        date = self.index[thisind]
        gen_freq = self.locator.gen_freq
        if gen_freq == 'T':
            return date.strftime('%H:%M %m/%d/%y')
        if gen_freq == 'H':
            return date.strftime('%H:%M %m/%d/%y')
        if gen_freq in ['D', 'W']:
            return date.strftime('%m/%d/%Y')
        if gen_freq in ['M', 'MS']:
            return date.strftime('%m/%d/%Y')
        return date.strftime('%m/%d/%Y %H:%M')

    @property
    def ticker_func(self):
        return ticker.FuncFormatter(self.format_date)
