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
    if CURRENT_FIGURE is None or reset:
        CURRENT_FIGURE = Figure(1)
    return CURRENT_FIGURE

def scf(figure):
    global CURRENT_FIGURE
    CURRENT_FIGURE = figure

_fplot_doc = """
    Parameters
    ----------
    secondary_y : bool
        Plot on a secondary y-axis
"""
# Monkey Patches, no good reason for this to be here...
@Appender(_fplot_doc)
def series_plot(self, label=None, *args, **kwargs):
    label = label or kwargs.get('label')
    label = label and label or self.name

    try:
        prefix = kwargs.pop('prefix')
        label = prefix +' '+label
    except:
        pass

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

def series_plot_markers(self, label=None, *args, **kwargs):
    """
    Really just an automated way of calling gcf
    """
    label = label or kwargs.get('label')
    label = label and label or self.name
    fig = gcf()
    fig.plot_markers(str(label), self, *args, **kwargs)

pd.Series.fplot_markers = series_plot_markers

def figure(*args, **kwargs):
    """ create Figure and set as current """
    fig = Figure(*args, **kwargs)
    scf(fig)
    return fig
