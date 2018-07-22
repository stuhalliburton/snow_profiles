import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy

num_classes = 5
epoch = 100
batch_size = 10

dataset = numpy.loadtxt("data/parsed.csv", delimiter=",")
x_train = dataset[:,0:25]
y_train = dataset[:,25]

y_train = keras.utils.to_categorical(y_train, num_classes)

model = Sequential()
model.add(keras.layers.normalization.BatchNormalization())
model.add(Dense(625, input_dim=25, kernel_initializer="uniform", activation="relu"))
model.add(Dense(625, kernel_initializer="uniform", activation="relu"))
model.add(Dense(5, kernel_initializer="uniform", activation="softmax"))

#opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)
#model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
model.compile(loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

model.fit(x_train, y_train, epochs=epoch, batch_size=batch_size, validation_split=0.1)

scores = model.evaluate(x_train, y_train)
print("Test loss:", scores[0])
print("Test accuracy:", scores[1])
