# Random Forest training classification
# https://www.datacamp.com/community/tutorials/random-forests-classifier-python

import pandas as pd
from sklearn import preprocessing

df = pd.read_csv('power_zones_data_label.csv', index_col=0)
df_train = df[df['label'].notnull()]
df_train['label'] = df_train['label'].astype(int)
df_train['zone_1_2'] = df_train['zone_1']+df_train['zone_2']
# df_train['zone_3_4'] = df_train['zone_3']+df_train['zone_4']
# df_train['zone_5_6'] = df_train['zone_5']+df_train['zone_6']
df_train['zone_4_6'] = df_train['zone_4']+df_train['zone_5']+df_train['zone_6']
df_train


# Import train_test_split function
from sklearn.model_selection import train_test_split

# options for input features below
# X=df_train[['time_n', 'zone_1', 'zone_2', 'zone_3', 'zone_4', 'zone_5', 'zone_6', 'cadence_zone_1', 'cadence_zone_2']]  # Features
# X=df_train[['time_n', 'zone_1', 'zone_2', 'zone_3', 'zone_4_6', 'cadence_zone_1', 'cadence_zone_2']]  # Features
# X=df_train[['time_n', 'zone_1_2', 'zone_3', 'zone_4_6', 'cadence_zone_1', 'cadence_zone_2']]  # Features
# X=df_train[['time_n', 'zone_1_2', 'zone_3_4', 'zone_5_6', 'cadence_zone_1', 'cadence_zone_2']]  # Features
# X=df_train[['time_n', 'zone_1_2', 'zone_3_4', 'zone_5_6', 'cadence_zone_1']]  # Features

# final option for input features chosen
X=df_train[['time_n', 'zone_1_2', 'zone_3', 'zone_4_6', 'cadence_zone_1']]  # Features
y=df_train['label']  # Labels

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% test

#Import Random Forest Model
from sklearn.ensemble import RandomForestClassifier

#Create a Gaussian Classifier
clf=RandomForestClassifier(n_estimators=100)

#Train the model using the training sets y_pred=clf.predict(X_test)
clf.fit(X,y)

y_pred=clf.predict(X_test)

#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# connect to the file
data = pd.read_csv('power_zones_data_label.csv', index_col=0)

data['zone_1_2'] = data['zone_1']+data['zone_2']
data['zone_4_6'] = data['zone_4']+data['zone_5']+data['zone_6']

# data['zone_3_4'] = data['zone_3']+data['zone_4']
# data['zone_5_6'] = data['zone_5']+data['zone_6']

# I=data[['time_n', 'zone_1', 'zone_2', 'zone_3', 'zone_4', 'zone_5', 'zone_6','cadence_zone_1', 'cadence_zone_2']]
# I=data[['time_n', 'zone_1', 'zone_2', 'zone_3', 'zone_4_6','cadence_zone_1', 'cadence_zone_2']]
# I=data[['time_n', 'zone_1_2', 'zone_3', 'zone_4_6','cadence_zone_1', 'cadence_zone_2']]
# I=data[['time_n', 'zone_1_2', 'zone_3_4', 'zone_5_6','cadence_zone_1', 'cadence_zone_2']]
# I=data[['time_n', 'zone_1_2', 'zone_3_4', 'zone_5_6','cadence_zone_1']]

# input and output features with prediction
I=data[['time_n', 'zone_1_2', 'zone_3', 'zone_4_6','cadence_zone_1']]
data['prediction'] = clf.predict(I)

# export dataframe
data.to_csv('random_forest_prediction.csv')