import tensorflow as tf
import numpy as np

class Model:

    def __init__(self, n_inputs, n_outputs):

        self.n_in = n_inputs
        self.n_out = n_outputs

        self.Q_model = self.build_model()

    def build_model(self):

        inputs = tf.keras.Input(shape=(self.n_in,), name='state')
        x = tf.keras.layers.Dense(256, activation='relu')(inputs)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        x = tf.keras.layers.Dense(self.n_out, activation='linear', name='action')(x)

        model = tf.keras.Model(inputs, x)
        model.summary()

        return model


    def get_Q_value(self, next_state, reward):
        
        q_value = np.amax(self.Q_model.predict(next_state)[0])
        q_value *= self.gamma
        q_value += reward
        
        return q_value