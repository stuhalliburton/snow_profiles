import os
import numpy as np
import pandas as pd

from keras.layers import Dense
from keras.models import Sequential, Model

label_name = 'hazard_rating'
encoded_feature_count = 8

class AutoEncoder:
    def __init__(self, encoding_dim=encoded_feature_count):
        self.encoding_dim = encoding_dim
        dataset = pd.read_csv('data/parsed.csv', dtype=float)
        features = np.array(dataset.drop([label_name], 1))
        self.features = features
        self.feature_count = features.shape[1]

    def _encoder(self):
        model = Sequential()
        model.add(Dense(self.encoding_dim, input_dim=self.feature_count, activation='relu'))
        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
        self.encoder = model

    def _decoder(self):
        model = Sequential()
        model.add(Dense(self.feature_count, input_dim=self.encoding_dim, activation='relu'))
        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
        self.decoder = model

    def auto_encode(self):
        self._encoder()
        self._decoder()

        model = Sequential()
        model.add(self.encoder)
        model.add(self.decoder)
        model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
        self.model = model

    def fit(self, batch_size=50, epochs=300):
        self.model.fit(self.features, self.features, epochs=epochs, batch_size=batch_size)

    def save(self):
        if not os.path.exists('./saved_models'):
            os.mkdir('./saved_models')
        else:
            self.encoder.save('./saved_models/encoder_weights.h5')
            self.decoder.save('./saved_models/decoder_weights.h5')
            self.model.save('./saved_models/ae_weights.h5')

if __name__ == '__main__':
    ae = AutoEncoder()
    ae.auto_encode()
    # print ae.encoder.predict(ae.features[:1])
    ae.fit()
    ae.save()
