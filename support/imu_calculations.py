
from scipy.signal import savgol_filter
import polars as pl

def calculate_imu_orientation(df, filter_size=51, filter_order=1, zero_drift=50):
    """
    df: the dataframe containing the imu data
    filter_size: the size of the filter window (should be odd)
    The funciton uses the savgol filter to smooth the data
    filter_order: the order of the filter
    zero_drift: the number of rows to use to calculate the zero drift

    the df should contain gx, gy, gz columns

    returns: the dataframe with the calculated angles
    """    
    
    _imu_df = df.copy()

    _imu_df["gy"] = savgol_filter(_imu_df["gy"], filter_size, filter_order)
    _imu_df["gx"] = savgol_filter(_imu_df["gx"], filter_size, filter_order)
    _imu_df["gz"] = savgol_filter(_imu_df["gz"], filter_size, filter_order)

    val_x = _imu_df["gx"][:zero_drift].mean()
    val_y = _imu_df["gy"][:zero_drift].mean()
    val_z = _imu_df["gz"][:zero_drift].mean()

    # calculating angle from gx, gy, gz

    my_dict = {"angle_gx":[],"angle_gy":[],"angle_gz":[]}

    for i in range(len(_imu_df)):
        if i == 0:
            my_dict["angle_gx"].append(0)
            my_dict["angle_gy"].append(0)
            my_dict["angle_gz"].append(0)
        else:
            my_dict["angle_gx"].append(my_dict["angle_gx"][i-1] + (_imu_df["gx"][i] - val_x) * 0.01)
            my_dict["angle_gy"].append(my_dict["angle_gy"][i-1] + (_imu_df["gy"][i] - val_y) * 0.01)
            my_dict["angle_gz"].append(my_dict["angle_gz"][i-1] + (_imu_df["gz"][i] - val_z) * 0.01)

    _gyro_df = df.copy()
    _gyro_df["angle_gx"] = my_dict["angle_gx"]
    _gyro_df["angle_gy"] = my_dict["angle_gy"]
    _gyro_df["angle_gz"] = my_dict["angle_gz"]

    return _gyro_df

def calculate_imu_velocity(df, filter_size=51, filter_order=1, zero_drift=50):
    """
    df: the dataframe containing the imu data
    filter_size: the size of the filter window (should be odd)
    The funciton uses the savgol filter to smooth the data
    filter_order: the order of the filter
    zero_drift: the number of rows to use to calculate the zero drift

    the df should contain ax, ay, az columns

    returns: the dataframe with the calculated angles
    """    
    
    _imu_df = df.copy()

    val_x = _imu_df["ax"][:zero_drift].mean()
    val_y = _imu_df["ay"][:zero_drift].mean()
    val_z = _imu_df["az"][:zero_drift].mean()

    # calculating angle from ax, ay, az
    _imu_df = pl.from_pandas(_imu_df)

    my_dict = {"vel_x":[],"vel_y":[],"vel_z":[]}

    for i in range(len(_imu_df)):
        if i == 0:
            my_dict["vel_x"].append(0)
            my_dict["vel_y"].append(0)
            my_dict["vel_z"].append(0)
        else:

            my_dict["vel_x"].append(my_dict["vel_x"][i-1] + (_imu_df["ax"][i] - val_x) * 0.01)
            my_dict["vel_y"].append(my_dict["vel_y"][i-1] + (_imu_df["ay"][i] - val_y) * 0.01)
            my_dict["vel_z"].append(my_dict["vel_z"][i-1] + (_imu_df["az"][i] - val_z) * 0.01)

    _vel_df = df.copy()
    _vel_df["vel_x"] = my_dict["vel_x"]
    _vel_df["vel_y"] = my_dict["vel_y"]
    _vel_df["vel_z"] = my_dict["vel_z"]

    return _vel_df


def calculate_imu_displacement(df, filter_size=51, filter_order=1, zero_drift=0):
    """
    df: the dataframe containing the imu data
    filter_size: the size of the filter window (should be odd)
    The funciton uses the savgol filter to smooth the data
    filter_order: the order of the filter
    zero_drift: the number of rows to use to calculate the zero drift

    the df should contain ax, ay, az columns

    returns: the dataframe with the calculated displacemnt
    """    
    
    _imu_df = df.copy()

    # calculating angle from ax, ay, az
    _imu_df = pl.from_pandas(_imu_df)

    my_dict = {"disp_x":[],"disp_y":[],"disp_z":[]}

    for i in range(len(_imu_df)):
        if i == 0:
            my_dict["disp_x"].append(0)
            my_dict["disp_y"].append(0)
            my_dict["disp_z"].append(0)
        else:

            my_dict["disp_x"].append(my_dict["disp_x"][i-1] + (_imu_df["vel_x"][i]) * 0.01)
            my_dict["disp_y"].append(my_dict["disp_y"][i-1] + (_imu_df["vel_y"][i]) * 0.01)
            my_dict["disp_z"].append(my_dict["disp_z"][i-1] + (_imu_df["vel_z"][i]) * 0.01)

    _disp_df = df.copy()
    _disp_df["disp_x"] = my_dict["disp_x"]
    _disp_df["disp_y"] = my_dict["disp_y"]
    _disp_df["disp_z"] = my_dict["disp_z"]

    return _disp_df
