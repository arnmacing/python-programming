import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        grid = self.life.curr_generation  # текущее поколение клеток
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                cell = "*" if grid[i][j] == 1 else " "  # живая/мёртвая
                screen.addch(i + 1, j + 1, cell)
                # принимает символ, который может быть либо строкой длины 1,
                # либо промежуточным тестированием длины 1, либо целым числом

    def run(self) -> None:
        screen = curses.initscr()
        # PUT YOUR CODE HERE
        curses.resizeterm(self.life.rows + 2, self.life.cols + 2)
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.life.step()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            curses.napms(500)
        curses.endwin()


Console(GameOfLife((24, 80), max_generations=50)).run()
