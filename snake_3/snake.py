import random
import pygame
import globals as g


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
        self.direction_input = g.RIGHT
    
    def input_direction(self):
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_UP] and self.direction != g.DOWN:
            self.direction_input = g.UP
        elif pressed[pygame.K_DOWN] and self.direction != g.UP:
            self.direction_input = g.DOWN
        elif pressed[pygame.K_LEFT] and self.direction != g.RIGHT:
            self.direction_input = g.LEFT
        elif pressed[pygame.K_RIGHT] and self.direction != g.LEFT:
            self.direction_input = g.RIGHT
    
    def move(self):
    
        self.direction = self.direction_input
        
        # エサをたべたとき、ここが新たな最後尾となる
        self.add_target_pos = self.body[-1].pos
        
        # お尻のキューブから順番に１つ前に移動する（先頭キューブは対象外）
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].pos = self.body[i - 1].pos
        
        # 先頭を新しい座標に移動する
        self.body[0].pos = (\
            self.body[0].pos[0] + self.direction[0],
            self.body[0].pos[1] + self.direction[1])
        
    def add_body(self, color):
        self.body.append(Cube(self.add_target_pos, color))
    
    def draw(self, surface):
        for cube in self.body:
            cube.draw(surface)

class Game:

    class State:
        MainGame = 1
        GameOver = 2
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.snake = Snake(g.START)
        self.update_counter = 0
        self.state = self.State.MainGame
        self.generate_food()
    
    def generate_food(self):
    
        snake_body_list = [cube.pos for cube in self.snake.body]
        
        while True:
            x = random.randint(0, g.cells_x - 1)
            y = random.randint(0, g.cells_y - 1)
            
            # ヘビの体と重ならない座標にエサを作成
            if ((x, y) not in snake_body_list):
                self.food = Cube((x, y), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                break

    
    def update(self):

        if self.state == self.State.MainGame:
            self.update_maingame()
        elif self.state == self.State.GameOver:
            self.update_gameover()
    
    def update_maingame(self):
        self.update_counter += 1
        
        self.snake.input_direction()
        
        if self.update_counter % g.GAMESPEED == 0:
            self.snake.move()
            
            if (self.check_death()):
                self.death_event()
            elif (self.check_food()):
                self.snake.add_body(self.food.color)
                self.generate_food()
    
    def update_gameover(self):
        
        pressed = pygame.key.get_pressed()
        
        if pressed[pygame.K_SPACE]:
            self.reset()
    
    def check_death(self):
        x, y = self.snake.body[0].pos
        
        # ヘビがワールドの外に出た
        if not (0 <= x < g.cells_x and 0 <= y < g.cells_y):
            return True
        
        # ヘビの体が重複していないかチェック
        if (len(self.snake.body) != len(set([cube.pos for cube in self.snake.body]))):
            return True
        
        return False
    
    def check_food(self):
        return self.food.pos == self.snake.body[0].pos
    
    def death_event(self):
        self.state = self.State.GameOver
    
    def render(self, surface):
        self.snake.draw(surface)
        self.food.draw(surface)
        
        drawGrid(g.cells_x, g.cells_y, g.cell_width, g.cell_height, surface)
        
        if self.state == self.State.GameOver:
            draw_text(surface, "- Game Over -", (255, 128, 128), (160, 128))
            draw_text(surface, "Retry (push space key)", (255, 128, 128), (160, 180))

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
