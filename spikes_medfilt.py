## ----------------------------------------------------------------------------
# Copyright (C) 2023 Sajad Sharhani
#
# @file         spikes_medfilt.py
# @author       Sajad Sharhani
# @brief        Spike Removal in Time Series Data
# @details      This script processes time series data from a CSV file, 
#               identifies and removes spikes using a median filter, and 
#               visualizes both the original and cleaned data for comparison.
#               It is designed to handle individual tracking data and employs
#               the median filter from scipy's signal processing module to 
#               mitigate the effects of transient spikes in signal data.
# -----------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import medfilt

# Read and parse the CSV file, assigning proper column names
def read_FA_file(filename):
    try:
        df = pd.read_csv(filename, header=None)
        df.columns = ['Column1', 'ID', 'Column3', 'Timestamp', 'X', 'Y', 'Column7']
        return df
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Filter data by a specific individual's ID
def get_individual(data, individual_id):
    return data[data['ID'] == individual_id]

# Get data within a specified time interval
def get_interval(data, start_time, end_time):
    try:
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')
        mask = (data['Timestamp'] >= pd.to_datetime(start_time)) & (data['Timestamp'] <= pd.to_datetime(end_time))
        return data.loc[mask]
    except Exception as e:
        print(f"An error occurred while filtering by interval: {e}")
        return pd.DataFrame()

# Remove spikes from the signal and return both the cleaned signal and the locations of the spikes
def remove_spikes_and_identify(y_data, spike_threshold):
    median_signal = medfilt(y_data, kernel_size=41)  # Using median filter to smooth the signal
    diff_signal = abs(y_data - median_signal)
    spikes = diff_signal > spike_threshold
    fixed_y_data = y_data.copy()
    fixed_y_data[spikes] = median_signal[spikes]
    return fixed_y_data, spikes

# Plot original and cleaned signals, including scatter plot and signal over time
def plot_data_with_spikes(interval_data, fixed_signal, spikes):
    plt.figure(figsize=(18, 6))

    # Scatter plot with spikes highlighted
    plt.subplot(1, 3, 1)
    plt.scatter(interval_data['X'], interval_data['Y'], label='Original Data')
    plt.scatter(interval_data['X'][spikes], interval_data['Y'][spikes], color='red', label='Spikes')
    plt.title('Scatter Plot with Spikes Highlighted')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()

    # Signal over time with spikes highlighted
    plt.subplot(1, 3, 2)
    plt.plot(interval_data['Timestamp'], interval_data['Y'], label='Original Signal')
    plt.scatter(interval_data['Timestamp'][spikes], interval_data['Y'][spikes], color='red', label='Spikes')
    plt.plot(interval_data['Timestamp'], fixed_signal, label='Fixed Signal', color='orange')
    plt.title('Signal Over Time with Spikes Highlighted')
    plt.xlabel('Time')
    plt.ylabel('Y')
    plt.legend()

    # Cleaned signal scatter plot
    plt.subplot(1, 3, 3)
    plt.scatter(interval_data['X'], fixed_signal, label='Data after Spike Removal', color='orange')
    plt.title('Cleaned Signal Scatter Plot')
    plt.xlabel('X')
    plt.ylabel('Y cleaned')
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    filename = 'FA_20191115T000000UTC.csv'
    individual_id = 2417246
    start_time = '2019-11-15 02:05:00'
    end_time = '2019-11-15 02:20:00'
    spike_threshold = 200

    data = read_FA_file(filename)
    if data is not None:
        individual_data = get_individual(data, individual_id)
        interval_data = get_interval(individual_data, start_time, end_time)
        fixed_signal, spikes = remove_spikes_and_identify(interval_data['Y'], spike_threshold)
        plot_data_with_spikes(interval_data, fixed_signal, spikes)

if __name__ == "__main__":
    main()
