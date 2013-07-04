import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

import ts_charting.styler as cstyler
from ts_charting.formatter import TimestampFormatter

class Figure(object):
    def __init__(self, rows=1, cols=1, skip_na=True):
        self.figure = plt.figure()
        self.rows = rows
        self.cols = cols
        self.ax = None
        self.axnum = None
        self.graphers = {}
        self.grapher = None
        self.skip_na = skip_na
        if rows == 1:
            self.set_ax(1)

    def get_ax(self, axnum):
        if axnum not in self.graphers:
            return None
        return self.graphers[axnum].ax

    def _set_ax(self, axnum):
        self.axnum = axnum
        grapher = self.graphers[axnum]
        self.grapher = grapher
        self.ax = grapher.ax

    def init_ax(self, axnum, sharex=None, skip_na=None):
        if skip_na is None:
            skip_na = self.skip_na
        shared_df = None
        if type(sharex) == int:
            shared_df = self.graphers[sharex].df
        ax = plt.subplot(self.rows, self.cols, axnum)
        self.graphers[axnum] = Grapher(ax, skip_na, sharex=shared_df) 

    def set_ax(self, axnum, sharex=None, skip_na=None):
        if self.get_ax(axnum) is None:
            self.init_ax(axnum, sharex, skip_na)
        self._set_ax(axnum)

    def align_xlim(self, axes=None):
        """
            Make sure the axes line up their xlims
        """
        # TODO take a param of ax numbers to align
        left = []
        right = []
        for grapher in self.graphers.values():
            if grapher.df is None:
                continue
            l, r = grapher.ax.get_xlim()
            left.append(l)
            right.append(r)

        for grapher in self.graphers.values():
            if grapher.df is None:
                continue
            grapher.ax.set_xlim(min(left), max(right)) 

    def plot(self, name, series, index=None, fillna=None, **kwargs):
        if self.ax is None:
            print('NO AX set')
            return
        self.figure.autofmt_xdate()
        self.grapher.plot(name, series, index, fillna, **kwargs)

    def plot_markers(self, name, series, yvalues=None, xindex=None, **kwargs):
        if self.ax is None:
            print('NO AX set')
            return
        self.grapher.plot_markers(name, series, yvalues, xindex, **kwargs)

    def clear(self, axnum=None):
        if axnum is None:
            axnum = self.axnum

        grapher = self.graphers[axnum]
        ax = grapher.ax
        ax.clear()
        del self.graphers[axnum]
        self.ax = None
        self.set_ax(axnum)

