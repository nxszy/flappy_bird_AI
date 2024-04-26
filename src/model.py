import tensorflow as tf
import numpy as np

class Model:

    def __init__(self, n_inputs, n_outputs, save_file):

        self.n_in = n_inputs
        self.n_out = n_outputs

        self.Q_model = self.build_model()

        self.save_file = save_file

    def build_model(self):

        inputs = tf.keras.Input(shape=(self.n_in,), name='state')
        x = tf.keras.layers.Dense(256, activation='relu')(inputs)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        x = tf.keras.layers.Dense(self.n_out, activation='linear', name='action')(x)

        model = tf.keras.Model(inputs, x)
        model.summary()

        return model
    
    def save_model(self):
        self.Q_model.save_weights(self.save_file)