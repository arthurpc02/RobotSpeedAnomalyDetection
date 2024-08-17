import requests
import pandas as pd
from io import StringIO

##########################################
# 1. Stream Data
##########################################
def receiveDataInChunks(desiredChunkSize=10):
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

print(receiveDataInChunks())

# csv = stream.content

# dataset = pd.read_csv(StringIO(stream.text))



##########################################
# 2. Anomaly Detection
##########################################


##########################################
# 3. Metrics Reporting
##########################################


##########################################
# 4. Code Submission
##########################################

# print(dataset)
# print(dataset.info())