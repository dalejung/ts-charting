import pandas as pd
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from pylab import plt

def grab_first_unique(index):
    """
    There are instances where you are subsetting your data and end up with a MultiIndex where
    one level is constant. This function grabs the first (and hopefully) unique level and returns it. 
    This is to you can plot a DataFrame that has the correct format but might have an extraneous index level
    """
    if isinstance(index, pd.MultiIndex):
        for i in range(index.nlevels):
            ind = index.get_level_values(i)
            if ind.is_unique:
                return ind
    return index

def _3d_values(df):
    # grab the first non-unique index
    index = grab_first_unique(df.index)
    columns = grab_first_unique(df.columns)

    X, Y = np.meshgrid(index, columns)
    Z = df.values.reshape(len(X), len(Y))
    return {'values': (X, Y, Z), 'labels': (index.name, columns.name)}

def plot_wireframe(df, ax=None, *args, **kwargs):
    if ax is None:
        fig = plt.figure()
        ax = Axes3D(fig)

    res = _3d_values(df)
    X, Y, Z = res['values']
    x_name, y_name = res['labels']

    ax.plot_wireframe(X, Y, Z, *args, **kwargs)
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    return ax
