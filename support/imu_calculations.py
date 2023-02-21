
from scipy.signal import savgol_filter

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

    for i in range(len(_imu_df)):
        if i == 0:
            _imu_df.loc[i, "angle_gx"] = 0
            _imu_df.loc[i, "angle_gy"] = 0
            _imu_df.loc[i, "angle_gz"] = 0
        else:
            _imu_df.loc[i, "angle_gx"] = _imu_df.loc[i-1, "angle_gx"] + (_imu_df.loc[i, "gx"] - val_x) * 0.01 
            _imu_df.loc[i, "angle_gy"] = _imu_df.loc[i-1, "angle_gy"] + (_imu_df.loc[i, "gy"] - val_y) * 0.01
            _imu_df.loc[i, "angle_gz"] = _imu_df.loc[i-1, "angle_gz"] + (_imu_df.loc[i, "gz"] - val_z) * 0.01

    return _imu_df