import pygame
import pygame_gui
import time
from algs.visualization import Visualization

class GraphVisualization(Visualization):
    def __init__(self, screen):
        super().__init__(screen)
        self.nodes = {}
        self.edges = []
        self.adjacency_list = {}
        self.node_radius = 20
        self.selected_node = None
        self.algorithm = None
        self.visited = set()
        self.stack = []
        self.queue = []
        self.next_node_value = 1
        self.ui_manager = pygame_gui.UIManager((1280,720))
        self.bfs_btn = pygame_gui.elements.UIButton(pygame.Rect((30,180), (75, 40)), 'BFS', manager=self.ui_manager,)
        self.dfs_btn = pygame_gui.elements.UIButton(pygame.Rect((30,220), (75, 40)), 'DFS', manager=self.ui_manager,)
        self.simple_btn = pygame_gui.elements.UIButton(pygame.Rect((30, 260), (75, 40)), 'Simple', manager=self.ui_manager)
        self.cycle_btn = pygame_gui.elements.UIButton(pygame.Rect((30, 300), (75, 40)), 'Cycle', manager=self.ui_manager)
        self.complete_btn = pygame_gui.elements.UIButton(pygame.Rect((30, 340), (75, 40)), 'Complete', manager=self.ui_manager)
        self.large_btn = pygame_gui.elements.UIButton(pygame.Rect((30, 380), (75, 40)), 'Large', manager=self.ui_manager)
        self.clear_btn = pygame_gui.elements.UIButton(pygame.Rect((30,420), (75, 40)), 'Clear', manager=self.ui_manager,)
        self.start_btn = pygame_gui.elements.UIButton(pygame.Rect((30,460), (75, 40)), 'Start', manager=self.ui_manager,)
        self.bfs_btn_pressed = False
        self.dfs_btn_pressed = False
        self.simple_btn_pressed = False
        self.cycle_btn_pressed = False
        self.complete_btn_pressed = False
        self.large_btn_pressed = False
        self.start_btn_pressed = False
        self.current = None
    
    def add_node(self, pos):
        self.nodes[pos] = self.next_node_value
        self.adjacency_list[pos] = []
        self.next_node_value += 1
    
    def remove_node(self, node):
        if node == None:
            return
        for index in self.adjacency_list.copy():
            if ((node, index)) in self.edges:
                self.remove_edge(node, index)
            elif ((index, node)) in self.edges:
                self.remove_edge(index, node, reverse=True)
        self.adjacency_list.pop(node)
        self.nodes.pop(node)
        if self.queue and node in self.queue:
            queue_index = self.queue.index(node)
            self.queue.pop(queue_index)
        elif self.stack and node in self.stack:
            stack_index = self.stack.index(node)
            self.stack.pop(stack_index)
    
    def add_edge(self, node1, node2):
        self.edges.append((node1, node2))
        self.adjacency_list[node1].append(node2)
        self.adjacency_list[node2].append(node1)
    
    def remove_edge(self, node1, node2, reverse=False):
        edge_index = self.edges.index((node1, node2))
        self.edges.pop(edge_index)
        node2_index = self.adjacency_list[node2]
        node1_index = node2_index.index(node1)
        if reverse:
            node2_index = self.adjacency_list[node1]
            node1_index = node2_index.index(node2)
            self.adjacency_list[node1].pop(node1_index)
            return
        self.adjacency_list[node2].pop(node1_index)
    
    def get_node_at_pos(self, pos):
        for node in self.nodes:
            if (node[0] - pos[0])**2 + (node[1] - pos[1])**2 <= self.node_radius**2:
                return node
        return None
    
    def handle_mouse_click(self, pos, button):
        node = self.get_node_at_pos(pos)
        if button == 1 and pos[0] > 250:
            if node is None:
                self.add_node(pos)
            else:
                self.selected_node = node
        elif button == 2:
            self.remove_node(node)
        elif button == 3 and self.selected_node:
            if node and node != self.selected_node:
                self.add_edge(self.selected_node, node)
            self.selected_node = None
    
    def bfs_step(self):
        time.sleep(1)
        if not self.queue:
            return
        self.current = self.queue.pop(0)
        for neighbor in self.adjacency_list[self.current]:
            if neighbor not in self.visited:
                self.visited.add(neighbor)
                self.queue.append(neighbor)
    
    def dfs_step(self):
        time.sleep(1)
        if not self.stack:
            return
        self.current = self.stack.pop()
        for neighbor in self.adjacency_list[self.current]:
            if neighbor not in self.visited:
                self.visited.add(neighbor)
                self.stack.append(neighbor)
    
    def start_bfs(self, start_node):
        self.algorithm = 'BFS'
        self.visited = {start_node}
        self.queue = [start_node]
        
    def start_dfs(self, start_node):
        self.algorithm = 'DFS'
        self.visited = {start_node}
        self.stack = [start_node]
        
    def draw_text(self, text, pos, font_size=18, color=(0,0,0)):
        font = pygame.font.SysFont('Arial', font_size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, pos)
    
    def clear_graph(self):
        self.__init__(self.screen)
    
    def load_sample(self, sample_kind):
        if sample_kind == "simple":
            self.add_node((400, 400))
            self.add_node((500, 400))
            self.add_node((450, 500))
            self.add_edge((400, 400), (500, 400))
            self.add_edge((500, 400), (450, 500))
            self.add_edge((450, 500), (400, 400))
        elif sample_kind == "cycle":
            positions = [(400, 400), (500, 400), (500, 500), (400, 500)]
            for pos in positions:
                self.add_node(pos)
            for i in range(len(positions)):
                self.add_edge(positions[i], positions[(i + 1) % len(positions)])
        elif sample_kind == "complete":
            positions = [(400, 400), (500, 400), (500, 500), (400, 500)]
            for pos in positions:
                self.add_node(pos)
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    self.add_edge(positions[i], positions[j])
        elif sample_kind == 'large':
            positions = [
                (350, 250), (450, 250), (550, 250), (650, 250), (750, 250),
                (350, 350), (450, 350), (550, 350), (650, 350), (750, 350),
                (350, 450), (450, 450), (550, 450), (650, 450), (750, 450),
                (350, 550), (450, 550), (550, 550), (650, 550), (750, 550)
            ]
            for pos in positions:
                self.add_node(pos)
            edges = [
                (positions[0], positions[1]), (positions[1], positions[2]), (positions[2], positions[3]), (positions[3], positions[4]),
                (positions[5], positions[6]), (positions[6], positions[7]), (positions[7], positions[8]), (positions[8], positions[9]),
                (positions[10], positions[11]), (positions[11], positions[12]), (positions[12], positions[13]), (positions[13], positions[14]),
                (positions[15], positions[16]), (positions[16], positions[17]), (positions[17], positions[18]), (positions[18], positions[19]),
                (positions[0], positions[5]), (positions[5], positions[10]), (positions[10], positions[15]), (positions[1], positions[6]),
                (positions[6], positions[11]), (positions[11], positions[16]), (positions[2], positions[7]), (positions[7], positions[12]),
                (positions[12], positions[17]), (positions[3], positions[8]), (positions[8], positions[13]), (positions[13], positions[18]),
                (positions[4], positions[9]), (positions[9], positions[14]), (positions[14], positions[19])
            ]
            for edge in edges:
                self.add_edge(*edge)
        
    def render(self):
        self.screen.fill((255,255,255))
        
        for edge in self.edges:
            pygame.draw.line(self.screen, (0,0,0), edge[0], edge[1], 2)
            
        for node, value in self.nodes.items():
            color = (0,0,255) if node == self.selected_node else (0, 128, 255)
            color = (0,255,0) if node in self.visited else color
            color = (255,0,0) if node == self.current else color
            pygame.draw.circle(self.screen, color, node, self.node_radius)
            text_surface = pygame.font.SysFont('Arial', 18).render(str(value), True, (255,255,255))
            self.screen.blit(text_surface, (node[0] - 10, node[1] - 10))
        
        if self.bfs_btn.check_pressed():
            self.bfs_btn_pressed = True
            self.dfs_btn_pressed = False
        if self.dfs_btn.check_pressed():
            self.dfs_btn_pressed = True
            self.bfs_btn_pressed = False
        
        if self.clear_btn.check_pressed():
            self.clear_graph()
        
        if self.start_btn.check_pressed():
            self.start_btn_pressed = True
        
        if self.simple_btn.check_pressed():
            self.simple_btn_pressed = True
            self.cycle_btn_pressed = False
            self.complete_btn_pressed = False
            self.large_btn_pressed = False
        if self.cycle_btn.check_pressed():
            self.simple_btn_pressed = False
            self.cycle_btn_pressed = True
            self.complete_btn_pressed = False
            self.large_btn_pressed = False
        if self.complete_btn.check_pressed():
            self.simple_btn_pressed = False
            self.cycle_btn_pressed = False
            self.complete_btn_pressed = True
            self.large_btn_pressed = False
        if self.large_btn.check_pressed():
            self.simple_btn_pressed = False
            self.cycle_btn_pressed = False
            self.complete_btn_pressed = False
            self.large_btn_pressed = True
        
        if self.start_btn_pressed:
            if self.bfs_btn_pressed:
                if not self.queue and not self.visited:
                    self.start_bfs(self.selected_node)
                self.bfs_step()
            elif self.dfs_btn_pressed:
                if not self.stack and not self.visited:
                    self.start_dfs(self.selected_node)
                self.dfs_step()
        
        if self.simple_btn_pressed:
            self.clear_graph()
            self.load_sample('simple')
        if self.cycle_btn_pressed:
            self.clear_graph()
            self.load_sample('cycle')
        if self.complete_btn_pressed:
            self.clear_graph()
            self.load_sample('complete')
        if self.large_btn_pressed:
            self.clear_graph()
            self.load_sample('large')
            
        
        self.draw_text('Graph Visualization', (30, 50), font_size=24)
        if self.algorithm == 'BFS':
            self.draw_text('Algorithm: BFS', (30, 80))
            self.draw_text(f"Queue: {list(map(lambda node: self.nodes[node], self.queue))}", (30, 110))
        elif self.algorithm == 'DFS':
            self.draw_text('Algorithm: BFS', (30, 80))
            self.draw_text(f"Stack: {list(map(lambda node: self.nodes[node], self.stack))}", (30, 110))
        self.draw_text(f'Visited: {list(map(lambda node: self.nodes[node], self.visited))}', (30, 140))