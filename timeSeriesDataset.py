import requests
import pandas as pd

##########################################
# 1. Stream Data
stream = requests.get('https://docs.google.com/spreadsheets/d/19galjYSqCDf6Ohb0IWv6YsRL7MV0EPFpN-2blGGS97U/pub?output=csv')
print(stream.status_code)
print(stream.headers)
csv = stream.content

# dataset = pd.read_csv(stream)
# print(dataset)
# https://docs.google.com/spreadsheets/d/19galjYSqCDf6Ohb0IWv6YsRL7MV0EPFpN-2blGGS97U/pub?output=csv


##########################################
# 2. Anomaly Detection



##########################################
# 3. Metrics Reporting



##########################################
# 4. Code Submission