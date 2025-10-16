# main.py - Menu chọn thuật toán bằng Pygame (TOÀN BỘ CHÚ THÍCH TIẾNG VIỆT)
import pygame, sys, os, time
from game import SnakeGame
from algorithms.bfs_agent import BFSAgent
from algorithms.astar_agent import AStarAgent
from algorithms.hill_agent import HillAgent
from algorithms.forward_agent import ForwardAgent

pygame.init()
FONT = pygame.font.SysFont('arial', 28)
SCREEN_W = 720
SCREEN_H = 520
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Snake AI - Chọn Thuật Toán (Pygame Menu)')

WHITE = (255,255,255); BLACK = (20,20,20); HIGHLIGHT = (80,200,120)

algorithms = [
    ("BFS - Tim kiem theo chieu rong", BFSAgent),
    ("A* - A Star (Manhattan)", AStarAgent),
    ("Hill-Climbing - Greedy", HillAgent),
    ("ForwardTracking", ForwardAgent),
]

def draw_menu(selected):
    screen.fill(BLACK)
    title = FONT.render("Chọn thuật toán AI cho Snake", True, WHITE); screen.blit(title, (30, 30))
    hint = pygame.font.SysFont('arial',18).render("Dùng ↑ ↓ để chọn, Enter để bắt đầu, Esc để thoát", True, WHITE); screen.blit(hint, (30, 70))
    for i, (name, _) in enumerate(algorithms):
        color = HIGHLIGHT if i == selected else WHITE
        txt = FONT.render(name, True, color); screen.blit(txt, (60, 130 + i*50))
    pygame.display.flip()

def choose_algorithm():
    selected = 0
    while True:
        draw_menu(selected)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: selected = (selected - 1) % len(algorithms)
                elif event.key == pygame.K_DOWN: selected = (selected + 1) % len(algorithms)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE): return algorithms[selected][1]
                elif event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

def main():
    agent_class = choose_algorithm()
    game = SnakeGame(width=30, height=20)
    agent = agent_class(game)
    clock = pygame.time.Clock(); FPS = 10
    start = time.time(); saved = False; running = True
    while running:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT: running = False
        action = agent.next_move(); game.step(action); game.draw(screen)
        if not saved and time.time() - start > 2:
            screenshot_path = os.path.join(os.path.dirname(__file__), 'demo_screenshot.png'); pygame.image.save(screen, screenshot_path); saved = True
        clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    main()
