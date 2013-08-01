from collections import OrderedDict

from ts_charting import Figure, Grapher, gcf, scf

class Lab(object):
    def __init__(self):
        self.data = {}
        self.plots = {}
        self.stations = OrderedDict()

    def station(self, name):
        station = Station(self, name)
        self.stations[name] = station
        scf(station)
        return station

class Station(object):
    def __init__(self, lab, name):
        self.lab = lab
        self.name = name
        self.figure = Figure(1, warn=False)
        self.layers = OrderedDict()

    def plot_markers(self, name, series, yvalues=None, xindex=None, **kwargs):
        geom = {'type': 'marker'}
        geom['yvalues'] = yvalues
        geom['xindex'] = xindex
        geom.update(kwargs)

        self.layer(name, series, geom)
        self.figure.plot_markers(name, series, yvalues=yvalues, xindex=xindex, **kwargs)

    def __getattr__(self, name):
        if hasattr(self.figure, name):
            return getattr(self.figure, name)
        raise AttributeError()

    def ohlc(self, df, width=0.3):
        self.layer('candlestick', df, {'type': 'candlestick', 'width': .03})
        self.figure.ohlc(df, width=width)

    def layer(self, name, data, geoms):
        if not isinstance(geoms, list):
            geoms = [geoms]

        if name in self.layers:
            raise Exception("Already have named layer, don't support updates yet")

        self.layers[name] = {'data': data, 'geoms':geoms}
