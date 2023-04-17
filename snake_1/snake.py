import globals as g
import pygame

def draw_text(surface, str, color, pos):
    text = g.font.render(str, True, color)
    surface.blit(text, pos)

def drawGrid(cells_x, cells_y, cell_w, cell_h, surface):

    for i in range(cells_x):
        x = i * cell_w
        pygame.draw.line(surface, (128, 128, 128), (x, 0), (x, g.window_height))
    
    for i in range(cells_y):
        y = i * cell_h
        pygame.draw.line(surface, (128, 128, 128), (0, y), (g.window_width, y))

def draw_cube(surface, pos, color):
    pygame.draw.rect(surface, color, 
        (pos[0] * g.cell_width, pos[1] * g.cell_height, g.cell_width, g.cell_height))

class Cube:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
    
    def draw(self, surface):
        draw_cube(surface, self.pos, self.color)

class Snake:
    def __init__(self, pos):
        self.body = [Cube(pos, (255, 0, 0))]
        self.direction = g.RIGHT
    
    def move(self):
        self.body[0].pos = (\
            self.body[0].pos[0] + self.direction[0],
            self.body[0].pos[1] + self.direction[1])
    
    def draw(self, surface):
        for cube in self.body:
            cube.draw(surface)

class Game:

    def __init__(self):
        self.snake = Snake(g.START)
        self.update_counter = 0
    
    def update(self):
        self.update_counter += 1

        if self.update_counter % g.GAMESPEED == 0:
            self.snake.move()

    def render(self, surface):
        self.snake.draw(surface)

        drawGrid(g.cells_x, g.cells_y, g.cell_width, g.cell_height, surface)

def main():

    # システムの初期化
    pygame.init()
    window = pygame.display.set_mode((g.window_width, g.window_height))
    g.font = pygame.font.Font("C:\Windows\Fonts\meiryo.ttc", 20)
    clock = pygame.time.Clock()

    # ゲームの作成
    game = Game()

    while True:
    
        window.fill((0, 0, 0))

        game.update()
        game.render(window)
        
        # FPSの表示
        draw_text(window, str(round(clock.get_fps(), 2)), (255, 255, 255), (440, 0))
        
        pygame.display.update()
        
        clock.tick(g.FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == '__main__':
    main()
