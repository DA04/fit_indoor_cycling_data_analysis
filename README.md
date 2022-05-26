# Virtual Cycling data analysis

I have detailed tutorial article published in Russian here https://habr.com/ru/post/661067/

All the datasets are based on the parsed FIT files. You can find more details and DB schema in this repo https://github.com/DA04/fitness_tracker_data_parsing

<h2>One training chart</h2>

The script [one_training_chart.py](/one_training_chart.py) will help you to create a chart for one training with general virtual cycling activity metrics - <i>HR, Power</i> and <i>Cadence</i> - on the Time axis. There are two options in the script: raw data and modified data with the spline function. Choose any which will fit your purpose. See the difference on the pic below:

![OTC](/one_training_with_spline.png)

<h2>Training Zones calculation</h2>

The script [training_zones.py](/training_zones.py) will guide you through the steps to calculate training zones split for each training based on known Power Threshold. The source for the zones description is sourced from [here](https://www.highnorth.co.uk/articles/cycling-training-zones)

![TZ](/seven_training_zones.jpeg)

<h2>Trainings classification</h2>

I have used <i>Random Forest</i> method to classify the trainings having the dataset with the manually established samples of 37 activities. Several models are available in the [rf_classification.py](/rf_classification.py) script (see the commented out ones as well). The final model helped me to find similar trainings from the dataset. See the profiles for FTP-test sample:

![Similar](/similar_3.png)

The code for the chart of similar trainings is also available in the [similar_trainings_subplots.py](/similar_trainings_subplots.py) file.