import pandas as pd
from pandas import json
from IPython.display import JSON

def dataframe_json(df):
    data = {}
    for k, v in df.items():
        data[k] = v.values
    data['index'] = df.index
    data['_pandas_type'] = 'dataframe';
    data['__repr__'] = repr(df)
    return json.dumps(data)

def series_json(series):
    data = {}
    data['data'] = series.values
    data['index'] = series.index
    data['name'] = series.name
    data['_pandas_type'] = 'series'
    data['__repr__'] = repr(series)
    return json.dumps(data)

def to_json(obj):
    if isinstance(obj, pd.DataFrame):
        return dataframe_json(obj)

    if isinstance(obj, pd.Series):
        return series_json(obj)

    if isinstance(obj, list):
        jlist = []
        for v in obj:
            jlist.append(to_json(v))
        return json_list(jlist)

    if isinstance(obj, dict):
        jdict = {}
        for k, v in obj.items():
            jdict[k] = to_json(v)
        return json_dict(jdict)

    if hasattr(obj, 'to_json'):
        return obj.to_json()

    return json.dumps(obj)

def json_dict(dct):
    items = []
    for k, v in dct.items():
        items.append("\"{k}\":{v}".format(k=k, v=v))
    return "{" + ','.join(items) + "}" 

def json_list(lst):
    return "[" + ','.join(lst) + "]" 

def to_json_display(obj):
    return JSON(to_json(obj));
