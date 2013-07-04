# TODO SeriesByGroupBy.boxplot
"""
import matplotlib.ticker as ticker

labels = []
data = []
for label, group in grouped:
        labels.append(label)
            data.append(group)
r = labels
N = len(r)
ind = np.arange(N)  # the evenly spaced plot indices
def format_date(x, pos=None):
        thisind = np.clip(int(x+0.5), 0, N-1)
            return r[thisind].strftime('%Y-%m-%d')

        fig = gcf()
        ax = gca()
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        _ = boxplot(data) 
        fig.autofmt_xdate()
"""
