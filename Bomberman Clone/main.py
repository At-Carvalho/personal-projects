import pygame
import random

pygame.init()

# CONFIGURACOES
TILE = 48
COLS = 15
ROWS = 11
HUD = 48

WIDTH = COLS * TILE
HEIGHT = ROWS * TILE + HUD

BOMB_RANGE = 2
BOMB_TIMER = 1800
EXPLOSION_DURATION = 400
ENEMY_DECISION_TIME = 800
ENEMY_FASTER_DECISION_TIME = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomberman")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# CORES
BLACK = (20, 20, 25)
WHITE = (240, 240, 240)
BLUE = (60, 150, 255)
RED = (230, 60, 60)
YELLOW = (255, 210, 50)
GREEN = (50, 190, 90)
GRAY = (100, 100, 110)
BROWN = (150, 95, 55)
ORANGE = (255, 125, 25)

# MAPA: 0 = livre, 1 = parede, 2 = bloco
def create_map():
    grid = [[0 for x in range(COLS)] for y in range(ROWS)]

    for y in range(ROWS):
        for x in range(COLS):
            if x == 0 or y == 0 or x == COLS - 1 or y == ROWS - 1:
                grid[y][x] = 1
            elif x % 2 == 0 and y % 2 == 0:
                grid[y][x] = 1
            elif random.random() < 0.28:
                grid[y][x] = 2

    # Deixar a saida inicial livre
    for x, y in [(1, 1), (2, 1), (1, 2)]:
        grid[y][x] = 0

    # Deixar o inimigo nascer em uma casa livre
    grid[ROWS - 2][COLS - 2] = 0
    return grid


def new_game():
    global grid, player, enemy, bombs, explosions
    global game_state, enemy_timer

    grid = create_map()
    player = [1, 1]
    enemy = [COLS - 2, ROWS - 2]
    bombs = []
    explosions = []
    game_state = "playing"
    enemy_timer = pygame.time.get_ticks()


# Verifica se uma casa pode ser ocupada
def can_walk(x, y):
    if not (0 <= x < COLS and 0 <= y < ROWS):
        return False

    if grid[y][x] != 0:
        return False

    for bomb in bombs:
        if bomb["pos"] == (x, y):
            return False

    return True


def plant_bomb(owner):

    # Identifica a posicao de quem vai colocar a bomba
    if owner == "player":
        pos = tuple(player)

    elif owner == "enemy":
        if not enemy:
            return False

        pos = tuple(enemy)

    else:
        return False

    # Impede mais de uma bomba por personagem
    if any(b["owner"] == owner for b in bombs):
        return False

    bombs.append({
        "pos": pos,
        "time": pygame.time.get_ticks() + BOMB_TIMER,
        "owner": owner
    })

    return True


def get_blast_cells(pos):
    x, y = pos
    blast = [(x, y)]

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for dx, dy in directions:
        for distance in range(1, BOMB_RANGE + 1):
            nx = x + dx * distance
            ny = y + dy * distance

            if not (0 <= nx < COLS and 0 <= ny < ROWS):
                break

            if grid[ny][nx] == 1:
                break

            blast.append((nx, ny))

            if grid[ny][nx] == 2:
                break

    return blast

def explode(bomb):
    global game_state

    # Calcula todas as casas atingidas
    blast = get_blast_cells(bomb["pos"])

    # Destroi os blocos atingidos
    for x, y in blast:
        if grid[y][x] == 2:
            grid[y][x] = 0

    # Cria a explosao
    now = pygame.time.get_ticks()

    explosions.append({
        "cells": blast,
        "end": now + EXPLOSION_DURATION
    })

    # Elimina o inimigo atingido
    if enemy and tuple(enemy) in blast:
        enemy.clear()

    # Elimina o jogador atingido
    if tuple(player) in blast:
        game_state = "lost"


def is_dangerous(pos):

    for bomb in bombs:
        if pos in get_blast_cells(bomb["pos"]):
            return True
    
    for explosion in explosions:
        if pos in explosion["cells"]:
            return True
            
    return False

def move_enemy_to_safety():

    if not enemy:
        return

    start = tuple(enemy)

    # Fila de posicoes para explorar
    queue = [(start, [])]

    # Posicoes ja visitadas
    visited = {start}

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:

        pos, path = queue.pop(0)

        # Encontrou uma posicao segura
        if not is_dangerous(pos) and pos != start:
            enemy[:] = list(path[0])
            return

        # Explorar as casas vizinhas
        for dx, dy in directions:

            nx = pos[0] + dx
            ny = pos[1] + dy

            new_pos = (nx, ny)

            if new_pos in visited:
                continue

            if not can_walk(nx, ny):
                continue

            if [nx, ny] == player:
                continue

            visited.add(new_pos)

            new_path = path + [new_pos]

            queue.append((new_pos, new_path))

