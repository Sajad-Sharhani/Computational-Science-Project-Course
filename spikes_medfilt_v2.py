import time
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import medfilt
import numpy as np
import math


# Read and parse the CSV file, assigning proper column names
def read_FA_file(filename):
    try:
        df = pd.read_csv(filename, header=None)
        df.columns = ['Column1', 'ID', 'Column3', 'Timestamp', 'X', 'Y', 'Z']
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


def calculate_acceleration(data): 
    # Calculate acceleration using the velocity difference
    data['Acceleration'] = data['Velocity'].diff() / data['TimeDiff']
    # Fill NaN values with 0 which might occur for the first calculation
    data['Acceleration'] = data['Acceleration'].fillna(0)
    # Return the modified DataFrame with the 'Acceleration' column added
    return data


def calculate_angular_observables(data):

    # Calculate slope
    data['Slope'] = data['Y'].diff() / data['X'].diff()
    data['Slope'] = data['Slope'].fillna(0)

    # Calculate angle theta
    data['Theta'] = data['Slope'].apply(lambda slope: math.atan(slope) if not math.isnan(slope) else None)
    data['Theta'] = np.degrees(data['Theta'])
    data['Theta'] = data['Theta'].fillna(0)
    data['Cosine'] = data['Theta'].apply(lambda theta: math.cos(theta) if not math.isnan(theta) else None)

    data['Theta_diff'] = data['Theta'].diff()
    data['Theta_diff'] = data['Theta_diff'].fillna(0)

    return data


# detect and drop inactive tags
def detect_drop_inactive_tags(df):
    """Detect and drop stationary tags."""
    
    print("Removing Stationary Tags.")
    
    # get unique cow tags
    unique_tags = df.ID.unique()
    to_drop = []

    # loop over ucows, find stationary tags
    for tag in unique_tags:
        temp = get_individual(df, tag)
        
        x = list(temp['X'])
        y = list(temp['Y'])
        z = list(temp['Z'])
        
        # save stationary tags to a list
        if abs(max(y)-min(y)) <= 2600:          # only check y-direction
            to_drop.append(tag)
    
    # drop stationary tags from the data
    for i in range(len(to_drop)):
        # print("Dropping Stationary Tag: ", cow)
        indexID = df[df.ID == to_drop[i]].index
        df = df.drop(indexID) # drop tags
    
    print("Stationary Tags Removed: ", len(to_drop))

    return df


# Plotting Quantities
def combined_plots(interval_data, fixed_signal, spikes, velocity_threshold, acc_threshold):
    # Set up a grid of plots with 2 rows and 3 columns
    # The first row for the original and cleaned signals, and velocity distribution
    # The second row for the scatter plots with original and cleaned data, and highlighted speeds
    fig, axs = plt.subplots(2, 4, figsize=(16, 8))

    # Original signal over time with spikes highlighted
    axs[0, 0].plot(interval_data['Timestamp'], interval_data['Y'], label='Original Signal')
    axs[0, 0].scatter(interval_data['Timestamp'][spikes], interval_data['Y'][spikes], color='red', label='Spikes')
    #axs[0, 0].set_title('Original Signal Over Time with Spikes')
    axs[0, 0].set_xlabel('Time')
    axs[0, 0].set_ylabel('Y')
    axs[0, 0].legend()

    # Cleaned signal over time
    axs[0, 1].plot(interval_data['Timestamp'], fixed_signal, label='Fixed Signal', color='orange')
    #axs[0, 1].set_title('Cleaned Signal Over Time')
    axs[0, 1].set_xlabel('Time')
    axs[0, 1].set_ylabel('Y cleaned')
    axs[0, 1].legend()

    # Velocity distribution
    axs[0, 2].hist(interval_data['Velocity'], bins=30, color='blue', alpha=0.7)
    #axs[0, 2].set_title('Velocity Distribution')
    axs[0, 2].set_xlabel('Velocity')
    axs[0, 2].set_ylabel('Frequency')

    # acceleration distribution
    axs[0, 3].hist(interval_data['Acceleration'], bins=30, color='blue', alpha=0.7)
    #axs[0, 3].set_title('acc Distribution')
    axs[0, 3].set_xlabel('Acceleration')
    axs[0, 3].set_ylabel('Frequency')

    # Scatter plot with original data
    axs[1, 0].scatter(interval_data['X'], interval_data['Y'], label='Original Data', alpha=0.5)
    axs[1, 0].scatter(interval_data['X'][spikes], interval_data['Y'][spikes], color='red', label='Spikes', alpha=0.5)
    #axs[1, 0].set_title('Scatter Plot with Spikes Highlighted')
    axs[1, 0].set_xlabel('X')
    axs[1, 0].set_ylabel('Y')
    axs[1, 0].legend()

    # Scatter plot with cleaned data
    axs[1, 1].scatter(interval_data['X'], fixed_signal, label='Data after Spike Removal', color='orange', alpha=0.5)
    #axs[1, 1].set_title('Cleaned Data Scatter Plot')
    axs[1, 1].set_xlabel('X')
    axs[1, 1].set_ylabel('Y cleaned')
    axs[1, 1].legend()

    # Scatter plot with speeds highlighted
    normal_speeds = interval_data['Velocity'] <= velocity_threshold
    abnormal_speeds = interval_data['Velocity'] > velocity_threshold
    axs[1, 2].scatter(interval_data['X'][normal_speeds], interval_data['Y'][normal_speeds], label='Normal Speed', alpha=0.5)
    axs[1, 2].scatter(interval_data['X'][abnormal_speeds], interval_data['Y'][abnormal_speeds], color='red', label='Abnormal Speed', alpha=0.5)
    #axs[1, 2].set_title('Scatter Plot with Speeds Highlighted')
    axs[1, 2].set_xlabel('X Position')
    axs[1, 2].set_ylabel('Y Position')
    axs[1, 2].legend()

    # Scatter plot with acceleration highlighted
    normal_acc = interval_data['Acceleration'] <= acc_threshold
    abnormal_acc = interval_data['Acceleration'] > acc_threshold
    axs[1, 3].scatter(interval_data['X'][normal_acc], interval_data['Y'][normal_acc], label='Normal Acceleration', alpha=0.5)
    axs[1, 3].scatter(interval_data['X'][abnormal_acc], interval_data['Y'][abnormal_acc], color='red', label='Abnormal Acceleration', alpha=0.5)
    #axs[1, 3].set_title('Scatter Plot with Acceleration Highlighted')
    axs[1, 3].set_xlabel('X Position')
    axs[1, 3].set_ylabel('Y Position')
    axs[1, 3].legend()

    plt.tight_layout()
    plt.savefig("com_plot.png")


