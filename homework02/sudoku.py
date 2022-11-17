import pathlib
import random
import typing as tp

T = tp.TypeVar("T")  # Возможные типа переменных: может быть что угодно


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]  # создаётся массив из каждого прочитанного элементе
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    width = 3  # ширина разметки
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[
    T]]:  # Создаетcя новый список, в котором каждый элемент списка является результатом некоторой операции,
    # примененной к каждому элементу
    return [values[idx:idx + n] for idx in range(0, len(values), n)]  # срез массива


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return [grid[i][pos[1]] for i in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    # Возвращает все значения из квадрата, в который попадает позиция pos
    row = pos[0] // 3 * 3
    col = pos[1] // 3 * 3
    # Возвращает все значения из квадрата, в который попадает позиция pos (всего 9 квадратов размером 3*3).
    return [
        grid[row][column] for row in range(row, row + 3) for column in range(col, col + 3)
    ]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == ".":
                # возвращает первую попавшуюся свободную позицию
                return row, col


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    # значения, которые на эту позицию можно поставить
    return set('123456789') - set(get_row(grid, pos)) - set(get_col(grid, pos)) - set(get_block(grid, pos))


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    free_position = find_empty_positions(grid)
    if not free_position:  # свободных позиций нет
        return grid
    possible_values = find_possible_values(grid, free_position)
    # методом перебора (поиска) с возвратом
    for value in possible_values:
        grid[free_position[0]][free_position[1]] = value
        solution = solve(grid)
        if solution is not None:  # если решается
            return solution  # решаем
    grid[free_position[0]][free_position[1]] = '.'


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    # Решение оказывается верным, если ни в одной строке, ни в одном столбце, ни в квадрате не повторяются значения
    for row in range(len(solution)):
        if set(get_row(solution, (row, 0))) != set('123456789'):
            return False
    for col in range(len(solution)):
        if set(get_col(solution, (0, col))) != set("123456789"):
            return False
    for row in range(len(solution), 3):
        for col in range(len(solution), 3):
            if set(get_block(solution, (row, col))) != set('123456789'):
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    # создает новый судоку, заполненный на N элементов
    grid = solve([['.'] * 9 for _ in range(9)])
    random_sudoku = solve(grid)
    for p in range(81 - N):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while random_sudoku[row][col] == ".":
            row, col = random.randint(0, 8), random.randint(0, 8)
        random_sudoku[row][col] = "."
    return random_sudoku


if __name__ == "__main__":
    # строка выше вернет True только в том случае, если программа будет запущена прямо
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
