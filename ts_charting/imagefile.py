"""
Idea is to turn on writing to images for all plots
"""
import os
import errno
import tempfile

import pandas as pd
import IPython
import IPython.core.pylabtools as pylabtools
import matplotlib.pylab as pylab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import ts_charting as charting

def save_to_pdf(file, figs=None):
    with PdfPages(file) as pdf:

        if figs is None:
            figs = pylabtools.getfigs()

        for fig in figs:
            fig.savefig(pdf, format='pdf')

    close_figures()

def plot_pdf(fn=None, open=True):
    if fn is None:
        file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        fn = file.name

    dir, file = os.path.split(fn)
    if dir:
        mkdir_p(dir)

    save_to_pdf(fn)
    if open:
        os.system('open '+fn)
    return fn

def _get_title(fig):
    """ 
    grab title from figure. Assume it's a one ax per figure or that
    the main ax is the first one
    """
    ax = fig.get_axes()[0] # assume first ax is correct
    title = ax.title.get_text()
    return title

def mkdir_p(path):
    """
    http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python 
    """
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def save_images(dir='', figs=None, prefix=None):
    """
    Save all open figures to image files. 

    Parameters:
    ----------
    dir : string
        Directory to place image files into
    figs : list of Figures
        will default to open figures
    prefix : string
        prefix all image file names
    """
    if figs is None:
        figs = pylabtools.getfigs()

    if dir:
        mkdir_p(dir)

    for i, fig in enumerate(figs, 1):
        label = _get_title(fig)
        if label == '':
            label = "Figure_%d" % i
        if prefix:
            label = prefix + '_' + label
        filepath = os.path.join(dir, label+'.png')
        fig.savefig(filepath)

    close_figures()

def close_figures():
    plt.close('all')
    charting.gcf(reset=True)


# start of doing something where the execution stuff runs automatically?
def imagefile_reroute(func):
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapped

shell = IPython.InteractiveShell._instance
shell = None

# check so we don't break non ipython runs
if shell:
    execution_magic = shell.magics_manager.registry['ExecutionMagics']
    execution_magic.default_runner = imagefile_reroute(execution_magic.default_runner)
