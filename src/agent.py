from gameAI import Game
from model import Model
from ploting import plot
import tensorflow as tf
import numpy as np
import random

# TODO:
# - implementacja agenta jak w książce
# input: ptak ponad, ptak na wysokosci i ptak pod - dziura, predkosc, odleglosc od nastepnej przeszkody (n = 5)
# output: kliknac up albo nie (n = 2)
# reward: +5 za kazda rure, -5 za smierc

class Agent:

    def __init__(self, episodes=300):

        self.episodes = episodes

        self.memory = []
        
        self.gamma = 0.9

        self.epsilon = 1.0
        self.epsilon_min = 0.02

        self.epsilon_decay = self.epsilon_min / self.epsilon
        self.epsilon_decay = self.epsilon_decay ** (1.0/float(self.episodes))

        self.Q_model = Model(5, 2).build_model()
        self.Q_model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam())
        self.target_Q_model = Model(5,2).build_model()

        self.update_weights()

        self.replay_counter = 0
        self.n_games = 0

    def update_weights(self):
        self.target_Q_model.set_weights(self.Q_model.get_weights())

    def get_target_Q_value(self, next_state, reward):
        
        q_value = np.amax(self.target_Q_model.predict(next_state)[0])
        q_value *= self.gamma
        q_value += reward
        
        return q_value

    def move(self, state):

        if np.random.rand() < self.epsilon:
            return np.random.choice([0,1])
        
        q_values = self.Q_model.predict(state)
        move = np.argmax(q_values[0])

        return move
    
    def remember(self, state, action, next_state, reward, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):

        sars = random.sample(self.memory, k=batch_size)
        states, Q_values = [], []

        for state, action, reward, next_state, done in sars:

            state_Q_values = self.Q_model.predict(state)

            state_Q_value = self.get_target_Q_value(next_state, reward)

            state_Q_values[0][action] = reward if done else state_Q_value

            states.append(state[0])
            Q_values.append(state_Q_values[0])
        
        self.Q_model.fit(np.array(states),
                         np.array(Q_values),
                         batch_size=batch_size,
                         epochs=1,
                         verbose=0)
        
        self.update_epsilon()

        if self.replay_counter % 10 == 0:
            self.update_weights()
        
        self.replay_counter += 1

    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

def train():
    episodes = 500
    game = Game()
    agent = Agent(episodes)

    record = 0
    total_score = 0

    plot_scores = []
    plot_mean_scores = []

    for ep in range(episodes):
    
        done = False
        
        while not done:

            state = game.get_state()

            move = agent.move(state)
            print(move)

            done, score, reward = game.play_step(move)

            next_state = game.get_state()

            agent.remember(state, move, next_state, reward, done)

        if len(agent.memory) >= 100000:
            agent.replay(100000)

        if score > record:
            record = score

        game.reset()
        agent.n_games += 1

        print('Game:', agent.n_games, 'Score:', score, 'Record:', record)

        plot_scores.append(score)
        total_score += score

        mean_score = total_score / agent.n_games
        plot_mean_scores.append(mean_score)

        plot(plot_scores, plot_mean_scores)
            
if __name__ == '__main__':
    train()