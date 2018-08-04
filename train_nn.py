import numpy as np
import pandas as pd

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import TensorBoard
from keras.utils import to_categorical
from sklearn import cross_validation

num_classes = 5
label_name = 'hazard_rating'
epoch = 1000
batch_size = 20
test_ratio = 0.1
dropout_ratio = 0.
feature_count = 49
tbCallBack = TensorBoard(log_dir='./log', histogram_freq=0, write_graph=True, write_images=True)

# load parses CSV and randomise
# dataset = np.loadtxt("data/parsed.csv", delimiter=",")
dataset = pd.read_csv('data/parsed.csv', dtype=float)

# split features & labels
features = np.array(dataset.drop([label_name], 1))
labels = np.array(dataset[label_name])

# categorise labels
labels = to_categorical(labels, num_classes)

# split training from test data
x_train, x_test, y_train, y_test = cross_validation.train_test_split(features,
        labels, test_size=test_ratio)

model = Sequential()
model.add(Dense(50, input_dim=feature_count, activation="relu"))
model.add(Dropout(dropout_ratio))
model.add(Dense(50, activation="relu"))
model.add(Dropout(dropout_ratio))
model.add(Dense(50, activation="relu"))
model.add(Dropout(dropout_ratio))
model.add(Dense(num_classes, activation="softmax"))

#opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)
#model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
model.compile(loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

model.fit(x_train, y_train,
  epochs=epoch,
  batch_size=batch_size,
  validation_split=0.1,
  callbacks=[tbCallBack])

scores = model.evaluate(x_test, y_test)
print("Test loss:", scores[0])
print("Test accuracy:", scores[1])

import operator

print "\nLow Test"
low_test = dataset.loc[dataset[label_name] == 0]
print low_test[:1]
low_features = low_test[:1].drop([label_name], 1)
predictions = model.predict(low_features)
(prediction, confidence) = max(enumerate(predictions[0]), key=operator.itemgetter(1))
print 'Prediction: {}, Confidence: {}'.format(prediction, confidence)

print "\nModerate Test"
moderate_test = dataset.loc[dataset[label_name] == 1]
print moderate_test[:1]
moderate_features = moderate_test[:1].drop([label_name], 1)
predictions = model.predict(moderate_features)
(prediction, confidence) = max(enumerate(predictions[0]), key=operator.itemgetter(1))
print 'Prediction: {}, Confidence: {}'.format(prediction, confidence)

print "\nConsiderable Test"
considerable_test = dataset.loc[dataset[label_name] == 2]
print considerable_test[:1]
considerable_features = considerable_test[:1].drop([label_name], 1)
predictions = model.predict(considerable_features)
(prediction, confidence) = max(enumerate(predictions[0]), key=operator.itemgetter(1))
print 'Prediction: {}, Confidence: {}'.format(prediction, confidence)

print "\nHigh Test"
high_test = dataset.loc[dataset[label_name] == 3]
print high_test[:1]
high_features = high_test[:1].drop([label_name], 1)
predictions = model.predict(high_features)
(prediction, confidence) = max(enumerate(predictions[0]), key=operator.itemgetter(1))
print 'Prediction: {}, Confidence: {}'.format(prediction, confidence)

print "\nExtreme Test"
extreme_test = dataset.loc[dataset[label_name] == 4]
print extreme_test[:1]
extreme_features = extreme_test[:1].drop([label_name], 1)
predictions = model.predict(extreme_features)
(prediction, confidence) = max(enumerate(predictions[0]), key=operator.itemgetter(1))
print 'Prediction: {}, Confidence: {}'.format(prediction, confidence)
