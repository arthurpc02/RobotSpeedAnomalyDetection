import requests
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
%matplotlib inline

def receive_data_in_chunks(desiredChunkSize=1000):
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
    
    return pd.DataFrame({'Data': data, 'Z-Score': z_scores, 'Anomaly': anomalies})


def plot_data_with_anomalies(data):
    """ Plotting the data and  highlighting the anomalies """

    plt.figure(figsize=(14, 7))
    plt.plot(dataFrame.index, anomaly_df['Data'], label='Speed Data', color='blue')

    # Highlight anomalies
    plt.scatter(anomaly_df.index[anomaly_df['Anomaly']], 
                anomaly_df['Data'][anomaly_df['Anomaly']], 
                color='red', label='Anomalies', marker='o')

    # Adding labels and title
    plt.title('Robot Speed Data with Anomalies Highlighted')
    plt.xlabel('Index')
    plt.ylabel('Speed')
    plt.legend()

    # Show the plot
    plt.show()


##########################################
# 1. Stream Data
##########################################

csv_data = "\n".join(receive_data_in_chunks())
dataFrame = pd.read_csv(StringIO(csv_data))

##########################################
# 2. Anomaly Detection
##########################################

anomaly_df = detect_anomalies_zscore(dataFrame['speed'])
anomaly_count = anomaly_df['Anomaly'].sum()



##########################################
# 3. Metrics Reporting
##########################################

plot_data_with_anomalies(anomaly_df)

print(dataFrame)
print(dataFrame.info())

# print(anomaly_df)
# print(anomaly_df.info())
print(f'anomaly count: {anomaly_count}')


##########################################
# 4. Code Submission
##########################################
# outside of the .py file