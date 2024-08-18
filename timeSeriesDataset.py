import requests
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt


def receive_data(url):
    """ Receive all the data"""
    response = requests.get(url, stream=True)
    response.raise_for_status() # check for errors

    data = []
    for line in response.iter_lines():
        if line:
            data.append(line.decode('utf-8'))
        
    return data


# def stream_data(increment=2, queue_size=10):



def receive_data_in_chunks(desiredChunkSize=200):
    """Simulates a stream of continuous data"""

    chunk = []

    url = 'https://docs.google.com/spreadsheets/d/19galjYSqCDf6Ohb0IWv6YsRL7MV0EPFpN-2blGGS97U/pub?output=csv'
    response = requests.get(url, stream=True)

    for line in response.iter_lines():
        if line:
            chunk.append(line.decode('utf-8'))
        if len(chunk) >= desiredChunkSize:
            break

    return chunk


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
csv_data = "\n".join(receive_data(url))
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