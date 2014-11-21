import pandas as pd
from pandas.util.decorators import Appender

from ts_charting import Figure
import ts_charting.styler as cstyler

CURRENT_FIGURE = None

def reset_figure(*args):
    """
    In ipython notebook, clear the figure after each cell execute.
    This negates the need to specify a Figure for each plot
    """
    global CURRENT_FIGURE
    CURRENT_FIGURE = None

def gcf(reset=False):
    global CURRENT_FIGURE
    if reset:
        CURRENT_FIGURE = None
        return CURRENT_FIGURE

    if CURRENT_FIGURE is None:
        CURRENT_FIGURE = figure(1)
    return CURRENT_FIGURE

def scf(figure):
    global CURRENT_FIGURE
    CURRENT_FIGURE = figure

_fplot_doc = """
    Keyword Parameters
    ----------
    secondary_y : bool
        Plot on a secondary y-axis
    yax : string:
        named y-axis plot. 
"""
# Monkey Patches, no good reason for this to be here...
@Appender(_fplot_doc)
def series_plot(self, label=None, *args, **kwargs):
    label = plot_label(self, label, **kwargs)

    fig = gcf()
    fig.plot(str(label), self, *args, **kwargs)

pd.Series.fplot = series_plot
pd.TimeSeries.fplot = series_plot

def df_plot(self, *args, **kwargs):
    force_plot = kwargs.pop('force_plot', False)
    styler = kwargs.pop('styler', cstyler.marker_styler())

    if len(self.columns) > 20 and not force_plot:
        raise Exception("Are you crazy? Too many columns")

    # pass styler to each series plot
    kwargs['styler'] = styler
    for col in self.columns:
        series = self[col]
        series.fplot(*args, **kwargs)

pd.DataFrame.fplot = df_plot

def series_plot_markers(self, label=None, yvalues=None, *args, **kwargs):
    """
    Really just an automated way of calling gcf
    """
    fig = gcf()
    label = plot_label(self, label, **kwargs)
    fig.plot_markers(str(label), self, yvalues=yvalues, *args, **kwargs)

pd.Series.fplot_markers = series_plot_markers

def figure(*args, **kwargs):
    """ create Figure and set as current """
    kwargs['warn'] = False
    fig = Figure(*args, **kwargs)
    scf(fig)
    return fig

def plot_label(self, label=None, **kwargs):
    """
    Logic to grab plot label

    Note that this both takes label as a positional argument and a keyword. 

    This is a legacy issue where instead of grabbing label from kwargs, 
    which is how matplotlib handles it, I decided to make it a positional
    argument, under the assumption that you would almost always need a label. 

    While this is true, it makes it so I have to check check both types of 
    args.
    """
    label = label or kwargs.get('label')
    if label is None: # allow series to define non `.name` label
        label = getattr(self, 'plot_label', None)
    label = label or self.name

    prefix = kwargs.pop('prefix', None)
    if prefix:
        label = prefix +' '+label

    return label

# try to monkey patch pandas_composition
# we do this to get access to the subclass self
# get around: https://github.com/dalejung/pandas-composition/issues/19
try:
    import pandas_composition as pc
    pc.UserFrame.fplot = df_plot
    pc.UserSeries.fplot = series_plot
    pc.UserSeries.fplot_markers = series_plot_markers
except ImportError:
    pass
