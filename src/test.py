from gameAI import Game
from agent import Agent
from ploting import plot

def test():
    game = Game()
    agent = Agent()

    agent.epsilon = -1
    agent.set_weights('model2.weights.h5')

    record = 0
    total_score = 0

    plot_scores = []
    plot_mean_scores = []

    for _ in range(10):
    
        done = False
        
        while not done:

            state = game.get_state()

            move = agent.move(state)

            done, score, reward = game.play_step(move)

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
    
test()