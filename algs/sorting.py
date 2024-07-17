import pygame
import pygame_gui
import time
import random
from algs.visualization import Visualization

class SortingVisualization(Visualization):
    def __init__(self, screen):
        super().__init__(screen)
        self.array = [5, 3, 8, 6, 2, 7, 4, 1]
        self.i = 0
        self.j = 0

    def render(self):
        time.sleep(0.1)
        self.screen.fill((255, 255, 255))
        width = 50
        spacing = 10
        offset = 150
        
        for idx, value in enumerate(self.array):
            color = (0, 255, 255) if idx == self.j or idx == self.j + 1 else (0, 0, 0)
            pygame.draw.rect(self.screen, color, (offset + idx * (width + spacing), 400 - value * 30, width, value * 30))
        
        if self.i < len(self.array):
            if self.j < len(self.array) - self.i - 1:
                if self.array[self.j] > self.array[self.j + 1]:
                    self.array[self.j], self.array[self.j + 1] = self.array[self.j + 1], self.array[self.j]
                self.j += 1
            else:
                self.j = 0
                self.i += 1
        
        text_surface = pygame.font.SysFont('Arial', 24).render("Bubble Sort Visualization", True, (0,0,0))
        self.screen.blit(text_surface, (150, 50))