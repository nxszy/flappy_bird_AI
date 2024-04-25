from multiprocessing import Pool
import matplotlib.pyplot as plt
from gameAI import Game
from agent import Agent

def train_agent(agent_id, episodes=500):
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
            done, score, reward = game.play_step(move)
            next_state = game.get_state()
            agent.remember(state, move, next_state, reward, done)

        if len(agent.memory) >= 32:
            agent.replay(32)

        if score > record:
            record = score

        game.reset()
        agent.n_games += 1

        print('Agent:', agent_id, 'Game:', agent.n_games, 'Score:', score, 'Record:', record)

        plot_scores.append(score)
        total_score += score
        mean_score = total_score / agent.n_games
        plot_mean_scores.append(mean_score)

    return plot_scores, plot_mean_scores

def plot_results(results):
    for i, result in enumerate(results):
        plot_scores, plot_mean_scores = result
        plt.plot(plot_scores, label=f'Agent {i+1} Score')
        plt.plot(plot_mean_scores, label=f'Agent {i+1} Mean Score')

    plt.title('Training Scores and Mean Scores of Agents')
    plt.xlabel('Episodes')
    plt.ylabel('Score')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    num_agents = 3
    with Pool(num_agents) as p:
        results = p.map(train_agent, range(1, num_agents+1))
    plot_results(results)
