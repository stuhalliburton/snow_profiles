import numpy as np
import pandas as pd

from keras.utils import to_categorical
from sklearn import neighbors
from sklearn.model_selection import train_test_split

label_name = 'hazard_rating'
num_classes = 5
test_ratio = 0.1
random_seed = 2

# load parses CSV and randomise
dataset = pd.read_csv('data/parsed.csv', dtype=float)

# split features & labels
features = np.array(dataset.drop([label_name], 1))
labels = np.array(dataset[label_name])

# categorise labels
labels = to_categorical(labels, num_classes)

# split training from test data
x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=test_ratio, random_state=random_seed)

knn = neighbors.KNeighborsClassifier(n_neighbors=5, p=1, algorithm='brute')
knn.fit(x_train, y_train)

accuracy = knn.score(x_test, y_test)
print 'Accuracy: {}'.format(accuracy)
