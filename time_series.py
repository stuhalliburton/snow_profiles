import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense, LSTM

file_name = 'profiles/southern-cairngorms.csv'
label_header = 'Observed aval. hazard'
temp_gradient = 'Max Temp Grad'
features = [label_header, temp_gradient]
feature_count = len(features)
look_back = 7
test_ratio = 0.

def numerical_labels(data):
    if data == 'Low':
        return 0
    if data == 'Moderate':
        return 1
    if data == 'Considerable -':
        return 2
    if data == 'Considerable +':
        return 3
    if data == 'High':
        return 4

def create_dataset(dataset, look_back=1):
    x, y = [], []
    for index, value in enumerate(dataset):
        try:
            current_index = index + 1
            dataframe_index = current_index + 1
            look_back_index = dataframe_index + look_back
            if look_back_index > len(dataset):
                raise IndexError
            previous = dataset[dataframe_index:look_back_index]
            prediction = dataset[current_index][0]
            x.append(previous)
            y.append(prediction)
        except IndexError:
            pass

    return np.array(x), np.array(y)

# load CSV data
dataset = pd.read_csv(file_name, index_col=False)

# drop null row and add numerical labels
dataset = dataset.dropna(subset=features)
dataset[label_header] = dataset[label_header].apply(numerical_labels)

# select feature values
dataset = dataset[features].values

# split train / test data
train, test = train_test_split(dataset, test_size=test_ratio, shuffle=False)

# create time seriesed dataset and reshape
x_train, y_train = create_dataset(train, look_back=look_back)
x_train = x_train.reshape(x_train.shape[0], 1, look_back*feature_count)
# x_test, y_test = create_dataset(test, look_back=look_back)
# x_test = x_test.reshape(x_test.shape[0], 1, look_back*feature_count)

# specify model and compile
model = Sequential()
model.add(LSTM(128, activation='relu', input_shape=x_train[0].shape))
model.add(Dense(1, activation='linear'))
model.compile(loss='mse', optimizer='adam')

# fit model to dataset
model.fit(x_train, y_train, epochs=50, batch_size=1, validation_split=0.05)

# make predictions
train_predict = model.predict(x_train)
# test_predict = model.predict(x_test)

plt.plot(y_train, label='y_train')
plt.plot(train_predict, label='train_predict')
# plt.plot(y_test, label='y_test')
# plt.plot(test_predict, label='test_predict')
plt.legend()
plt.show()
