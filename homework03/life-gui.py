import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        self.cell_size = cell_size
        self.speed = speed
        self.screen = pygame.display.set_mode((life.cols * self.cell_size, life.rows * self.cell_size))
        super().__init__(life)

    def draw_lines(self) -> None:
        for x in range(0, self.life.cols*self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.life.rows*self.cell_size))
        for y in range(0, self.life.rows*self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.life.cols*self.cell_size, y))

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                cell_color = pygame.Color('white')
                if self.life.curr_generation[i][j]:
                    cell_color = pygame.Color('green')
                pygame.draw.rect(self.screen, cell_color,
                                 (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('black'))

        running = True
        pause = False
        while running and not self.life.is_max_generations_exceed and self.life.is_changing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYUP and event.key == K_SPACE:
                    pause = not pause
                elif event.type == MOUSEBUTTONUP and pause:
                    j, i = pygame.mouse.get_pos()
                    i = i // self.cell_size
                    j = j // self.cell_size
                    if self.life.curr_generation[i][j] == 1:
                        self.life.curr_generation[i][j] = 0
                    else:
                        self.life.curr_generation[i][j] = 1

            self.draw_grid()
            self.draw_lines()
            if not pause:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == '__main__':
    ui = GUI(GameOfLife((10, 10), True, 50))
    ui.run()