def draw_cell(x, y, color):
    rect = pygame.Rect(x * TILE, y * TILE, TILE, TILE)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


def draw_game():
    screen.fill(BLACK)

    for y in range(ROWS):
        for x in range(COLS):
            draw_cell(x, y, (45, 65, 50))

            if grid[y][x] == 1:
                draw_cell(x, y, GRAY)
            elif grid[y][x] == 2:
                draw_cell(x, y, BROWN)

    # Bombas
    for bomb in bombs:
        x, y = bomb["pos"]
        center = (x * TILE + TILE // 2, y * TILE + TILE // 2)
        pygame.draw.circle(screen, BLACK, center, TILE // 3)
        pygame.draw.circle(screen, WHITE, center, TILE // 3, 2)

    # Explosoes
    for explosion in explosions:
        for x, y in explosion["cells"]:
            rect = pygame.Rect(
                x * TILE + 4, y * TILE + 4,
                TILE - 8, TILE - 8
            )
            pygame.draw.rect(screen, ORANGE, rect)
            pygame.draw.rect(screen, YELLOW, rect, 5)

    # Jogador
    if game_state != "lost":
        px = player[0] * TILE + TILE // 2
        py = player[1] * TILE + TILE // 2
        pygame.draw.circle(screen, BLUE, (px, py), TILE // 3)

    # Inimigo
    if enemy:
        ex = enemy[0] * TILE + TILE // 2
        ey = enemy[1] * TILE + TILE // 2
        pygame.draw.circle(screen, RED, (ex, ey), TILE // 3)

    # HUD
    pygame.draw.rect(screen, BLACK, (0, ROWS * TILE, WIDTH, HUD))

    if game_state == "playing":
        msg = "WASD ou Setas: mover | ESPACO: bomba"
    elif game_state == "won":
        msg = "VITORIA! Aperte R para reiniciar"
    else:
        msg = "DERROTA! Aperte R para reiniciar"

    text = font.render(msg, True, WHITE)
    screen.blit(text, (10, ROWS * TILE + 14))

    pygame.display.flip()


new_game()

# LOOP PRINCIPAL
running = True

while running:
    clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_r and game_state != "playing":
                new_game()

            if game_state == "playing":
                dx, dy = 0, 0

                if event.key in (pygame.K_UP, pygame.K_w):
                    dy = -1
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    dy = 1
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    dx = -1
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    dx = 1
                elif event.key == pygame.K_SPACE:
                    plant_bomb("player")

                nx = player[0] + dx
                ny = player[1] + dy

                if (dx != 0 or dy != 0) and can_walk(nx, ny):
                    player = [nx, ny]

    if game_state == "playing":
        # Detonar bombas cujo tempo acabou
        for bomb in bombs[:]:
            if now >= bomb["time"]:
                bombs.remove(bomb)
                explode(bomb)

        # Remover explosoes antigas
        explosions = [
            e for e in explosions if now < e["end"]
        ]

        # O jogador tambem morre se entrar numa explosao ativa
        if any(tuple(player) in e["cells"] for e in explosions):
            game_state = "lost"

        # O inimigo tambem morre se entrar numa explosao ativa
        if enemy and any(tuple(enemy) in e["cells"] for e in explosions):
            enemy.clear()

        # "IA" do inimigo
        decision_time = ENEMY_DECISION_TIME

        if enemy and is_dangerous(tuple(enemy)):
            decision_time = ENEMY_FASTER_DECISION_TIME

        if enemy and now - enemy_timer >= decision_time:
            enemy_timer = now

            # PRIORIDADE 1: Fugir de qualquer perigo
            if is_dangerous(tuple(enemy)):
                move_enemy_to_safety()

            else:
                # PRIORIDADE 2: Tentar atacar o jogador
                planted = False

                ex, ey = enemy
                px, py = player

                if (ex == px or ey == py):
                    blast = get_blast_cells(tuple(enemy))

                    if tuple(player) in blast:
                        planted = plant_bomb("enemy")

                if planted:
                    move_enemy_to_safety()

                else:
                    # PRIORIDADE 3: Movimentacao normal
                    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                    random.shuffle(directions)

                    for dx, dy in directions:
                        nx = enemy[0] + dx
                        ny = enemy[1] + dy

                        if not can_walk(nx, ny):
                            continue

                        if [nx, ny] == player:
                            continue

                        if is_dangerous((nx, ny)):
                            continue

                        enemy[:] = [nx, ny]
                        break

        # Encostar no inimigo causa derrota
        if enemy and enemy == player:
            game_state = "lost"

        # Vencer eliminando o inimigo
        if not enemy and game_state == "playing":
            game_state = "won"

    draw_game()

pygame.quit()
