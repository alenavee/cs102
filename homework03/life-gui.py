import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                cell_color = pygame.Color('white')
                if self.grid[i][j]:
                    cell_color = pygame.Color('green')
                pygame.draw.rect(self.screen, cell_color,
                                 (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.life.create_grid(True)

        running = True
        while running and self.life.is_changing and not self.life.is_max_generations_exceed:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                    elif event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            paused = not paused
                    elif event.type == pygame.MOUSEBUTTONUP:
                        cli_x, cli_y = event.pos
                        cli_x //= self.cell_size
                        cli_y //= self.cell_size
                        self.life.curr_generation[cli_y][cli_x] = \
                            int(not bool(self.life.curr_generation[cli_y][cli_x]))

                        self.draw_grid()
                        pygame.display.flip()
                if paused:
                    self.draw_grid()
                    pygame.display.flip()
                    continue
                # Отрисовка списка клеток
                # Выполнение одного шага игры (обновление состояния ячеек)

                self.draw_lines()
                self.draw_grid()
                self.life.step()
                pygame.display.flip()
                clock.tick(self.speed)
            pygame.quit()

if __name__ == '__main__':
    ui = GUI(GameOfLife((10, 10), True, 50))
    ui.run()