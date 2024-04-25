from gameAI import Game

# TODO:
# - implementacja agenta jak w książce
# input: ptak ponad, ptak na wysokosci i ptak pod - dziura, predkosc, odleglosc od nastepnej przeszkody (n = 5)
# output: kliknac up albo nie (n = 2)
# reward: +5 za kazda rure, -5 za smierc

class Agent:

    def __init__(self, episodes=300):

        self.episodes = episodes
        
        self.epsilon = 1.0
        self.epsilon_min = 0.02

        self.epsilon_decay = self.epsilon_min / self.epsilon
        self.epsilon_decay = self.epsilon_decay ** (1.0/float(self.episodes))

