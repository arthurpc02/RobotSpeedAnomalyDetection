import requests
import pandas as pd
from io import StringIO

##########################################
# 1. Stream Data
##########################################
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

csv_data = "\n".join(receive_data_in_chunks())
dataFrame = pd.read_csv(StringIO(csv_data))



##########################################
# 2. Anomaly Detection
##########################################


##########################################
# 3. Metrics Reporting
##########################################


##########################################
# 4. Code Submission
##########################################

print(dataFrame)
print(dataFrame.info())