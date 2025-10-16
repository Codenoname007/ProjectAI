import time
from utils import DIRS

class ForwardAgent:
    def __init__(self, game):
        self.game = game

    def next_move(self):
        start = self.game.snake[0]  # Đầu rắn
        goal = self.game.food  # Mục tiêu là thức ăn

        if goal is None: 
            return (1, 0)  # Nếu không có thức ăn, giữ nguyên hướng (di chuyển sang phải)

        # Tìm hướng di chuyển gần nhất đến thức ăn
        best_move = None
        min_distance = float('inf')  # Khoảng cách ngắn nhất đến thức ăn
        for d in DIRS:
            nb = (start[0] + d[0], start[1] + d[1])  # Vị trí mới sau khi di chuyển
            if 0 <= nb[0] < self.game.cols and 0 <= nb[1] < self.game.rows:  # Kiểm tra nếu trong phạm vi
                if nb not in self.game.snake:  # Kiểm tra nếu không phải thân rắn
                    # Tính khoảng cách Manhattan đến thức ăn
                    distance = abs(nb[0] - goal[0]) + abs(nb[1] - goal[1])
                    if distance < min_distance:
                        min_distance = distance
                        best_move = d  # Lưu hướng di chuyển tốt nhất

        if best_move is not None:
            return best_move
        return (1, 0)  # Mặc định di chuyển sang phải nếu không có hướng hợp lệ
