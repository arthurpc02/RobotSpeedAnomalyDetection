import requests
import pandas as pd
from io import StringIO
from collections import deque
import matplotlib.pyplot as plt
plot_counter = 0

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

    zscore_output = detect_anomalies_zscore(dataFrame, threshold)
    zscore_df = zscore_output[0]
    spd_mean = zscore_output[1]
    spd_std = zscore_output[2]
    anomaly_count = zscore_df['Anomaly'].sum()
    anomalies_df = zscore_output[3]

    return {'zscore_df': zscore_df,
             'mean': spd_mean,
             'std': spd_std,
             'count': anomaly_count,
             'anomaly_df': anomalies_df}


def detect_anomalies_zscore(df, threshold=5):
    """
    Detect anomalies using the Z-score method.
    
    Parameters:
    - df: A pandas DataFrame containing the time-series data.
    - threshold: Z-score threshold for detecting anomalies.
    
    Returns:
    - zscore_df: A DataFrame with the original columns plus an additional 'Anomaly' column.
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
    zscore_df = df.copy()
    zscore_df['Z-Score'] = z_scores
    zscore_df['Anomaly'] = anomalies

    return zscore_df, mean, std, anomalies_with_timestamp_df


def validate_anomalies_with_a_chart(anomalyResults):
    """ Plotting the data and highlighting the anomalies with additional metrics. """

    data = anomalyResults['zscore_df']
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
    global plot_counter
    plot_counter += 1
    plt.savefig(f'speed_data_with_anomalies_{plot_counter}.png')


    print("################################# ")
    print(f"This is the analysis number {plot_counter}: ")
    print(anomalyResults['anomaly_df'])
    print(anomalyResults['anomaly_df'].info())

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

    analysisWindow_size = 100000
    analysis_threshold = 5

    url = "https://docs.google.com/spreadsheets/d/19galjYSqCDf6Ohb0IWv6YsRL7MV0EPFpN-2blGGS97U/pub?output=csv"
    data_fifo = receive_data_and_queue_it(url)
    csv_headers = data_fifo.popleft()
    
    while len(data_fifo) > analysisWindow_size:
        analysis_window_list = simulate_continuous_data(data_fifo, analysisWindow_size)
        analysis_windos_csv = list_to_csv(analysis_window_list, csv_headers)
        analysis_window_df = pd.read_csv(analysis_windos_csv)

        analysis_results_dict = anomaly_detection(analysis_window_df, analysis_threshold)
        validate_anomalies_with_a_chart(analysis_results_dict)

        anomaly_df = analysis_results_dict['anomaly_df']
        post_results(anomaly_df)

    if len(data_fifo) < analysisWindow_size:
        print("Finishing analysis: not enough data to analyze. ")
        print(f"Check the app folder for the {plot_counter} .png images generated for validation.")

    exit()

if __name__ == "__main__":
    main()