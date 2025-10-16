# hill_agent.py - Hill-Climbing (Greedy) 
import random
from utils import DIRS, manhattan

class HillAgent:
    def __init__(self, game):
        self.game = game

    def next_move(self):
        head = self.game.snake[0]
        food = self.game.food
        blocked = set(list(self.game.snake)[:-1])
        candidates = []
        for d in DIRS:
            nb = (head[0]+d[0], head[1]+d[1])
            if nb[0]<0 or nb[1]<0 or nb[0]>=self.game.cols or nb[1]>=self.game.rows: continue
            if nb in blocked: continue
            score = -manhattan(nb, food)
            candidates.append((score, d))
        if not candidates: return (1,0)
        candidates.sort(reverse=True)
        best_score = candidates[0][0]
        top = [d for s,d in candidates if s==best_score]
        return random.choice(top)
