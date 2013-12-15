"""
Specific ipython stuff
"""
import IPython

from ts_charting import reset_figure

IN_NOTEBOOK = True
instance = IPython.Application._instance

# IPython.frontend was flattened so its submodule now live in the root
# namespace. i.e. IPython.frontend.terminal -> IPython.terminal
if hasattr(IPython, 'frontend'):
    terminal = IPython.frontend.terminal.ipapp.TerminalIPythonApp
else:
    terminal = IPython.terminal.ipapp.TerminalIPythonApp

if isinstance(instance, terminal):
    IN_NOTEBOOK = False

def figsize(width, height):
    """
    Resize figure
    """
    IPython.core.pylabtools.figsize(width, height)

# in notebook, reset the CURRENT_FIGURE for every cell execution
# this allows us to have cell specific plots
shell = IPython.InteractiveShell._instance
if IN_NOTEBOOK and shell:
    shell.register_post_execute(reset_figure)
