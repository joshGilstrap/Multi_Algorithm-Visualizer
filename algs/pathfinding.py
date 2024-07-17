import pygame
import pygame_gui
import random
from algs.visualization import Visualization

class PathfindingVisualization(Visualization):
    def __init__(self, screen):
        super().__init__(screen)
        self.grid_size = 80
        self.cell_size = 8
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        self.start = (0,0)
        self.start_set = False
        self.end = (self.grid_size - 1, self.grid_size - 1)
        self.end_set = False
        
        self.queue = []
        self.visited = set()
        self.parent = {}
        self.path_found = False
        self.path = []
        self.obstacles = set()
        self.g_score = {}
        self.f_score = {}
        self.current = None
        
        self.ui_manager = pygame_gui.UIManager((1280,720))
        self.start_btn = pygame_gui.elements.UIButton(pygame.Rect((650,0), (75, 40)), 'Start', manager=self.ui_manager,)
        self.bfs_btn = pygame_gui.elements.UIButton(pygame.Rect((750, 0), (75, 40)), 'BFS', manager=self.ui_manager)
        self.dfs_btn = pygame_gui.elements.UIButton(pygame.Rect((750, 50), (75, 40)), 'DFS', manager=self.ui_manager)
        self.a_star_btn = pygame_gui.elements.UIButton(pygame.Rect((750, 100), (75, 40)), 'A Star', manager=self.ui_manager)
        self.maze_btn = pygame_gui.elements.UIButton(pygame.Rect((650,50), (75, 40)), 'Make Maze', manager=self.ui_manager,)
        self.fwd_step_btn = pygame_gui.elements.UIButton(pygame.Rect((650, 100), (75, 40)), 'Step Fwd', manager=self.ui_manager)
        self.bck_step_btn = pygame_gui.elements.UIButton(pygame.Rect((650, 150), (75, 40)), 'Step Back', manager=self.ui_manager)
        self.reset_btn = pygame_gui.elements.UIButton(pygame.Rect((650, 200), (75, 40)), 'Reset', manager=self.ui_manager)
        self.clear_btn = pygame_gui.elements.UIButton(pygame.Rect((650, 250), (75, 40)), 'Clear', manager=self.ui_manager)
        
        self.go = False
        self.maze_btn_pressed = False
        self.fwd_btn_pressed = False
        self.bck_btn_pressed = False
        self.reset_btn_pressed = False
        self.bfs_btn_pressed = True
        self.dfs_btn_pressed = False
        self.a_star_btn_pressed = False
        
        self.states = []
        self.current_state_index = -1
        
        self.alg_text = ''
    
    def handle_mouse_click(self, pos, button):
        x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
        if button == 1 and x < self.grid_size and y < self.grid_size and (x, y) not in self.obstacles:
            self.start = (x, y)
            self.start_set = True
            self.queue = []
            self.queue.append(self.start)
            self.g_score[self.start] = 0
            self.f_score[self.start] = self.heuristic(self.start, self.end)
        elif button == 3 and x < self.grid_size and y < self.grid_size and (x, y) not in self.obstacles:
            self.end = (x, y)
            self.end_set = True
        elif button == 2 and x < self.grid_size and y < self.grid_size:
            if (x, y) in self.obstacles:
                self.obstacles.remove((x, y))
            else:
                self.obstacles.add((x, y))
    
    def save_state(self):
        self.states.append((self.grid.copy(), self.start, self.end, self.obstacles.copy(), self.queue, self.visited.copy(), self.parent.copy(), self.path_found, self.path.copy()))
        self.current_state_index = len(self.states) - 1
    
    def load_state(self, index):
        if 0 <= index < len(self.states):
            (self.grid, self.start, self.end, self.obstacles, self.queue, self.visited, self.parent, self.path_found, self.path) = self.states[index]
            self.render()
    
    def next_step(self):
        if self.current_state_index < len(self.states) - 1:
            self.current_state_index += 1
            self.load_state(self.current_state_index)
    
    def prev_step(self):
        if self.current_state_index > 0:
            self.current_state_index -= 1
            self.load_state(self.current_state_index)
        
    def bfs_step(self):
        if self.queue and not self.path_found:
            self.current = self.queue.pop(0)
            pygame.draw.rect(self.screen, (255,0,0), (self.current[0] * self.cell_size, self.current[1] * self.cell_size, self.cell_size, self.cell_size))
            if self.current == self.end:
                self.path_found = True
                self.path = []
                while self.current != self.start:
                    self.path.append(self.current)
                    self.current = self.parent[self.current]
                self.path.append(self.start)
                self.path.reverse()
                self.save_state()
                return
            for neighbor in self.get_neighbors(self.current):
                if neighbor not in self.visited and neighbor not in self.obstacles:
                    self.visited.add(neighbor)
                    self.queue.append(neighbor)
                    self.parent[neighbor] = self.current
                    self.grid[neighbor[1]][neighbor[0]] = 1
                    self.save_state()
    
    def dfs_step(self):
        if self.queue and not self.path_found:
            self.current = self.queue.pop()
            pygame.draw.rect(self.screen, (255,0,0), (self.current[0] * self.cell_size, self.current[1] * self.cell_size, self.cell_size, self.cell_size))
            if self.current == self.end:
                self.path_found = True
                self.path = []
                while self.current != self.start:
                    self.path.append(self.current)
                    self.current = self.parent[self.current]
                self.path.append(self.start)
                self.path.reverse()
                self.save_state()
                return
            for neighbor in self.get_neighbors(self.current):
                if neighbor not in self.visited and neighbor not in self.obstacles:
                    self.visited.add(neighbor)
                    self.queue.append(neighbor)
                    self.parent[neighbor] = self.current
                    self.grid[neighbor[1]][neighbor[0]] = 1
                    self.save_state()
    
    def a_star_step(self):
        if self.queue and not self.path_found:
            self.current = self.queue.pop(0)
            pygame.draw.rect(self.screen, (255,0,0), (self.current[0] * self.grid_size, self.current[1] * self.grid_size, self.cell_size, self.cell_size))
            if self.current == self.end:
                self.path_found = True
                self.path = []
                while self.current != self.start:
                    self.path.append(self.current)
                    self.current = self.parent[self.current]
                self.path.append(self.start)
                self.path.reverse()
                self.save_state()
                return
            for neighbor in self.get_neighbors(self.current):
                if neighbor not in self.visited and neighbor not in self.obstacles:
                    tentative_g_score = self.g_score[self.current] + 1
                    if tentative_g_score < self.g_score.get(neighbor, float('inf')):
                        self.visited.add(neighbor)
                        self.parent[neighbor] = self.current
                        self.g_score[neighbor] = tentative_g_score
                        self.f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.end)
                        self.queue.append(neighbor)
                        self.queue.sort(key=lambda x: self.f_score[x])
                        self.grid[neighbor[1]][neighbor[0]] - 1
                        self.save_state()
    
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def get_neighbors(self, node):
        x, y = node
        neighbors = []
        if x > 0: neighbors.append((x - 1, y))
        if x < self.grid_size - 1: neighbors.append((x + 1, y))
        if y > 0: neighbors.append((x, y - 1))
        if y < self.grid_size - 1: neighbors.append((x, y + 1))
        return neighbors
    
    def reset_board(self):
        self.start = (0,0)
        self.start_set = False
        self.end = (self.grid_size - 1, self.grid_size - 1)
        self.end_set = False
        self.queue = []
        self.visited = set()
        self.parent = {}
        self.path_found = False
        self.path = []
        self.go = False
        self.states = []
        self.current_state_index = -1
        self.alg_text = ''
        self.g_score = {}
        self.f_score = {}
    
    def input_handler(self):
        if self.start_btn.check_pressed():
            self.go = True
        if self.maze_btn.check_pressed():
            self.go = False
            self.__init__(self.screen)
            self.generate_maze()
        if self.fwd_step_btn.check_pressed():
            self.fwd_step_btn.pressed = False
            self.fwd_btn_pressed = True
        if self.bck_step_btn.check_pressed():
            self.bck_step_btn.pressed = False
            self.bck_btn_pressed = True
        if self.reset_btn.check_pressed():
            self.reset_btn.pressed = False
            self.reset_btn_pressed = True
            self.reset_board()
        if self.clear_btn.check_pressed():
            self.clear_btn.pressed = False
            self.__init__(self.screen)
        if self.bfs_btn.check_pressed():
            self.bfs_btn_pressed = True
            self.dfs_btn_pressed = False
            self.a_star_btn_pressed = False
            self.alg_text = 'Breadth First Pathfinding'
        if self.dfs_btn.check_pressed():
            self.dfs_btn_pressed = True
            self.bfs_btn_pressed = False
            self.a_star_btn_pressed = False
            self.alg_text = 'Depth First Pathfinding'
        if self.a_star_btn.check_pressed():
            self.a_star_btn_pressed = True
            self.bfs_btn_pressed = False
            self.dfs_btn_pressed = False
            self.alg_text = 'A* First Pathfinding'
    
    def render_active(self):
        for item in self.visited:
            if item == self.current:
                color = (255,0,0)
                pygame.draw.rect(self.screen, color, (item[0], item[1], self.cell_size, self.cell_size))
    
    def render(self):
        self.screen.fill((255,255,255))
        
        # self.render_grid()
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                color = (200,200,200) if (x + y) % 2 == 0 else (220,220,220)
                pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        
        for x, y in self.obstacles:
            pygame.draw.rect(self.screen, (0,0,0), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        
        self.input_handler()
        
        if self.go:
            if self.bfs_btn_pressed:
                self.bfs_step()
                self.render_active()
            elif self.dfs_btn_pressed:
                self.dfs_step()
            elif self.a_star_btn_pressed:
                self.a_star_step()
        if self.fwd_btn_pressed:
            self.go = False
            self.bfs_step()
            self.save_state()
            self.fwd_btn_pressed = False
        if self.bck_btn_pressed:
            self.bck_btn_pressed = False
            self.go = False
            self.prev_step()
            
        for x, y in self.visited:
            pygame.draw.rect(self.screen, (0,128,255), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        
        if self.path_found:
            for x, y in self.path:
                pygame.draw.rect(self.screen, (255,255,0), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        if self.start_set:
            pygame.draw.rect(self.screen, (0,255,0), (self.start[0] * self.cell_size, self.start[1] * self.cell_size, self.cell_size, self.cell_size))
        if self.end_set:
            pygame.draw.rect(self.screen, (255,0,0), (self.end[0] * self.cell_size, self.end[1] * self.cell_size, self.cell_size, self.cell_size))
        
        text_surface = pygame.font.SysFont('Arial', 24).render(self.alg_text, True, (0,0,0))
        self.screen.blit(text_surface, (150,650))
        
    def recursive_division(self, x, y, width, height, passage_frequency=0.4):
        if width <= 2 or height <= 2:
            return
        divide_horizontally = width < height

        if not divide_horizontally:
            wx = x + random.randint(1, width - 2)
            for wy in range(y, y + height):
                self.obstacles.add((wx, wy))
            for _ in range(int(height * passage_frequency)):
                passage = y + random.randint(0, height - 1)
                if (wx, passage) in self.obstacles:
                    self.obstacles.remove((wx, passage))
            self.recursive_division(x, y, wx - x, height)
            self.recursive_division(wx + 1, y, x + width - wx - 1, height)
        else:
            wy = y + random.randint(1, height - 2)
            for wx in range(x, x + width):
                self.obstacles.add((wx, wy))
            for _ in range(int(width * passage_frequency)):
                passage = x + random.randint(0, width - 1)
                if (passage, wy) in self.obstacles:
                    self.obstacles.remove((passage, wy))
            self.recursive_division(x, y, width, wy - y)
            self.recursive_division(x, wy + 1, width, y + height - wy - 1)

    def generate_maze(self):
        self.obstacles = set()
        self.recursive_division(0, 0, self.grid_size, self.grid_size)
        self.start = (0,0)
        self.end = (self.grid_size - 1, self.grid_size - 1)
        self.save_state()
        self.render()