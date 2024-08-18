import requests
import pandas as pd
from io import StringIO
from collections import deque
import matplotlib.pyplot as plt

# to do: remove unused functions to a cemetery file
def receive_data_as_a_list(url):
    """ Receive all the data"""
    response = requests.get(url, stream=True)
    response.raise_for_status() # check for errors

    data = []
    for line in response.iter_lines():
        if line:
            data.append(line.decode('utf-8'))
        
    return data

def receive_data_and_queue_it(url):
    """ Receive all the data and puts it in a FIFO queue. """
    response = requests.get(url, stream=True)
    response.raise_for_status() # check for errors

    queue = deque()
    for line in response.iter_lines():
        if line:
            queue.append(line.decode('utf-8'))
        
    return queue



def queue_to_csv(queue, headers):
    csv = headers + "\n" + "\n".join(queue)
    return StringIO(csv)

def list_to_csv(list, headers):
    csv = headers + "\n" + "\n".join(list)
    return StringIO(csv)


def stream_data(queue, input_data, increment=2):
    """ Simulates a continuous data stream """
    for _ in range(increment):
        new_data = input_data.pop()
        queue.append(new_data)
    return

def simulate_continuous_data(data_source, window_size):
    """ Simulates a continuous data stream by taking only part of a queue """

    window = []
    for _ in range(window_size):
        new_data = data_source.popleft()
        window.append(new_data)
    return window




def zscore_anomaly_detection(dataFrame):
    anomalies_output = detect_anomalies_zscore(dataFrame)
    anomaly_df = anomalies_output[0]
    spd_mean = anomalies_output[1]
    spd_std = anomalies_output[2]
    anomaly_count = anomaly_df['Anomaly'].sum()
    anomalies_df_count = anomalies_output[3]

    return {'anomaly_df': anomaly_df, 'mean': spd_mean, 'std': spd_std, 'count': anomaly_count, 'df_count': anomalies_df_count}


def detect_anomalies_zscore(df, threshold=3):
    """
    Detect anomalies using the Z-score method.
    
    Parameters:
    - df: A pandas DataFrame containing the time-series data.
    - threshold: Z-score threshold for detecting anomalies.
    
    Returns:
    - anomaly_df: A DataFrame with the original columns plus an additional 'Anomaly' column.
    - mean: The mean of the 'speed' column.
    - std: The standard deviation of the 'speed' column.
    - anomalies_with_timestamp_df: A DataFrame containing only the anomalies with their corresponding timestamps.
    """
    data = df['speed']
    mean = data.mean()
    std = data.std()

    z_scores = (data - mean) / std
    anomalies = z_scores.abs() > threshold

    # Create a DataFrame with anomalies and corresponding timestamps
    anomalies_with_timestamp_df = df[anomalies].copy()
    anomalies_with_timestamp_df['Z-Score'] = z_scores[anomalies]
    
    # Add 'Z-Score' and 'Anomaly' columns to the original DataFrame
    anomaly_df = df.copy()
    anomaly_df['Z-Score'] = z_scores
    anomaly_df['Anomaly'] = anomalies

    return anomaly_df, mean, std, anomalies_with_timestamp_df


def validate_anomalies_with_a_chart(anomalyResults):
    """ Plotting the data and highlighting the anomalies with additional metrics """

    data = anomalyResults['anomaly_df']
    mean = anomalyResults['mean']
    std = anomalyResults['std']
    anomaly_count = anomalyResults['count']

    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['speed'], label='Speed Data', color='blue')

    # Highlight anomalies
    plt.scatter(data.index[data['Anomaly']], 
                data['speed'][data['Anomaly']], 
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


def post_results(anomaly_df):
    
    print(anomaly_df)
    print(anomaly_df.info())

    # to do: 
    # simulatePost()


##########################################
# 1. Stream Data
##########################################

def main():
    url = "https://docs.google.com/spreadsheets/d/19galjYSqCDf6Ohb0IWv6YsRL7MV0EPFpN-2blGGS97U/pub?output=csv"
    analysisWindow_size = 1000

    # data_list = receive_data_as_a_list(url)
    data_fifo = receive_data_and_queue_it(url)
    csv_headers = data_fifo.popleft()
    
    while len(data_fifo) > analysisWindow_size:
        analysis_window_list = simulate_continuous_data(data_fifo, analysisWindow_size)
        analysis_windos_csv = list_to_csv(analysis_window_list, csv_headers)
        analysis_window_df = pd.read_csv(analysis_windos_csv)

        analysis_results_dict = zscore_anomaly_detection(analysis_window_df)
        validate_anomalies_with_a_chart(analysis_results_dict)

        anomaly_df = analysis_results_dict['df_count']
        post_results(anomaly_df)

    if len(data_fifo) < analysisWindow_size:
        print("not enough data to analyze. Finishing analysis")


    exit()

    # streamed_queue = deque(maxlen=analysisWindow_size)

    # in the first run, the increment should be enough to fill the window frame for the analysis
    # so we provide the maxlen of the queue as the increment.
    stream_data(streamed_queue, data_list, increment=analysisWindow_size) 

    csv_data = queue_to_csv(streamed_queue, csv_headers)
    dataFrame = pd.read_csv(csv_data)
    anomalyResults = zscore_anomaly_detection(dataFrame, anomaly_count_df)
    anomaly_count_df = anomalyResults['df_count']

    print(dataFrame)
    print(dataFrame.info())
    validate_anomalies_with_a_chart(anomalyResults)

    while len(data_list) > 0: 
        stream_data(streamed_queue, data_list, increment) 

        csv_data = queue_to_csv(streamed_queue, csv_headers)
        dataFrame = pd.read_csv(csv_data)
        anomalyResults = zscore_anomaly_detection(dataFrame, anomaly_count_df)
        anomaly_count_df = anomalyResults['df_count']

        print(dataFrame)
        print(dataFrame.info())
        validate_anomalies_with_a_chart(anomalyResults)

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


# validate_anomalies_with_a_chart(anomaly_df, spd_mean, spd_std, anomaly_count)

##########################################
# 4. Code Submission
##########################################
# outside of the .py file

if __name__ == "__main__":
    main()