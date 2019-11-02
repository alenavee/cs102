import pygame
import random
import time
from pygame.locals import *
import copy
from typing import List, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.grid = copy.deepcopy(self.get_next_generation())

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        self.grid = [[0] * self.cell_width for _ in range(self.cell_height)]
        if randomize:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    self.grid[i][j] = randomize * (random.randint(0, 1))
        return self.grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                cell_color = pygame.Color('white')
                if self.grid[i][j]:
                    cell_color = pygame.Color('green')
                pygame.draw.rect(self.screen, cell_color,
                                 (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, 1для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        row, col = cell
        neighbours = []
        if col > 0:
            neighbours.append(self.grid[row][col - 1])
        if col < self.cell_width - 1:
            neighbours.append(self.grid[row][col + 1])
        if row > 0:
            neighbours.append(self.grid[row - 1][col])
            if col > 0:
                neighbours.append(self.grid[row - 1][col - 1])
            if col < self.cell_width - 1:
                neighbours.append(self.grid[row - 1][col + 1])
        if row < self.cell_height - 1:
            neighbours.append(self.grid[row + 1][col])
            if col > 0:
                neighbours.append(self.grid[row + 1][col - 1])
            if col < self.cell_width - 1:
                neighbours.append(self.grid[row + 1][col + 1])

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = copy.deepcopy(self.grid)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                neighbours = self.get_neighbours((i, j)).count(1)
                if neighbours == 3:
                    new_grid[i][j] = 1
                elif neighbours == 2 and self.grid[i][j] == 1:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0
        return new_grid


if __name__ == '__main__':
    game = GameOfLife(320, 240, 40)
    game.run()
