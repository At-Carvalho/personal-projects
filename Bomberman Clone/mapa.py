import random

from config import (
    COLS,
    ROWS,
    EMPTY_TILE,
    UNBREAKABLE_WALL,
    BREAKABLE_WALL,
    BREAKABLE_WALL_SPAWNRATE
)


# Cria o mapa
def create_map():
    grid = [[EMPTY_TILE for x in range(COLS)] for y in range(ROWS)]

    for y in range(ROWS):
        for x in range(COLS):

            if x == 0 or y == 0 or x == COLS - 1 or y == ROWS - 1:
                grid[y][x] = UNBREAKABLE_WALL

            elif x % 2 == 0 and y % 2 == 0:
                grid[y][x] = UNBREAKABLE_WALL

            elif random.random() < BREAKABLE_WALL_SPAWNRATE:
                grid[y][x] = BREAKABLE_WALL

    # Deixar a saida inicial livre
    for x, y in [(1, 1), (2, 1), (1, 2)]:
        grid[y][x] = EMPTY_TILE

    # Deixar o inimigo nascer em uma casa livre
    grid[ROWS - 2][COLS - 2] = EMPTY_TILE

    return grid
