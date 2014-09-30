from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pylab import *

def _gen_labels(labels, names=None):
    if names is None:
        names = labels.names
    if np.isscalar(labels[0]):
        labels = [(l,) for l in labels]
    zips = [list(zip(names, l)) for l in labels]
    new_labels = [', '.join(['{1}'.format(*m) for m in z]) for z in zips]
    return new_labels, names

def heatmap(data, xlabels=None, ylabels=None, title=None):
    fig, ax = plt.subplots()

    values = data.values
    cmap = plt.cm.RdYlGn
    # plot np.nan as white
    cmap.set_bad('w',1.)
    masked_array = np.ma.array(values, mask=np.isnan(values))

    heatmap = ax.pcolormesh(masked_array, cmap=cmap)
    plt.colorbar(heatmap)


    xaxis = data.columns
    yaxis = data.index
    xlabels, xnames = _gen_labels(xaxis)
    ylabels, ynames = _gen_labels(yaxis)
    ax.set_xticklabels(xlabels, minor=False)
    ax.set_yticklabels(ylabels, minor=False)

    ax.set_xlabel(xnames)
    ax.set_ylabel(ynames)

    # trying to be smart about creating ticks. 
    # previously this was to cut down on having like 1000's of labels
    if isinstance(yaxis, pd.MultiIndex):
        yaxis_labels = yaxis.labels
    else:
        yaxis_labels = [yaxis]

    for i in range(len(yaxis_labels)):
        labels, ind = np.unique(yaxis_labels[i], return_index=True)
        yticks = ind + 0.5
        if len(ind) > 1:
            break

    ax.set_xticks(np.arange(len(xaxis))+0.5, minor=False)
    ax.set_yticks(yticks, minor=False)
    plt.xticks(rotation=90)
    ax.set_xlim(0, len(xaxis))
    ax.set_ylim(0, len(yaxis))
    if title:
        ax.set_title(title)
    return ax
