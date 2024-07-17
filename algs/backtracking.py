import pygame
import pygame_gui
import time
from algs.visualization import Visualization
    
class NQueensVisualization(Visualization):
    def __init__(self, screen):
        self.screen = screen
        self.n = 8
        self.cell_size = 50
        self.board = [[0 for _ in range(self.n)] for _ in range(self.n)]
        self.current_col = 0
        self.solved = False
        
        self.ui_manager = pygame_gui.UIManager((1280,720))
        self.start_btn = pygame_gui.elements.UIButton(pygame.Rect((600, 0), (75, 40)), 'Start', self.ui_manager)
        self.fwd_btn = pygame_gui.elements.UIButton(pygame.Rect((600, 50), (75, 40)), 'Step Fwd', self.ui_manager)
        self.bck_btn = pygame_gui.elements.UIButton(pygame.Rect((600, 100), (75, 40)), 'Step Back', self.ui_manager)
        self.reset_btn = pygame_gui.elements.UIButton(pygame.Rect((600, 150), (75, 40)), 'Reset', self.ui_manager)
        self.start_btn_pressed = False
        
        self.states = []
        self.current_state_index = -1
        
        self.message = 'Click "Start" to begin'
        
    def save_state(self):
        self.states.append((self.board, self.current_col))
        self.current_state_index = len(self.states) - 1
        self.message = f"Column {self.current_col} processed"
        
    def load_state(self, index):
        if 0 <= index < len(self.states):
            state = self.states[index]
            self.board, self.current_col = state
            self.render()
            
    def next_step(self):
        if self.current_state_index < len(self.states) - 1:
            self.current_state_index += 1
            self.load_state(self.current_state_index)
            self.message = f"Stepping forward to state {self.current_state_index + 1}"
            
    def prev_step(self):
        if self.current_state_index > 0:
            self.current_state_index -= 1
            self.load_state(self.current_state_index)
            self.message = f"Stepping back to state {self.current_state_index + 1}"
    
    def solve_step(self):
        if self.current_col >= self.n:
            self.solved = True
            return
        
        if self.solve_n_queens_util(self.current_col):
            self.save_state()
            self.render()
            self.current_col += 1
        else:
            self.solved = True
    
    def render_board(self):
        for x in range(self.n):
            for y in range(self.n):
                color = (200,200,200) if (x + y) % 2 == 0 else (220,220,220)
                pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                if self.board[y][x] == 1:
                    pygame.draw.circle(self.screen, (0,0,0), (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2), self.cell_size // 3)
        pygame.display.flip()
    
    def render(self):
        self.screen.fill((255,255,255))
        self.render_board()
        
        if self.start_btn.check_pressed():
            self.start_btn.pressed = False
            self.start_btn_pressed = True
        
        if self.start_btn_pressed and not self.solved:
            self.solve_step()
        if self.fwd_btn.check_pressed():
            self.start_btn_pressed = False
            self.next_step()
        if self.bck_btn.check_pressed():
            self.start_btn_pressed = False
            self.prev_step()
        if self.reset_btn.check_pressed():
            self.__init__(self.screen)
        
        pygame.display.flip()
        
    
    def handle_mouse_click(self, pos, button):
        pass
    
    def is_safe(self, row, col):
        for i in range(col):
            if self.board[row][i] == 1:
                return False

        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False

        for i, j in zip(range(row, self.n, 1), range(col, -1, -1)):
            if self.board[i][j] == 1:
                return False

        return True

    def solve_n_queens_util(self, col):
        if col >= self.n:
            return True
        time.sleep(0.25)
        for i in range(self.n):
            if self.is_safe(i, col):
                self.board[i][col] = 1
                self.render_board()
                if self.solve_n_queens_util(col + 1):
                    return True
                self.board[i][col] = 0
                self.render_board()

        return False