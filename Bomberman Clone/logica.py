import pygame

from config import (
    COLS,
    ROWS,
    BOMB_RANGE,
    BOMB_TIMER,
    EXPLOSION_DURATION,
    EMPTY_TILE,
    UNBREAKABLE_WALL,
    BREAKABLE_WALL
)

# Verifica se uma casa pode ser ocupada
def can_walk(game, x, y):

    if not (0 <= x < COLS and 0 <= y < ROWS):
        return False

    if game["grid"][y][x] != EMPTY_TILE:
        return False

    for bomb in game["bombs"]:
        if bomb["pos"] == (x, y):
            return False

    return True

# Coloca uma bomba
def plant_bomb(game, owner):

    # Identifica a posicao de quem vai colocar a bomba
    if owner == "player":
        pos = tuple(game["player"])

    elif owner == "enemy":
        if not game["enemy"]:
            return False

        pos = tuple(game["enemy"])

    else:
        return False

    # Impede mais de uma bomba por personagem
    if any(b["owner"] == owner for b in game["bombs"]):
        return False

    game["bombs"].append({
        "pos": pos,
        "time": pygame.time.get_ticks() + BOMB_TIMER,
        "owner": owner
    })

    return True


# Calcula as casas atingidas pela explosao
def get_blast_cells(game, pos):

    x, y = pos
    blast = [(x, y)]

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for dx, dy in directions:

        for distance in range(1, BOMB_RANGE + 1):

            nx = x + dx * distance
            ny = y + dy * distance

            if not (0 <= nx < COLS and 0 <= ny < ROWS):
                break

            if game["grid"][ny][nx] == UNBREAKABLE_WALL:
                break

            blast.append((nx, ny))

            if game["grid"][ny][nx] == BREAKABLE_WALL:
                break

    return blast


# Detona uma bomba
def explode(game, bomb):

    blast = get_blast_cells(game, bomb["pos"])

    # Destroi os blocos atingidos
    for x, y in blast:

        if game["grid"][y][x] == BREAKABLE_WALL:
            game["grid"][y][x] = EMPTY_TILE

    # Cria a explosao
    now = pygame.time.get_ticks()

    game["explosions"].append({
        "cells": blast,
        "end": now + EXPLOSION_DURATION
    })

    # Elimina o inimigo atingido
    if game["enemy"] and tuple(game["enemy"]) in blast:
        game["enemy"].clear()

    # Elimina o jogador atingido
    if tuple(game["player"]) in blast:
        game["game_state"] = "lost"


# Verifica se uma posicao esta em perigo
def is_dangerous(game, pos):

    # Verifica bombas que ainda vao explodir
    for bomb in game["bombs"]:

        if pos in get_blast_cells(game, bomb["pos"]):
            return True

    # Verifica explosoes ativas
    for explosion in game["explosions"]:

        if pos in explosion["cells"]:
            return True

    return False


# Procura uma rota de fuga para o inimigo
def move_enemy_to_safety(game):

    if not game["enemy"]:
        return

    start = tuple(game["enemy"])

    # Fila de posicoes para explorar
    queue = [(start, [])]

    # Posicoes ja visitadas
    visited = {start}

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:

        pos, path = queue.pop(0)

        # Encontrou uma posicao segura
        if not is_dangerous(game, pos) and pos != start:

            game["enemy"][:] = list(path[0])
            return

        # Explora as casas vizinhas
        for dx, dy in directions:

            nx = pos[0] + dx
            ny = pos[1] + dy

            new_pos = (nx, ny)

            if new_pos in visited:
                continue

            if not can_walk(game, nx, ny):
                continue

            if [nx, ny] == game["player"]:
                continue

            visited.add(new_pos)

            new_path = path + [new_pos]

            queue.append((new_pos, new_path))
