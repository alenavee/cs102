import pathlib
import random
import copy

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool = True,
        max_generations: Optional[float] = float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.n_generation = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0] * self.cols for _ in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = randomize * (random.randint(0, 1))
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours = []
        if col > 0:
            neighbours.append(self.curr_generation[row][col - 1])
        if col < self.cols - 1:
            neighbours.append(self.curr_generation[row][col + 1])
        if row > 0:
            neighbours.append(self.curr_generation[row - 1][col])
            if col > 0:
                neighbours.append(self.curr_generation[row - 1][col - 1])
            if col < self.cols - 1:
                neighbours.append(self.curr_generation[row - 1][col + 1])
        if row < self.rows - 1:
            neighbours.append(self.curr_generation[row + 1][col])
            if col > 0:
                neighbours.append(self.curr_generation[row + 1][col - 1])
            if col < self.cols - 1:
                neighbours.append(self.curr_generation[row + 1][col + 1])

        return neighbours

    def get_next_generation(self) -> Grid:
        for i in range(self.rows):
            for j in range(self.cols):
                self.prev_generation[i][j] = self.curr_generation[i][j]
        new_grid = copy.deepcopy(self.curr_generation)
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[i])):
                neighbours = self.get_neighbours((i, j)).count(1)
                if neighbours == 3:
                    new_grid[i][j] = 1
                elif neighbours == 2 and self.curr_generation[i][j] == 1:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """

        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.n_generation < self.max_generations:
            return False
        return True

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation == self.prev_generation:
            return False
        return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        strings = filename.read_text().split('\n')
        rows = len(strings)
        cols = len(strings[0])
        strings = strings[:-1]
        for s in strings:
            sub_array = []
            for char in s:
                sub_array.append(int(char))
            grid.append(sub_array)
        game = GameOfLife((rows, cols), False)
        game.curr_generation = copy.deepcopy(grid)
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, 'w')
        for s in self.curr_generation:
            for item in s:
                f.write(str(item).replace("'", ''))
            f.write('\n')
