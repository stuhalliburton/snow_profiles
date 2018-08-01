import keras
from keras.layers import Input, Dense
from keras.models import Model, load_model
import numpy
import os

class AutoEncoder:
    def __init__(self, feature_count=23, encoding_dim=5):
        self.feature_count = feature_count
        self.encoding_dim = encoding_dim
        dataset = numpy.loadtxt("data/parsed.csv", delimiter=",")
        features = dataset[:, 0:feature_count]
        features = features / numpy.linalg.norm(features)
        self.features = features

    def _encoder(self):
        inputs = Input(shape=self.features[0].shape)
        encoded = Dense(self.encoding_dim, activation='relu')(inputs)
        model = Model(inputs, encoded)
        self.encoder = model
        return model

    def _decoder(self):
        inputs = Input(shape=(self.encoding_dim,))
        decoded = Dense(self.feature_count, activation='relu')(inputs)
        model = Model(inputs, decoded)
        self.decoder = model
        return model

    def encoder_decoder(self):
        self._encoder()
        self._decoder()

        inputs = Input(shape=self.features[0].shape)
        ec_out = self.encoder(inputs)
        dc_out = self.decoder(ec_out)
        model = Model(inputs, dc_out)

        self.model = model

    def fit(self, batch_size=10, epochs=300):
        self.model.compile(optimizer='sgd', loss='mse', metrics=['accuracy'])
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
    ae.encoder_decoder()
    ae.fit(batch_size=50, epochs=300)
    ae.save()

    print ae.encoder.predict(ae.features[:1])
