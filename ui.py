import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.font.init()
FONT = pygame.font.SysFont('Arial', 24)

def draw_menu(screen):
    screen.fill(WHITE)
    menu_items = [
        '1. Sorting Algorithms',
        '2. Pathfinding Algorithms',
        '3. Graph Algorithms',
        '4. Backtracking Algorithms',
        '5. Dynamic Programming',
        '6. Data Structures',
    ]
    for index, item in enumerate(menu_items):
        text_surface = FONT.render(item, True, BLACK)
        screen.blit(text_surface, (50, 50 + index * 40))