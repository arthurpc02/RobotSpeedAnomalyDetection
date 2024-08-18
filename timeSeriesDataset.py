import requests
import pandas as pd
from io import StringIO
from collections import deque
import matplotlib.pyplot as plt


def receive_data_as_a_list(url):
    """ Receive all the data"""
    response = requests.get(url, stream=True)
    response.raise_for_status() # check for errors

    data = []
    for line in response.iter_lines():
        if line:
            data.append(line.decode('utf-8'))
        
    return data


def fill_window_frame(queue, input_data, queue_max_len=10):
    """ the queue has to be full to start the data analysis """

    while len(queue) < queue_max_len:
        new_data = input_data.pop()
        queue.append(new_data)
    return


def stream_data(queue, input_data, increment=2, queue_max_len=10):
    """ Simulates a continuous data stream """
    pass


def detect_anomalies_zscore(data, threshold=3):
    """
    Detect anomalies using the Z-score method.
    
    Parameters:
    - data: A pandas Series containing the time-series data.
    - threshold: Z-score threshold for detecting anomalies.
    
    Returns:
    - A DataFrame with an additional 'Anomaly' column.
    """
    mean = data.mean()
    std = data.std()
    
    z_scores = (data - mean) / std
    anomalies = z_scores.abs() > threshold

    anomaly_df = pd.DataFrame({'Data': data, 'Z-Score': z_scores, 'Anomaly': anomalies})

    return anomaly_df, mean, std


def plot_data_with_anomalies(data, mean, std, anomaly_count):
    """ Plotting the data and highlighting the anomalies with additional metrics """

    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['Data'], label='Speed Data', color='blue')

    # Highlight anomalies
    plt.scatter(data.index[data['Anomaly']], 
                data['Data'][data['Anomaly']], 
                color='red', label='Anomalies', marker='o')

    # Add annotations for mean, std, and anomaly count
    plt.text(0.81, 1.03, f"Mean: {mean:.2f} | Std Dev: {std:.2f} | Anomaly Count: {anomaly_count}", 
             horizontalalignment='center', 
             verticalalignment='center', 
             transform=plt.gca().transAxes,
             fontsize=12, 
             bbox=dict(facecolor='white', alpha=0.5))

    # Adding labels and title
    plt.title('Robot Speed Data with Anomalies Highlighted', loc='left')
    plt.xlabel('Index')
    plt.ylabel('Speed')
    plt.legend()

    # Save the plot as an image file
    plt.savefig('speed_data_with_anomalies.png')

    # Show the plot
    plt.show()


##########################################
# 1. Stream Data
##########################################

url = "https://docs.google.com/spreadsheets/d/19galjYSqCDf6Ohb0IWv6YsRL7MV0EPFpN-2blGGS97U/pub?output=csv"
window_frame = 10
increment = 2

data_list = receive_data_as_a_list(url)
csv_headers = data_list.pop(0)

streamed_queue = deque(maxlen=window_frame)
fill_window_frame(streamed_queue, data_list, window_frame)

# data_analysis()
# while len(data_list) > 0:
# stream_data(streamed_queue, data_list, increment, window_frame)

csv_data = csv_headers + "\n" + "\n".join(streamed_queue)
print(csv_data)
dataFrame = pd.read_csv(StringIO(csv_data))


##########################################
# 2. Anomaly Detection
##########################################

# anomalies_output = detect_anomalies_zscore(dataFrame['speed'])
# anomaly_df = anomalies_output[0]
# anomaly_count = anomaly_df['Anomaly'].sum()
# spd_mean = anomalies_output[1]
# spd_std = anomalies_output[2]


##########################################
# 3. Metrics Reporting
##########################################


print(dataFrame)
print(dataFrame.info())

# print(anomaly_df)
# print(anomaly_df.info())
# print(f'anomaly count: {anomaly_count}')
# print(f'mean: {spd_mean}')
# print(f'std dev.: {spd_std}')

# plot_data_with_anomalies(anomaly_df, spd_mean, spd_std, anomaly_count)

##########################################
# 4. Code Submission
##########################################
# outside of the .py file