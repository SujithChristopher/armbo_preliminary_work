"""this code is written by Sujith"""

import enum
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import msgpack
import msgpack_numpy as mpn
from scipy.interpolate import interp1d

def read_df_csv(filename, offset=2):
    """
    this function reads the csv file from motion capture system
     and makes it into a dataframe and returns only useful information

    filename: input path to csv file from motive
    offset:to ignore the first two columns with time and frames generally

    """

    # offset = 2 #first two columns with frame_no and time

    pth = filename
    raw = pd.read_csv(pth)
    cols_list = raw.columns     # first row which contains capture start time
    inx = [i for i, x in enumerate(cols_list) if x == "Capture Start Time"]
    st_time = cols_list[inx[0] + 1]
    st_time = datetime.strptime(st_time, "%Y-%m-%d %I.%M.%S.%f %p")  # returns datetime object

    mr_inx = pd.read_csv(pth, skiprows=3)
    markers_raw = mr_inx.columns
    marker_offset = offset  # for ignoring time and frame cols
    markers_raw = markers_raw[marker_offset:]
    col_names = []
    for i in range(0, len(markers_raw), 3):
        col_names.append(markers_raw[i].split(":")[1])

    df_headers = ["frame", "seconds"]

    for id, i in enumerate(col_names):
        if not i.islower():
            col_names[id] = i.lower()
    
    for i in col_names:
        df_headers.append(i + "_x")
        df_headers.append(i + "_y")
        df_headers.append(i + "_z")
    mo_data = pd.read_csv(pth, skiprows=6)
    # mo_data = mo_data.rename(mo_data.columns, df_headers)
    mo_data.columns = df_headers

    return mo_data, st_time


def add_datetime_col(df, _time, _name):

    """
    df:     dataframe
    _time:  the time you want to start your column with
    _name:  name of the column that has time in seconds
    """

    _t = []
    for i in list(df[_name]):
        _t.append(_time + timedelta(0,float(i)))
    df["time"] = _t
    return df
    
def add_datetime_diff(df, _time, _sync, _diff_name, truncate = False):

    """
    df:         dataframe
    _time:      the time you want to start your column with
    _sync:      Name of the column with external sync which turns 1 when your recording 
                your data and 0 when your not
    _diff_name: external time/ other time which you want to find the difference 
                and add them to the _time column to sync clock
    truncate:   truncate will also cut the values after your _sync goes to 0
    """
    _inx = 0
    for inx, i in enumerate(df[_sync]):
        if i == 1:
            _inx = inx
            break

    df = df.loc[_inx:].copy()     # dropping unnecessary rows

    _diff = list(df[_diff_name].diff())
    _sum = 0
    _t = []
    for i in _diff:
        if np.isnan(i):
            i = 0
        _sum = _sum + i
        _t.append(_time + timedelta(0,float(_sum/1000)))

    df["time"] = _t

    if truncate:
        _count = 0
        for count, j in enumerate(df[_sync]):
            if j == 0:
                _count = count
                print(_count)
                break
        if _count is not 0:   
            df = df.loc[:_count].copy()     # dropping unnecessary rows
    
    return df

def add_time_from_file(df, _pth):
    """
    df:     dataframe
    _pth:   path to the file which has time in seconds
    """
    with open(_pth, "rb") as f:
        _time_obj = msgpack.Unpacker(f)
        _time = []
        for i in _time_obj:
            _time.append(i)
    df["time"] = _time
    df["time"] = pd.to_datetime(df["time"])
    return df

def interpolate_target_df(target_df, reference_df, col_names = None):
    # based on mocap time using interp1d function
    # for x, y, z coordinates and yaw, pitch, roll
    """
    target_df: dataframe to be interpolated
    reference_df: dataframe to be used as reference
    col_names: list of column names to be interpolated

    both dataframes should have a column named "time"
    """

    target_df = target_df.reset_index(drop=True)
    reference_df = reference_df.reset_index(drop=True)

    # column names 
    if col_names is None:
        col_names = ["frame_id","x", "y", "z", "yaw", "pitch", "roll"]

    df = pd.DataFrame(columns=col_names)
    df["time"] = reference_df.time

    # change reference time to float
    reference_df["time"] = reference_df["time"].dt.hour * 3600 + reference_df["time"].dt.minute * 60 + reference_df["time"].dt.second + reference_df["time"].dt.microsecond / 1000000
    # change target time to float
    target_df["time"] = target_df["time"].dt.hour * 3600 + target_df["time"].dt.minute * 60 + target_df["time"].dt.second + target_df["time"].dt.microsecond / 1000000

    new_cols = []
    for i in col_names:
        f = interp1d(target_df.time, target_df[i], fill_value="extrapolate")

        _new_val = f(reference_df.time)

        new_cols.append(_new_val)

    for idx, i in enumerate(col_names):
        df[i] = new_cols[idx]
    
    
    return df

def trunkate_dfs(df_1, df_2, display_print = False):
    # which starts earlier
    """
    df_1: dataframe 1
    df_2: dataframe 2

    both dataframes should have a column named "time"

    this code will truncate the dataframes to the same "time" length
    """
    if df_1["time"].iloc[0] < df_2["time"].iloc[0]:
        _start_inx = df_1.time.searchsorted(df_2.time[0])

        df_1 = df_1.loc[_start_inx:]
        df_1 = df_1.reset_index(drop=True)
        if display_print:
            print(_start_inx)
            print("df_1 starts earlier")
    else:
        _start_inx = df_2.time.searchsorted(df_1.time[0])
        df_2 = df_2.loc[_start_inx:]
        df_2 = df_2.reset_index(drop=True)
        if display_print:
            print(_start_inx)
            print("df_2 starts earlier")

    # which ends later
    if df_1["time"].iloc[-1] > df_2["time"].iloc[-1]:
        _end_inx = df_1.time.searchsorted(df_2.time.iloc[-1])
        df_1 = df_1.loc[:_end_inx]
        df_1 = df_1.reset_index(drop=True)
        if display_print:
            print(_end_inx)
            print("df_1 ends later")
    else:
        _end_inx = df_2.time.searchsorted(df_1.time.iloc[-1])
        df_2 = df_2.loc[:_end_inx]
        df_2 = df_2.reset_index(drop=True)
        if display_print:
            print(_end_inx)
            print("df_2 ends later")

    return df_1, df_2