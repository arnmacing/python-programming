import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
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

        # Список клеток
        self.grid = self.create_grid()

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            self.draw_grid()
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
        # создание матрицы клеток размером cell_height/width
        grid = [
            #  клетка может находиться в двух состояниях: «живая» или «мертвая»
            [random.randint(0, 1) if randomize else 0 for _ in range(self.cell_width)]
            for _ in range(self.cell_height)
        ]
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for h in range(self.cell_height):
            for w in range(self.cell_width):
                y = h * self.cell_size
                x = w * self.cell_size
                color = pygame.Color("white") if self.grid[h][w] == 0 else pygame.Color("green")
                # принимает: screen - где нужно отрисовать прямоугольник; цвет; координаты прямоугольника (x,y,
                # длина a,длина b)
                pygame.draw.rect(
                    self.screen,
                    color,
                    [x + 1, y + 1, self.cell_size - 1, self.cell_size - 1],
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        # получает для клетки список ее соседей
        neighbours = []
        # Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        # то есть, во всех направлениях.
        for i in range(-1, 2):
            for j in range(-1, 2):
                h = cell[0] + i
                w = cell[1] + j
                if i == 0 and j == 0:  # мёртвые клетки
                    continue
                if 0 <= w < self.cell_width and 0 <= h < self.cell_height:
                    neighbours.append(self.grid[h][w])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = []
        for y, row in enumerate(
            self.grid
        ):  # enumerate вернет кортеж, счётчик количества элементов в
            # последовательности
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


GameOfLife(320, 240, 20).run()
