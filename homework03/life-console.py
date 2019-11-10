import curses

from life import GameOfLife
from ui import UI
import os


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border('|', '|', '-', '-', '+', '+', '+', '+')

    def draw_grid(self, screen) -> None:
        for i in range(0, self.life.rows):
            for j in range(0, self.life.cols):

                screen.addstr(j+1, i+1, '*'
                                 if self.life.curr_generation[i][j] else ' ')

    def run(self) -> None:

        screen = curses.initscr()
        self.draw_borders(screen)
        curses.curs_set(0)
        screen.keypad(True)

        self.life.create_grid(True)
        running = True
        while running and self.life.is_changing and \
                not self.life.is_max_generations_exceed:
            self.life.step()
            self.draw_grid(screen)
            screen.refresh()
        curses.endwin()


if __name__ == '__main__':
    os.system('clear')
    gui = Console(GameOfLife((30, 20), True, 50))
    gui.run()
