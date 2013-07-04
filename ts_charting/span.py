"""
Span highlighting
"""
import ts_charting as charting

def highlight_span(start=None, end=None, color='g', alpha=0.5, grapher=None):
    """
    A quick shortcut way to highlight regions of a chart. Uses the Grapher.df.index
    to translate non int-position arguments to int locations.
    """
    if start is None and end is None:
        raise Exception("strat and end cannot both be None")

    if grapher is None:
        fig = charting.gcf()
        grapher = fig.grapher
    df = grapher.df

    if not df:
        raise Exception("grapher/ax has no plots on it. Can only highlight populated ax")

    if start is None:
        start = 0
    if end is None:
        end = len(df.index) 

    # convert from object/string to pos-index
    if not isinstance(start, int):
        start = df.index.get_loc(start) 
    if not isinstance(end, int):
        end = df.index.get_loc(end) 
    
    grapher.ax.axvspan(start, end, color=color, alpha=alpha)

def hl_span_figure(self, *args, **kwargs):
    grapher = self.grapher
    kwargs['grapher'] = grapher
    return highlight_span(*args, **kwargs)

charting.Figure.hl_span = hl_span_figure
