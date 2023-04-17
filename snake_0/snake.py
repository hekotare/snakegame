import globals as g
import pygame

def draw_text(surface, str, color, pos):
    text = g.font.render(str, True, color)
    surface.blit(text, pos)

class Game():

    def update(self):
        pass

    def render(self):
        pass

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
        game.render()
        
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
