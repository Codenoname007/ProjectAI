import pygame, random, os
from collections import deque

CELL = 24
COLS = 30
ROWS = 20

class SnakeGame:
    def __init__(self, width=COLS, height=ROWS):
        # Khởi tạo game và tải assets
        self.width = width
        self.height = height
        self.cell = CELL
        self.cols = width
        self.rows = height
        self.screen_w = self.cols * self.cell
        self.screen_h = self.rows * self.cell + 40
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption('Snake AI - Ran san moi')
        self.font = pygame.font.SysFont('arial', 20)
        self.clock = pygame.time.Clock()

        assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
        try:
            self.bg = pygame.image.load(os.path.join(assets_dir, 'background.png')).convert()
        except:
            self.bg = None
        try:
            self.head_img = pygame.image.load(os.path.join(assets_dir, 'snake_head.png')).convert_alpha()
        except:
            self.head_img = None
        try:
            self.body_img = pygame.image.load(os.path.join(assets_dir, 'snake_body.png')).convert_alpha()
        except:
            self.body_img = None
        try:
            self.food_img = pygame.image.load(os.path.join(assets_dir, 'food.png')).convert_alpha()
        except:
            self.food_img = None

        self.reset()

    def reset(self):
        # Đặt rắn giữa, chiều dài 3
        mid = (self.cols // 2, self.rows // 2)
        self.snake = deque([mid, (mid[0] - 1, mid[1]), (mid[0] - 2, mid[1])])
        self.grow = 0
        self.place_food()
        self.score = 0
        self.steps = 0
        self.alive = True
        self.agent = None

    def place_food(self):
        free = [(x, y) for x in range(self.cols) for y in range(self.rows) if (x, y) not in self.snake]
        self.food = random.choice(free) if free else None

    def set_agent(self, agent_cls):
        self.agent = agent_cls(self)  # Sử dụng ForwardAgent hoặc các agent khác

    def step(self, move=(1, 0)):
        if not self.alive: return
        head = self.snake[0]
        new_head = (head[0] + move[0], head[1] + move[1])

        # Va chạm tường
        if not (0 <= new_head[0] < self.cols and 0 <= new_head[1] < self.rows):
            self.alive = False
            return

        # Tự cắn (không tính tail)
        if new_head in list(self.snake)[:-1]:
            self.alive = False
            return

        self.snake.appendleft(new_head)

        if self.food and new_head == self.food:
            self.score += 1
            self.grow += 1
            self.place_food()

        if self.grow > 0:
            self.grow -= 1
        else:
            self.snake.pop()

        self.steps += 1

    def draw(self, screen=None):
        if screen is None: screen = self.screen
        if self.bg:
            screen.blit(pygame.transform.scale(self.bg, (self.cols * self.cell, self.rows * self.cell)), (0, 0))
        else:
            screen.fill((40, 40, 40))

        # Vẽ thức ăn
        if self.food_img and self.food is not None:
            fx, fy = self.food
            screen.blit(pygame.transform.scale(self.food_img, (self.cell, self.cell)), (fx * self.cell, fy * self.cell))
        else:
            if self.food is not None:
                fx, fy = self.food
                pygame.draw.rect(screen, (200, 30, 30), (fx * self.cell, fy * self.cell, self.cell, self.cell))

        # Vẽ rắn
        for i, (sx, sy) in enumerate(self.snake):
            x, y = sx * self.cell, sy * self.cell
            if i == 0 and self.head_img:
                screen.blit(pygame.transform.scale(self.head_img, (self.cell, self.cell)), (x, y))
            elif i == 0:
                pygame.draw.rect(screen, (34, 177, 76), (x, y, self.cell, self.cell))
            else:
                if self.body_img:
                    screen.blit(pygame.transform.scale(self.body_img, (self.cell, self.cell)), (x, y))
                else:
                    pygame.draw.rect(screen, (255, 242, 0), (x, y, self.cell, self.cell))

        # Trước khi vẽ thông tin mới, xóa thông tin cũ (vẽ lại một hình chữ nhật nền)
        screen.fill((40, 40, 40), (0, self.rows * self.cell, self.screen_w, 40))  # Xóa vùng thông tin

        # Vẽ thông tin mới
        info_point = 'Point: {}'.format(self.score)
        info_step = 'Step: {}'.format(self.steps)
        info_length = 'Length: {}'.format(len(self.snake))

        # Vẽ từng thông tin tại các vị trí khác nhau để tránh đè lên nhau
        txt_point = self.font.render(info_point, True, (230, 230, 230))
        screen.blit(txt_point, (8, self.rows * self.cell + 8))  # Vị trí của Point

        txt_step = self.font.render(info_step, True, (230, 230, 230))
        screen.blit(txt_step, (150, self.rows * self.cell + 8))  # Vị trí của Step (Dịch ra phải)

        txt_length = self.font.render(info_length, True, (230, 230, 230))
        screen.blit(txt_length, (300, self.rows * self.cell + 8))  # Vị trí của Length (Dịch xa hơn nữa)

        pygame.display.flip()  # Cập nhật màn hình
