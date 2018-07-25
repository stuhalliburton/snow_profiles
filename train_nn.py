import keras
import numpy

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import TensorBoard

num_classes = 5
epoch = 5000
batch_size = 20
test_size = 50
dropout_ratio = 0.
feature_count = 23
tbCallBack = keras.callbacks.TensorBoard(log_dir='./log', histogram_freq=0, write_graph=True, write_images=True)

# load parses CSV and randomise
dataset = numpy.loadtxt("data/parsed.csv", delimiter=",")
numpy.random.shuffle(dataset)

# split features and normalise
features = dataset[:, 0:feature_count]
features = features / numpy.linalg.norm(features)

# split labels and categorise
labels = dataset[:, feature_count]
labels = keras.utils.to_categorical(labels, num_classes)

# split training from testing data
x_train, x_test = features[test_size:], features[:test_size]
y_train, y_test = labels[test_size:], labels[:test_size]

model = Sequential()
model.add(Dense(23, input_dim=feature_count, activation="relu"))
model.add(Dropout(dropout_ratio))
model.add(Dense(23, activation="relu"))
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

print x_test[:1]
print y_test[:1]
print model.predict(x_test[:1])
