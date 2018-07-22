import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy

num_classes = 5
epoch = 100
batch_size = 10

dataset = numpy.loadtxt("data/parsed.csv", delimiter=",")
x_train = dataset[:,1:28]
y_train = dataset[:,28]

y_train = keras.utils.to_categorical(y_train, num_classes)

model = Sequential()
model.add(Dense(12, input_dim=27, kernel_initializer="uniform", activation="relu"))
model.add(Dense(28, kernel_initializer="uniform", activation="relu"))
model.add(Dense(14, kernel_initializer="uniform", activation="relu"))
model.add(Dense(5, kernel_initializer="uniform", activation="softmax"))

#opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)
#model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
model.compile(loss="categorical_crossentropy", optimizer="rmsprop", metrics=["accuracy"])


model.fit(x_train, y_train, epochs=epoch, batch_size=batch_size)

scores = model.evaluate(x_train, y_train)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

scores = model.evaluate(x_train, y_train)
print("Test loss:", scores[0])
print("Test accuracy:", scores[1])
