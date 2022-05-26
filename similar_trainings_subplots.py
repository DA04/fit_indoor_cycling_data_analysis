# import libraries
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# connect to the dataset
df = pd.read_csv('power_zones_data_rf_comparison.csv', index_col=0)
df = df[['activity_id', 'training_type']]
training_3 = df.loc[df['training_type']==3]
list_3 = training_3['activity_id'].to_list()

conn = psycopg2.connect(host="localhost", database="garmin_data", user="postgres", password="*****")

# generate a chart for each training from the list_3
for i in range(5):
    activity_id = list_3[i]
    df = pd.read_sql_query("""select timestamp, heart_rate, cadence, power from record 
                 where activity_id ={} order by timestamp asc""".format(activity_id), conn)
    df['sec'] = (df['timestamp']-min(df['timestamp'])).dt.total_seconds()/60
    plt.subplot(2,3,i+1)
    plt.plot(df.sec, df.power)
    plt.title(min(df['timestamp']).date())
    plt.xlim(0, 60)
    plt.ylim(0,450)
    plt.xlabel('time, min')
    plt.ylabel('power, watts')
plt.rcParams['figure.figsize'] = [20, 10]
plt.show()