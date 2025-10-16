# astar_agent.py - A* với heuristic Manhattan cho game
import heapq
from utils import DIRS, manhattan

class AStarAgent:
    def __init__(self, game):
        self.game = game

    def next_move(self):
        start = self.game.snake[0]
        goal = self.game.food
        if goal is None:
            return (1,0)
        cols, rows = self.game.cols, self.game.rows
        blocked = set(self.game.snake)
        tail = self.game.snake[-1]
        if tail in blocked: blocked.remove(tail)
        open_heap = []
        heapq.heappush(open_heap, (manhattan(start,goal), 0, start))
        came = {start: None}; gscore = {start:0}
        while open_heap:
            f, g, cur = heapq.heappop(open_heap)
            if cur == goal: break
            for d in DIRS:
                nb = (cur[0]+d[0], cur[1]+d[1])
                if nb[0]<0 or nb[1]<0 or nb[0]>=cols or nb[1]>=rows: continue
                if nb in blocked: continue
                ng = g + 1
                if nb not in gscore or ng < gscore[nb]:
                    gscore[nb] = ng; came[nb] = cur
                    heapq.heappush(open_heap, (ng + manhattan(nb,goal), ng, nb))
        if goal not in came:
            for d in DIRS:
                nb = (start[0]+d[0], start[1]+d[1])
                if 0<=nb[0]<cols and 0<=nb[1]<rows and nb not in set(list(self.game.snake)[:-1]):
                    return d
            return (1,0)
        cur = goal; path = []
        while cur != start:
            path.append(cur); cur = came[cur]
        path.reverse(); first = path[0]
        return (first[0]-start[0], first[1]-start[1])
