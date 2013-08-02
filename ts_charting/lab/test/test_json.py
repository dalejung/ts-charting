import numpy as np
import pandas as pd
from pandas import json
from ts_charting.json import to_json

import ts_charting.lab.lab as tslab

plot_index = pd.date_range(start="2000-1-1", freq="B", periods=10000)
df = pd.DataFrame(index=plot_index)
df['open'] = np.random.randn(len(plot_index))
df['high'] = np.random.randn(len(plot_index))
df['low'] = np.random.randn(len(plot_index))
df['close'] = np.random.randn(len(plot_index))

lab = tslab.Lab()
fig = lab.station('candle')
df.tail(5).ohlc_plot()
fig.plot_markers('high', df.high > df.high.shift(1), yvalues=df.open)

jd = to_json(lab)
obj = json.loads(jd)

