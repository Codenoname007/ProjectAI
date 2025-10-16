# bfs_agent.py - BFS (Tìm kiếm theo chiều rộng) 
from collections import deque
from utils import DIRS

class BFSAgent:
    def __init__(self, game):
        self.game = game

    def next_move(self):
        start = self.game.snake[0]
        goal = self.game.food
        if goal is None:
            return (1,0)
        blocked = set(self.game.snake)
        tail = self.game.snake[-1]
        if tail in blocked: blocked.remove(tail)
        q = deque([start])
        came = {start: None}
        while q:
            cur = q.popleft()
            if cur == goal: break
            for d in DIRS:
                nb = (cur[0]+d[0], cur[1]+d[1])
                if nb in came: continue
                if nb[0]<0 or nb[1]<0 or nb[0]>=self.game.cols or nb[1]>=self.game.rows: continue
                if nb in blocked: continue
                came[nb] = cur; q.append(nb)
        if goal not in came:
            for d in DIRS:
                nb = (start[0]+d[0], start[1]+d[1])
                if 0<=nb[0]<self.game.cols and 0<=nb[1]<self.game.rows and nb not in set(list(self.game.snake)[:-1]):
                    return d
            return (1,0)
        cur = goal; path = []
        while cur != start:
            path.append(cur); cur = came[cur]
        path.reverse(); first = path[0]
        return (first[0]-start[0], first[1]-start[1])
