import requests
import pandas as pd
from io import StringIO
from collections import deque
import matplotlib.pyplot as plt


def receive_data_and_queue_it(url):
    """ Receive all the data and puts it in a FIFO queue, to simulate a continuous stream."""

    response = requests.get(url, stream=True)
    response.raise_for_status() # check for errors

    queue = deque()
    for line in response.iter_lines():
        if line:
            queue.append(line.decode('utf-8'))
        
    return queue


def list_to_csv(list, headers):
    """ Prepares a list to become a csv, to be read by pandas."""
    
    csv = headers + "\n" + "\n".join(list)
    return StringIO(csv)


def simulate_continuous_data(data_source, window_size):
    """ Simulates a continuous data stream by taking only part of the data available in the queue."""

    window = []
    for _ in range(window_size):
        new_data = data_source.popleft()
        window.append(new_data)
    return window


def anomaly_detection(dataFrame, threshold):
    """ Detects anomalies."""

    anomalies_output = detect_anomalies_zscore(dataFrame, threshold)
    anomaly_df = anomalies_output[0]
    spd_mean = anomalies_output[1]
    spd_std = anomalies_output[2]
    anomaly_count = anomaly_df['Anomaly'].sum()
    anomalies_df_count = anomalies_output[3]

    return {'anomaly_df': anomaly_df,
             'mean': spd_mean,
             'std': spd_std,
             'count': anomaly_count,
             'df_count': anomalies_df_count}


def detect_anomalies_zscore(df, threshold=5):
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
    """ Plotting the data and highlighting the anomalies with additional metrics. """

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

    print(anomalyResults['df_count'])
    print(anomalyResults['df_count'].info())

    # Show the plot and wait for it to be closed
    plt.show()

    # show the plot and hold it for some seconds
    # plt.draw()
    # plt.pause(10)
    # plt.close()


def post_results(anomaly_df):
    """ Simulate a POST request to a flask server"""
    # to do: 

    pass


def main():
    url = "https://docs.google.com/spreadsheets/d/19galjYSqCDf6Ohb0IWv6YsRL7MV0EPFpN-2blGGS97U/pub?output=csv"

    analysisWindow_size = 50000
    analysis_threshold = 5

    data_fifo = receive_data_and_queue_it(url)
    csv_headers = data_fifo.popleft()
    
    while len(data_fifo) > analysisWindow_size:
        analysis_window_list = simulate_continuous_data(data_fifo, analysisWindow_size)
        analysis_windos_csv = list_to_csv(analysis_window_list, csv_headers)
        analysis_window_df = pd.read_csv(analysis_windos_csv)

        analysis_results_dict = anomaly_detection(analysis_window_df, analysis_threshold)
        validate_anomalies_with_a_chart(analysis_results_dict)

        anomaly_df = analysis_results_dict['df_count']
        post_results(anomaly_df)

    if len(data_fifo) < analysisWindow_size:
        print("not enough data to analyze. Finishing analysis")

    exit()

if __name__ == "__main__":
    main()