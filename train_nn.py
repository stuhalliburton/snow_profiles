import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy

num_classes = 5
epoch = 1000
batch_size = 500
test_size = 200

dataset = numpy.loadtxt("data/parsed.csv", delimiter=",")
numpy.random.shuffle(dataset)
features = dataset[:, 0:25]
labels = dataset[:, 25]
labels = keras.utils.to_categorical(labels, num_classes)

x_train, x_test = features[test_size:], features[:test_size]
y_train, y_test = labels[test_size:], labels[:test_size]

model = Sequential()
model.add(Dense(625, input_dim=25, kernel_initializer="uniform", activation="relu"))
model.add(Dense(50, kernel_initializer="uniform", activation="relu"))
model.add(Dense(5, kernel_initializer="uniform", activation="softmax"))

#opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)
#model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
model.compile(loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

model.fit(x_train, y_train, epochs=epoch, batch_size=batch_size, validation_split=0.1)

scores = model.evaluate(x_test, y_test)
print("Test loss:", scores[0])
print("Test accuracy:", scores[1])
