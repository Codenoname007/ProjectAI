# utils.py - Các hàm phụ trợ cho các thuật toán 
from collections import deque
from heapq import heappush, heappop

# Hướng 4 chiều
DIRS = [(0,1),(1,0),(0,-1),(-1,0)]

def manhattan(a,b):
    """Khoảng cách Manhattan giữa hai ô a và b."""
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def bfs_path(start, goal, blocked, cols, rows):
    """BFS trả về đường đi list từ start->goal hoặc None."""
    q = deque([start])
    came = {start: None}
    while q:
        cur = q.popleft()
        if cur == goal: break
        for dx,dy in DIRS:
            nb = (cur[0]+dx, cur[1]+dy)
            if nb in came: continue
            if nb[0]<0 or nb[1]<0 or nb[0]>=cols or nb[1]>=rows: continue
            if nb in blocked: continue
            came[nb] = cur; q.append(nb)
    if goal not in came: return None
    path = []
    cur = goal
    while cur != start:
        path.append(cur); cur = came[cur]
    path.reverse(); return path

def a_star_path(start, goal, blocked, cols, rows):
    """A* với heuristic Manhattan."""
    openh = []
    heappush(openh, (manhattan(start,goal), 0, start))
    came = {start: None}; gscore = {start:0}
    while openh:
        f,g,cur = heappop(openh)
        if cur == goal: break
        for dx,dy in DIRS:
            nb = (cur[0]+dx, cur[1]+dy)
            if nb[0]<0 or nb[1]<0 or nb[0]>=cols or nb[1]>=rows: continue
            if nb in blocked: continue
            ng = g+1
            if nb not in gscore or ng < gscore[nb]:
                gscore[nb]=ng; came[nb]=cur
                heappush(openh, (ng + manhattan(nb,goal), ng, nb))
    if goal not in came: return None
    path = []; cur = goal
    while cur != start:
        path.append(cur); cur = came[cur]
    path.reverse(); return path
