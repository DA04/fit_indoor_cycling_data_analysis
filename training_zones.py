# import libraries
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# connect to the data
conn = psycopg2.connect(host="localhost", database="garmin_data", user="postgres", password="******")

# fit file session data with ftp
data = pd.read_sql_query("""select * from (select session.activity_id, session.timestamp, session.avg_heart_rate, session.avg_power, 
session.total_timer_time/3600 as time,
test.power_threshold, test.timestamp as test_timestamp,
rank() over (partition by session.activity_id order by session.activity_id, test.timestamp desc) as ftp_rank
from session cross join test
where sub_sport = 'virtual_activity' and avg_heart_rate > 90
and session.timestamp > '2020-12-26' and session.timestamp >= test.timestamp
and record.activity_id not in (109983788203, 110771005101, 111376595537, 111494782478)
order by session.activity_id) a
where a.ftp_rank = 1""", conn)

activity_ftp = data[['activity_id', 'power_threshold']]

# fit file record data
record_data = pd.read_sql_query("""select record.record_id, record.activity_id, record.timestamp, record.heart_rate, 
record.cadence, record.power
from record join session on record.activity_id = session.activity_id
where record.timestamp >= '2020-12-26' and session.sub_sport = 'virtual_activity' and record.power > 0 
and record.activity_id not in (109983788203, 110771005101, 111376595537, 111494782478)
order by timestamp asc
""", conn)

record_data = pd.merge(record_data, activity_ftp, on='activity_id', how='inner')
record_data['percent_power'] = round(record_data['power']/record_data['power_threshold']*100.00)

# training zones calculation - https://www.highnorth.co.uk/articles/cycling-training-zones
def zone(row):
    if row['percent_power'] <= 55:
        val = 1
    elif row['percent_power'] > 55 and row['percent_power'] <=75:
        val = 2
    elif row['percent_power'] > 75 and row['percent_power'] <=90:
        val = 3
    elif row['percent_power'] > 90 and row['percent_power'] <=105:
        val = 4
    elif row['percent_power'] > 105 and row['percent_power'] <=120:
        val = 5
    elif row['percent_power'] > 120 and row['percent_power'] <=130:
        val = 6
    elif row['percent_power'] > 130:
        val = 7
    else:
        val = 0
    return val

# cadence zone calculation
def cadence(row):
    if row['cadence'] >= 45 and row['cadence'] < 65:
        val = 1
    elif row['cadence'] >=85 and row['cadence'] <= 95:
        val = 2
    elif row['cadence'] > 95:
        val = 3
    else:
        val = 0
    return val

# data pivoting for training and cadence zones ratio
record_data['zone'] = record_data.apply(zone, axis=1)
record_data['cadence_zone'] = record_data.apply(cadence, axis=1)
cadence_pivot = pd.pivot_table(record_data, index = ['activity_id', 'cadence_zone'], values = ['cadence'], aggfunc='count')
cadence_pivot = cadence_pivot.reset_index()

cadence_pivot['record_count'] = cadence_pivot.groupby('activity_id')['cadence'].transform('sum')
cadence_pivot['cadence'] = round(cadence_pivot.cadence/cadence_pivot.record_count*100.00)
cadence_pivot = cadence_pivot[['activity_id', 'cadence_zone', 'cadence']]
cadence_pivot['cadence_zone_desc'] = cadence_pivot.apply(lambda row: 'cadence_zone_'+str(int(row['cadence_zone'])), axis=1)
cadence_zone = pd.pivot_table(cadence_pivot, index=['activity_id'], values='cadence', columns='cadence_zone_desc')
cadence_zone = cadence_zone.reset_index()

record_pivot = pd.pivot_table(record_data, index = ['activity_id', 'zone'], values = ['percent_power'], aggfunc='count')
record_pivot = record_pivot.reset_index()
record_pivot['record_count'] = record_pivot.groupby('activity_id')['percent_power'].transform('sum')
record_pivot['percent_zone'] = round(record_pivot.percent_power/record_pivot.record_count*100.00)
record_pivot = record_pivot[['activity_id', 'zone', 'percent_zone']]

record_pivot['zone_desc'] = record_pivot.apply(lambda row: 'zone_'+str(int(row['zone'])), axis=1)
training_zone = pd.pivot_table(record_pivot, index=['activity_id'], values='percent_zone', columns='zone_desc')
training_zone = training_zone.reset_index()

# data merge
data = pd.merge(data, training_zone, on='activity_id', how='inner')
data = pd.merge(data, cadence_zone, on='activity_id', how='inner')
data = data.fillna(0)

# time column normalization
data['time_n'] = data.apply(lambda row: round((row['time']-min(data['time']))/(max(data['time'])-min(data['time']))*100.00), axis=1)

# export dataframe
data.to_csv('power_zones_data_7.csv')