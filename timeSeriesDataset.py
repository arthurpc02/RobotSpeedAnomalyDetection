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


def queue_to_csv(queue, headers):
    csv = headers + "\n" + "\n".join(queue)
    return StringIO(csv)


def stream_data(queue, input_data, increment=2):
    """ Simulates a continuous data stream """
    for _ in range(increment):
        new_data = input_data.pop()
        queue.append(new_data)
    return


def anomaly_detection(dataFrame):
    anomalies_output = detect_anomalies_zscore(dataFrame['speed'])
    anomaly_df = anomalies_output[0]
    spd_mean = anomalies_output[1]
    spd_std = anomalies_output[2]
    anomaly_count = anomaly_df['Anomaly'].sum()

    return {'anomaly_df':anomaly_df, 'mean':spd_mean, 'std':spd_std, 'count':anomaly_count}


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


def plot_data_with_anomalies(anomalyResults):
    """ Plotting the data and highlighting the anomalies with additional metrics """

    data = anomalyResults['anomaly_df']
    mean = anomalyResults['mean']
    std = anomalyResults['std']
    anomaly_count = anomalyResults['count']

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
    plt.draw()

    # Pause before closing the plot
    plt.pause(5)
    plt.close()


##########################################
# 1. Stream Data
##########################################

url = "https://docs.google.com/spreadsheets/d/19galjYSqCDf6Ohb0IWv6YsRL7MV0EPFpN-2blGGS97U/pub?output=csv"
window_frame = 10000
increment = 1000

data_list = receive_data_as_a_list(url)
csv_headers = data_list.pop(0)

streamed_queue = deque(maxlen=window_frame)

# in the first run, the increment should be enough to fill the window frame for the analysis
# so we provide the maxlen of the queue as the increment.
stream_data(streamed_queue, data_list, window_frame) 

# to do: wrap the data analysis in a function, because it's repeating
csv_data = queue_to_csv(streamed_queue, csv_headers)
dataFrame = pd.read_csv(csv_data)
anomalyResults = anomaly_detection(dataFrame)

print(dataFrame)
print(dataFrame.info())
plot_data_with_anomalies(anomalyResults)

while len(data_list) > 0: 
    stream_data(streamed_queue, data_list, increment)  # to do: this function probably breaks in the last elements

    csv_data = queue_to_csv(streamed_queue, csv_headers)
    dataFrame = pd.read_csv(csv_data)
    anomalyResults = anomaly_detection(dataFrame)

    print(dataFrame)
    print(dataFrame.info())
    plot_data_with_anomalies(anomalyResults)

# to do: final report with all the anomalies detected

print("end")

##########################################
# 2. Anomaly Detection
##########################################




##########################################
# 3. Metrics Reporting
##########################################




# print(anomaly_df)
# print(anomaly_df.info())
# print(f'mean: {spd_mean}')
# print(f'std dev.: {spd_std}')
# print(f'anomaly count: {anomalyResults[]}')


# plot_data_with_anomalies(anomaly_df, spd_mean, spd_std, anomaly_count)

##########################################
# 4. Code Submission
##########################################
# outside of the .py file