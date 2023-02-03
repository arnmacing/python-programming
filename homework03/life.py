import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
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
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        return [[random.randint(0, 1) if randomize else 0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        neighbours = []
        for i in range(-1, 2):
            h = cell[0] + i
            for j in range(-1, 2):
                w = cell[1] + j
                if i == 0 and j == 0:
                    continue
                if 0 <= w < self.cols and 0 <= h < self.rows:
                    neighbours.append(self.curr_generation[h][w])
        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_grid = []
        for y, row in enumerate(self.curr_generation):
            new_row = []
            for x, cell in enumerate(row):
                neighbours = self.get_neighbours((y, x))
                live_neighbours = neighbours.count(1)
                if cell and (live_neighbours < 2 or live_neighbours > 3):
                    new_row.append(0)
                elif not cell and live_neighbours == 3:
                    new_row.append(1)
                else:
                    new_row.append(cell)
            new_grid.append(new_row)
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation  # предыдущее = текущее
        next_generation = self.get_next_generation()
        self.curr_generation = next_generation  # текущее = следующее
        self.generations += 1  # + поколение

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return bool(self.max_generations and self.generations >= self.max_generations)

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with filename.open() as file:
            grid = [list(map(int, col.strip())) for col in file.readlines()]
        size = len(grid), len(grid[0])
        game = GameOfLife(size, randomize=False)
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with filename.open("w") as file:
            file.write("\n".join(["".join(map(str, col)) for col in self.curr_generation]))
