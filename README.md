# Robot Speed Anomaly Detection
This project aims to detect anomalies in the speed sensor readings of a real robot in real time.
- **Data**: The speed sensor readings are served through an online CSV file. The data is parsed using a queue, in a way that it can be applied to continuous data streams (real time readings). Data is fetched in chunks from the queue and analyzed.
- **Analysis**: The anomalies are detected through a Z-score analysis.
- **Validation**: The timestamp of each anomaly is recorded and charts are plotted for validation. In the charts we can see that when the speed reading is too high or too low, it is highlighted as an anomaly.
- **Results**: This analysis concluded that not all anomalies might be issues with the sensor or with the reading process, but they should be flagged anyway and used for further studies.

![image](https://github.com/user-attachments/assets/f651ada4-c5df-409a-b94c-c7634fa794d8)


## Instructions:
1. clone the repository
2. Build the image with the command: `docker build -t my_anomaly_detection_image .`
3. **Important:** Run the app with the -v option and provide a path for the app's outputs. E.g (Only Replace `your/output/path`): `docker run --name my_anomaly_detection_container -v your/output/path:/usr/src/app my_anomaly_detection_image`.
4. Stop the image with the commands `docker stop my_anomaly_detection_container` followed by `docker rm my_anomaly_detection_container` before running the app again.
5. Check the results on the log printed on the screen and the .png images on the path you provided on step3.

## Code explanation
Here's the flowchart of how the code runs:

![flowchart](https://github.com/user-attachments/assets/dc0f75c3-9f7c-4610-a39d-a29a48c7bc80)


## Objectives
### 1. Stream Data
Given that the data endpoint was a static .csv file, I had to simulate a constant stream using a queue. In a real situation, an async function would receive the data and fill an async queue. The main code would verify the queue constantly for new data.
![image](https://github.com/user-attachments/assets/988645c3-7801-4da7-a92e-91eaa9c69134)

### 2. Anomaly Detection
Straightforward static analysis was performed with the Z-score (Standard score method). That means, speed values too far away from the standard deviation were flagged as anomalies.
I got better results with the threshold at 5. So that only really high or low values were flagged. E.g:

![speed_data_with_anomalies_2](https://github.com/user-attachments/assets/58366cd6-dff4-49bb-927e-78553f2a90fe)


### 3. Metrics Reporting
I had two conclusions during this:
- The high speed values recognized as anomalies by my code might be acceptable as real sensor readings, because the data in the neighborhood show the speed increasing and decreasing. Anyway, they should be tagged as an anomaly because they are suspicious.
- Negative values are certainly an anomaly.

Now, to reach this conclusion, I used two outputs for metrics and validation: Tables and charts.

![dataValidation_v2](https://github.com/user-attachments/assets/28364393-6201-4d9b-bf80-8fb256ab9a34)


#### 1. Tables: Printed logs of the anomalies identified and their timestamps
All the anomalies and their timestamps are logged in the output screen. Since the analysis is performed multiple times until it goes through all the data, multiple tables will be printed (please check the number of the analysis in the beginning of the table output). The tables present columns "timestamp", "speed" and "Z-score".
#### 2. Charts
Some images(.png) will be saved in the app's root folder. They represent the speed reading, and the anomalies are highlighted. In the upper right corner the mean, std deviation, and anomaly count are present. These charts serve as the validation step, where we can see if the anomalies make sense. Again, multiple images will be there, check the filename to find out the corresponding analysis number.

![images_saved_in_root](https://github.com/user-attachments/assets/4264a3f6-77d7-4f21-b13a-51f378a8926e)

### 4. Code Submission
This repository with a complete readme.md and a dockerized solution.

## Considerations:
- There's room for improvements in the code: input validations in the functions, more modularization (maybe with OOP), unit tests, infrastructure as code (build the docker image and maybe a flask server for POST), etc.
- *Optional:* Edit the analysis parameters by changing the `analysis_window_size` and the `analysis_threshold` in _timeSeriesDataset.py_ file. The results might be misleading if the analysis window or the threshold are too small.
