try:
    from itertools import izip
except ImportError:
    izip = zip

import itertools
from collections import OrderedDict
from pandas.core.algorithms import factorize
import numpy as np

LINESTYLES = ('-', '--', ':')
COLORS = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
MARKERS = (None,'o', 's', 'v', '*', '^', 'x')

def styler():
    """
    Default styler that cycles colors than line-styles
    """
    styles = itertools.product(LINESTYLES, COLORS)

    # cycle through
    while True:
        yield dict(list(zip(('linestyle', 'color'), next(styles))))

def marker_styler():
    """
    Adds differing markers
    """
    styles = itertools.product(LINESTYLES, MARKERS, COLORS)

    # cycle through
    while True:
        yield dict(list(zip(('linestyle', 'marker', 'color'), next(styles))))

class StyleCategory(object):
    def __init__(self, name, values):
        self.name = name
        self.values = values

STYLES = {}
STYLES['linestyle'] = LINESTYLES
STYLES['color'] = COLORS
STYLES['marker'] = MARKERS

def level_styler(linestyle=None, color=None, marker=None):
    """
    This function is useful for categorical plotting. Based on certain categories,
    it will return styles that are persistant. 

    This is when you want to distinguish groups of line plots by their style
    """
    vars = locals().copy()

    styles = OrderedDict()

    for k, SC in list(STYLES.items()):
        vals = vars.get(k, None)
        if vals is None:
            continue
        labels, uniques = factorize(vals)
        labels = labels % len(SC) # cycle back to start
        style_values = np.take(SC, labels)
        styles[k] = style_values

    keys = list(styles.keys())
    return [dict(list(zip(keys, st))) for st in izip(*list(styles.values()))]