def angular_plots(data, spikes):
    """Plot angular quantities with or without spikes."""
    
    fig, axs = plt.subplots(1, 4, figsize=(16, 4))

    # Theta Distribution
    # axs[0].hist(data['Theta'][~spikes], bins=30, color='blue', alpha=0.7)       # without spikes
    # axs[0].hist(data['Theta'][spikes], bins=30, color='red', alpha=0.7)         # only spikes
    axs[0].hist(data['Theta'], bins=30, color='blue', alpha=0.7)                  # all data
    axs[0].set_xlabel('Theta')
    axs[0].set_ylabel('Frequency')

    # Cosine Theta Distribution
    # axs[1].hist(data['Cosine'][~spikes], bins=30, color='blue', alpha=0.7)
    # axs[1].hist(data['Cosine'][spikes], bins=30, color='red', alpha=0.7)
    axs[1].hist(data['Cosine'], bins=30, color='blue', alpha=0.7)
    axs[1].set_xlabel('Cosine')
    axs[1].set_ylabel('Frequency')
    
    # Theta Difference Distribution
    # axs[2].hist(data['Theta_diff'][~spikes], bins=30, color='blue', alpha=0.7)
    # axs[2].hist(data['Theta_diff'][spikes], bins=30, color='red', alpha=0.7)
    axs[2].hist(data['Theta_diff'], bins=30, color='blue', alpha=0.7)
    axs[2].set_xlabel('Theta Diff')
    axs[2].set_ylabel('Frequency')
    
    # Velocity vs Theta Diff Distribution
    # axs[3].scatter(data['Velocity'][~spikes], data['Theta_diff'][~spikes], alpha=0.7)
    # axs[3].scatter(data['Velocity'][spikes], data['Theta_diff'][spikes],  color='red', alpha=0.7)
    axs[3].scatter(data['Velocity'], data['Theta_diff'], alpha=0.7)
    axs[3].set_xlabel('Velocity')
    axs[3].set_ylabel('Theta Diff')

    # Adjust layout and save figure.
    plt.tight_layout()
    plt.savefig("ang_plot.png")

    
def main():
    
    # 7 days data of cows
    filenames = [
        'FA_20200919T000000UTC.csv',
        'FA_20200920T000000UTC.csv',
        'FA_20200921T000000UTC.csv',
        'FA_20200922T000000UTC.csv',
        'FA_20200923T000000UTC.csv',
        'FA_20200924T000000UTC.csv',
        'FA_20200925T000000UTC.csv',
    ]

    # 1 day data of cows
    filenames = ['FA_20191115T000000UTC.csv']
    
    datafiles = []
    for filename in filenames:
        print(filename)
        data = read_FA_file(filename)
        datafiles.append(data)
    
    data = pd.concat(datafiles)

    individual_id = 2417246
    start_time = '2019-11-15 02:05:00'
    end_time = '2019-11-15 02:20:00'
    spike_threshold = 200

    if data is not None:
        
        # Remove Stationary Tags
        data = detect_drop_inactive_tags(data)
               
        # Benchmark: Start Time
        starttime = time.time()

        data = get_individual(data, individual_id)
        data = get_interval(data, start_time, end_time)
        data = calculate_velocity(data)
        data = calculate_acceleration(data)
        data = calculate_angular_observables(data)
        fixed_signal, spikes = remove_spikes_and_identify(data['Y'], spike_threshold)

        # Ensure 'Velocity' column exists before trying to access it
        if 'Velocity' in data.columns:
            velocity_threshold = np.percentile(data['Velocity'], 95)
            print(f"The calculated velocity threshold is: {velocity_threshold}")

        # Ensure 'Acceleration' column exists before trying to access it
        if 'Acceleration' in data.columns:
            acceleration_threshold = np.percentile(data['Acceleration'], 95)
            print(f"The calculated acceleration threshold is: {acceleration_threshold}")
        
        # Benchmark: Elapsed Time
        endtime = time.time()
        elapsed_time = endtime - starttime
        print(f'Time taken: {elapsed_time:.6f} seconds')
        
        # Use combined plot function here
        combined_plots(data, fixed_signal, spikes, velocity_threshold, acceleration_threshold)
        
        # angular quantities with/without spikes
        angular_plots(data, spikes)

        
if __name__ == "__main__":

    # Benchmark: Start Time
    # start_time = time.time()

    main()

    # Benchmark: Elapsed Time
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f'Time taken: {elapsed_time:.6f} seconds')
