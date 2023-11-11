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
import numpy as np


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


def calculate_velocity(data):
    # Convert the 'Timestamp' column to datetime format for time operations
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    # Calculate the time difference between each consecutive timestamp in seconds
    data['TimeDiff'] = data['Timestamp'].diff().dt.total_seconds()
    # Calculate the difference in the 'X' position between each consecutive reading
    data['X_diff'] = data['X'].diff()
    # Calculate the difference in the 'Y' position between each consecutive reading
    data['Y_diff'] = data['Y'].diff()
    # Calculate the velocity using the Pythagorean theorem and dividing by time difference
    data['Velocity'] = np.sqrt(data['X_diff']**2 + data['Y_diff']**2) / data['TimeDiff']
    # Fill any NaN values with 0 which might occur for the first calculation
    data['Velocity'] = data['Velocity'].fillna(0)
    # Return the modified DataFrame with the new 'Velocity' column
    return data

def combined_plots(interval_data, fixed_signal, spikes, velocity_threshold):
    # Set up a grid of plots with 2 rows and 3 columns
    # The first row for the original and cleaned signals, and velocity distribution
    # The second row for the scatter plots with original and cleaned data, and highlighted speeds
    fig, axs = plt.subplots(2, 3, figsize=(18, 12))

    # Original signal over time with spikes highlighted
    axs[0, 0].plot(interval_data['Timestamp'], interval_data['Y'], label='Original Signal')
    axs[0, 0].scatter(interval_data['Timestamp'][spikes], interval_data['Y'][spikes], color='red', label='Spikes')
    axs[0, 0].set_title('Original Signal Over Time with Spikes')
    axs[0, 0].set_xlabel('Time')
    axs[0, 0].set_ylabel('Y')
    axs[0, 0].legend()

    # Cleaned signal over time
    axs[0, 1].plot(interval_data['Timestamp'], fixed_signal, label='Fixed Signal', color='orange')
    axs[0, 1].set_title('Cleaned Signal Over Time')
    axs[0, 1].set_xlabel('Time')
    axs[0, 1].set_ylabel('Y cleaned')
    axs[0, 1].legend()

    # Velocity distribution
    axs[0, 2].hist(interval_data['Velocity'], bins=30, color='blue', alpha=0.7)
    axs[0, 2].set_title('Velocity Distribution')
    axs[0, 2].set_xlabel('Velocity (units per second)')
    axs[0, 2].set_ylabel('Frequency')

    # Scatter plot with original data
    axs[1, 0].scatter(interval_data['X'], interval_data['Y'], label='Original Data', alpha=0.5)
    axs[1, 0].scatter(interval_data['X'][spikes], interval_data['Y'][spikes], color='red', label='Spikes', alpha=0.5)
    axs[1, 0].set_title('Scatter Plot with Spikes Highlighted')
    axs[1, 0].set_xlabel('X')
    axs[1, 0].set_ylabel('Y')
    axs[1, 0].legend()

    # Scatter plot with cleaned data
    axs[1, 1].scatter(interval_data['X'], fixed_signal, label='Data after Spike Removal', color='orange', alpha=0.5)
    axs[1, 1].set_title('Cleaned Data Scatter Plot')
    axs[1, 1].set_xlabel('X')
    axs[1, 1].set_ylabel('Y cleaned')
    axs[1, 1].legend()

    # Scatter plot with speeds highlighted
    normal_speeds = interval_data['Velocity'] <= velocity_threshold
    abnormal_speeds = interval_data['Velocity'] > velocity_threshold
    axs[1, 2].scatter(interval_data['X'][normal_speeds], interval_data['Y'][normal_speeds], label='Normal Speed', alpha=0.5)
    axs[1, 2].scatter(interval_data['X'][abnormal_speeds], interval_data['Y'][abnormal_speeds], color='red', label='Abnormal Speed', alpha=0.5)
    axs[1, 2].set_title('Scatter Plot with Speeds Highlighted')
    axs[1, 2].set_xlabel('X Position')
    axs[1, 2].set_ylabel('Y Position')
    axs[1, 2].legend()

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
        interval_data_with_velocity = calculate_velocity(interval_data)
        fixed_signal, spikes = remove_spikes_and_identify(interval_data['Y'], spike_threshold)

        # Ensure 'Velocity' column exists before trying to access it
        if 'Velocity' in interval_data_with_velocity.columns:
            velocity_threshold = np.percentile(interval_data_with_velocity['Velocity'], 95)
            print(f"The calculated velocity threshold is: {velocity_threshold}")
            # Use the combined plot function here
            combined_plots(interval_data_with_velocity, fixed_signal, spikes, velocity_threshold)
        else:
            print("Velocity column has not been created.")

if __name__ == "__main__":
    main()

