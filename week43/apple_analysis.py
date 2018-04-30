# -*- coding:utf-8 -*-
import pandas as pd

def quarter_volume():
    data = pd.read_csv('apple.csv', header=0)
    data_ext = data.loc[:,['Date','Volume']]
    data_series = pd.Series(data_ext['Volume'].tolist(),index = pd.to_datetime(data_ext['Date']))
    #print(data_series)
    #pd.to_datetime(data_series.Date)
    #print(data_series)
    data_sere = data_series.resample('Q').sum()
    #print(data_sere)
    #data_result = data_sere.to_frame('Volume')
    data_sort = data_sere.sort_values(ascending=False)
    second_volume = data_sort.get_value(1)
    print(second_volume)
    return second_volume

quarter_volume()
