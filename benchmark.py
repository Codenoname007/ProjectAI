# benchmark.py - Chạy benchmark và xuất results.csv + results.png (TOÀN BỘ CHÚ THÍCH TIẾNG VIỆT)
import time, os, csv
import matplotlib.pyplot as plt
from statistics import mean
from game import SnakeGame
from algorithms.bfs_agent import BFSAgent
from algorithms.astar_agent import AStarAgent
from algorithms.hill_agent import HillAgent
from algorithms.forward_agent import ForwardAgent

if os.path.exists('results.csv'): os.remove('results.csv')
if os.path.exists('results.png'): os.remove('results.png')

RUNS_PER_AGENT = 10
AGENTS = {
    'BFS': BFSAgent,
    'A*': AStarAgent,
    'Hill-Climb': HillAgent,
    'ForwardTracking': ForwardAgent,
}

def run_once(agent_cls):
    game = SnakeGame(width=30, height=20)
    agent = agent_cls(game)
    steps = 0; start = time.time()
    while game.alive and steps < 2000:
        mv = agent.next_move(); game.step(mv); steps += 1
    elapsed = time.time() - start
    return game.score, steps, elapsed / max(steps,1)

def benchmark():
    results = []
    print(f"Chạy benchmark {RUNS_PER_AGENT} lần mỗi thuật toán...\n")
    for name, cls in AGENTS.items():
        scores, steps_list, times = [], [], []
        for i in range(RUNS_PER_AGENT):
            s, st, t = run_once(cls)
            scores.append(s); steps_list.append(st); times.append(t)
        avg_score = mean(scores); avg_steps = mean(steps_list); avg_time = mean(times)
        results.append((name, avg_score, avg_steps, avg_time))
        print(f"{name:18s} | Điểm TB: {avg_score:6.2f} | Steps TB: {avg_steps:7.2f} | Time/step: {avg_time*1000:6.3f} ms")

    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f); writer.writerow(['Agent','AvgScore','AvgSteps','AvgTimePerStep(s)']); writer.writerows(results)

    agents = [r[0] for r in results]; scores = [r[1] for r in results]; steps = [r[2] for r in results]; times = [r[3]*1000 for r in results]
    fig, axs = plt.subplots(1,3,figsize=(14,4))
    axs[0].bar(agents, scores); axs[0].set_title('Điểm trung bình')
    axs[1].bar(agents, steps); axs[1].set_title('Steps trung bình')
    axs[2].bar(agents, times); axs[2].set_title('Thời gian trung bình (ms/step)')
    for ax in axs: ax.set_xlabel('Thuật toán'); ax.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout(); plt.savefig('results.png'); plt.show()

if __name__ == '__main__':
    benchmark()