class Grapher(object):
    def __init__(self, ax, skip_na=True, sharex=None):
        self.df = None
        self.formatter = None
        self.ax = ax
        self.skip_na = skip_na
        self.sharex = sharex
        self.styler = cstyler.styler()
        self.yaxes = {}

    @property
    def right_ax(self):
        return self.yaxes.get('right', None)

    def is_datetime(self):
        return self.df.index.inferred_type in ('datetime', 'date', 'datetime64')

    def find_ax(self, secondary_y, kwargs):
        """
        multiple y-axis support. stay backward compatible with secondary_y
        
        Note: we take in the actual kwargs because we want to pop('yax')
        to affect the callers kwargs
        """
        yax = kwargs.pop('yax', None)
        if yax and secondary_y:
            raise Exception('yax and secondary_y should not both be set')
        if secondary_y:
            yax = 'right'

        ax = self.ax
        if yax:
            ax = self.get_yax(yax)
        return ax

    def plot(self, name, series, index=None, fillna=None, secondary_y=False, 
             **kwargs):

        # use default styler if one is not passed in
        styler = kwargs.pop('styler', self.styler)
        if styler:
            style_dict = next(styler)
            # note we do it this way so explicit args passed in kwargs
            # override style_dict
            kwargs = dict(style_dict.items() + kwargs.items())

        if self.sharex is not None:
            series = series.reindex(self.sharex.index, method=fillna)

        if self.df is None:
            self.df = pd.DataFrame(index=series.index)
        
        is_datetime = self.is_datetime()
        if is_datetime:
            self.setup_datetime(self.df.index)

        # Previous we were using DataFrame.setitem to implicitly reindex
        # and then fillna later. This only works if the original series
        # has items that line up in the Grapher.df
        # We now reindex and fillna in one step. 
        # Ran into this when plotting daily data that had no normalized (midnight)
        # times. 
        if not np.isscalar(series):
            series = series.reindex(self.df.index, method=fillna)
        self.df[name] = series

        plot_series = self.df[name]

        if name is not None:
            kwargs['label'] = name

        xax = self.df[name].index
        if self.skip_na and is_datetime:
            xax = np.arange(len(self.df))
            self.formatter.index = self.df.index
        
        ax = self.find_ax(secondary_y, kwargs)
        ax.plot(xax, plot_series, **kwargs)

        # generate combined legend
        lines, labels = self.consolidate_legend()
        self.ax.legend(lines, labels, loc=0)

        if is_datetime: 
            # plot empty space for leading NaN and trailing NaN
            # not sure if I should only call this for is_datetime
            plt.xlim(0, len(self.df.index)-1)

    def consolidate_legend(self):
        """
        consolidate the legends from all axes and merge into one
        """
        lines, labels = self.ax.get_legend_handles_labels()
        for k, ax in self.yaxes.iteritems():
            new_lines, new_labels = ax.get_legend_handles_labels()
            lines = lines + new_lines
            labels = labels + new_labels
        return lines, labels

    def get_right_ax(self):
        return self.get_yax('right')

    def get_yax(self, name):
        """
        Get a yaxis keyed by name. Returns a newly
        generted twinx if it doesn't exist
        """
        def make_patch_spines_invisible(ax):
            ax.set_frame_on(True)
            ax.patch.set_visible(False)
            for sp in ax.spines.itervalues():
                sp.set_visible(False)

        size = len(self.yaxes)
        if name not in self.yaxes:
            ax = self.ax.twinx()
            self.yaxes[name] = ax
            # set spine 
            ax.spines["right"].set_position(("outward", 50 * size))    
            make_patch_spines_invisible(ax)
            ax.spines["right"].set_visible(True)
            ax.set_ylabel(name)

            self.set_formatter()
        return self.yaxes[name]

    def setup_datetime(self, index):
        """
            Setup the int based matplotlib x-index to translate
            to datetime

            Separated out here to share between plot and candlestick
        """
        is_datetime = self.is_datetime()
        if self.formatter is None and self.skip_na and is_datetime:
            self.formatter = TimestampFormatter(index)
            self.formatter.set_formatter(self.ax)

    def set_index(self, index):
        if self.df is not None:
            raise Exception("Cannot set index if df already exists")
        df = pd.DataFrame(index=index)
        self.df = df

    def set_formatter(self):
        """ quick call to reset locator/formatter when lost. i.e. boxplot """
        if self.formatter:
            self.formatter.set_formatter(self.ax)

    def add_data(self, data):
        if self.df is None:
            self.df = data
        else: 
            # merge ohlc data
            for k,v in data.iterkv():
                self.df[k] = v

    def plot_markers(self, name, series, yvalues=None, xindex=None, **kwargs):
        if yvalues is not None:
            series = process_signal(series, yvalues)
        props = {}
        props['linestyle'] = 'None'
        props['marker'] = 'o'
        props['markersize'] = 10
        props.update(kwargs)

        if xindex is not None:
            series = series.copy()
            series.index = xindex

        self.plot(name, series, **props)

    def plot_surface(self, df, *args, **kwargs):
        pass

def process_signal(series, source):
    """
        Take any non 0/na value and changes it to corresponding value of source
    """
    temp = series.astype(float).copy()
    temp[temp == 0] = None
    temp, source = temp.align(source, join='left')
    temp *= source
    return temp
