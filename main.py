import pygame
import sys
from ui import draw_menu
from algs.sorting import SortingVisualization
from algs.pathfinding import PathfindingVisualization
from algs.graph import GraphVisualization
from algs.backtracking import NQueensVisualization

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BG_COLOR = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Algorithm Visualizer')

visualizations = {
    "NONE" : 0,
    "SRT" : SortingVisualization(screen),
    "BFS" : PathfindingVisualization(screen),
    "GRPH" : GraphVisualization(screen),
    "BCK" : NQueensVisualization(screen)
}

current = visualizations["NONE"]

clock = pygame.time.Clock()

running = True
while running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current = visualizations["SRT"]
            elif event.key == pygame.K_2:
                current = visualizations["BFS"]
            elif event.key == pygame.K_3: 
                current = visualizations["GRPH"]
            elif event.key == pygame.K_4:
                current = visualizations["BCK"]
            elif event.key == pygame.K_ESCAPE:
                current = visualizations["NONE"]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            current.handle_mouse_click(event.pos, event.button)
        visualizations["BFS"].ui_manager.process_events(event)
        visualizations["GRPH"].ui_manager.process_events(event)
        visualizations["BCK"].ui_manager.process_events(event)
        
    if current == visualizations["NONE"]:        
        draw_menu(screen)
    else:
        current.render()
        
    if current == visualizations["BFS"]:
        visualizations["BFS"].ui_manager.update(time_delta)
        visualizations["BFS"].ui_manager.draw_ui(screen)
    elif current == visualizations['GRPH']:
        visualizations["GRPH"].ui_manager.update(time_delta)
        visualizations["GRPH"].ui_manager.draw_ui(screen)
    elif current == visualizations["BCK"]:
        visualizations["BCK"].ui_manager.update(time_delta)
        visualizations["BCK"].ui_manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
sys,quit()