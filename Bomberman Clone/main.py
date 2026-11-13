
import pygame
import random

import config

from mapa import create_map

from logica import (
    can_walk,
    plant_bomb,
    get_blast_cells,
    explode,
    is_dangerous,
    move_enemy_to_safety
)

from desenho import draw_game


# INICIALIZACAO DO PYGAME
pygame.init()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Bomberman Clone")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)


# CRIAR UMA NOVA PARTIDA
def new_game():

    game = {
        "grid": create_map(),
        "player": [1, 1],
        "enemy": [config.COLS - 2, config.ROWS - 2],
        "bombs": [],
        "explosions": [],
        "game_state": "playing",
        "enemy_timer": pygame.time.get_ticks(),
        "menu_selection": 0,
        "pause_started": None
    }

    return game


# RETOMAR UMA PARTIDA PAUSADA
def resume_game(game):

    now = pygame.time.get_ticks()
    pause_duration = now - game["pause_started"]

    # Compensar o tempo das bombas
    for bomb in game["bombs"]:
        bomb["time"] += pause_duration

    # Compensar o tempo das explosoes
    for explosion in game["explosions"]:
        explosion["end"] += pause_duration

    # Compensar o temporizador do inimigo
    game["enemy_timer"] += pause_duration

    game["pause_started"] = None
    game["game_state"] = "playing"


# ESTADO INICIAL: MENU
game = new_game()
game["game_state"] = "menu"


# LOOP PRINCIPAL
running = True

while running:

    clock.tick(60)
    now = pygame.time.get_ticks()

    
    # EVENTOS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # ESC
            if event.key == pygame.K_ESCAPE:

                # Abrir pausa
                if game["game_state"] == "playing":

                    game["game_state"] = "paused"
                    game["pause_started"] = pygame.time.get_ticks()
                    game["menu_selection"] = 0

                # Retomar partida
                elif game["game_state"] == "paused":

                    resume_game(game)

                # Voltar ao menu depois da vitoria ou derrota
                elif game["game_state"] in ("won", "lost"):

                    game["game_state"] = "menu"
                    game["menu_selection"] = 0

            # MENU INICIAL
            elif game["game_state"] == "menu":

                if event.key in (pygame.K_UP, pygame.K_w):

                    game["menu_selection"] = (
                        game["menu_selection"] - 1
                    ) % 2

                elif event.key in (pygame.K_DOWN, pygame.K_s):

                    game["menu_selection"] = (
                        game["menu_selection"] + 1
                    ) % 2

                elif event.key == pygame.K_SPACE:

                    if game["menu_selection"] == 0:
                        game = new_game()

                    elif game["menu_selection"] == 1:
                        running = False

            # MENU DE PAUSA
            elif game["game_state"] == "paused":

                if event.key in (pygame.K_UP, pygame.K_w):

                    game["menu_selection"] = (
                        game["menu_selection"] - 1
                    ) % 3

                elif event.key in (pygame.K_DOWN, pygame.K_s):

                    game["menu_selection"] = (
                        game["menu_selection"] + 1
                    ) % 3

                elif event.key == pygame.K_SPACE:

                    if game["menu_selection"] == 0:
                        resume_game(game)

                    elif game["menu_selection"] == 1:
                        game["game_state"] = "menu"
                        game["menu_selection"] = 0

                    elif game["menu_selection"] == 2:
                        running = False

            # MENU DE VITORIA OU DERROTA
            elif game["game_state"] in ("won", "lost"):

                if event.key in (pygame.K_UP, pygame.K_w):

                    game["menu_selection"] = (
                        game["menu_selection"] - 1
                    ) % 3

                elif event.key in (pygame.K_DOWN, pygame.K_s):

                    game["menu_selection"] = (
                        game["menu_selection"] + 1
                    ) % 3

                elif event.key == pygame.K_SPACE:

                    if game["menu_selection"] == 0:
                        game = new_game()

                    elif game["menu_selection"] == 1:
                        game["game_state"] = "menu"
                        game["menu_selection"] = 0

                    elif game["menu_selection"] == 2:
                        running = False

            # PARTIDA
            elif game["game_state"] == "playing":

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
                    plant_bomb(game, "player")

                nx = game["player"][0] + dx
                ny = game["player"][1] + dy

                if (dx != 0 or dy != 0) and can_walk(game, nx, ny):
                    game["player"] = [nx, ny]


    # ATUALIZACAO DO JOGO
    if game["game_state"] == "playing":

        # Detonar bombas cujo tempo acabou
        for bomb in game["bombs"][:]:

            if now >= bomb["time"]:

                game["bombs"].remove(bomb)
                explode(game, bomb)

        # Remover explosoes antigas
        game["explosions"] = [
            e for e in game["explosions"]
            if now < e["end"]
        ]

        # O jogador morre se entrar numa explosao ativa
        if any(
            tuple(game["player"]) in e["cells"]
            for e in game["explosions"]
        ):
            game["game_state"] = "lost"

        # O inimigo morre se entrar numa explosao ativa
        if game["enemy"] and any(
            tuple(game["enemy"]) in e["cells"]
            for e in game["explosions"]
        ):
            game["enemy"].clear()

        # IA DO INIMIGO
        if game["game_state"] == "playing":

            decision_time = config.ENEMY_DECISION_TIME

            if game["enemy"] and is_dangerous(game, tuple(game["enemy"])):
                decision_time = config.ENEMY_FASTER_DECISION_TIME

            if game["enemy"] and now - game["enemy_timer"] >= decision_time:

                game["enemy_timer"] = now

                # PRIORIDADE 1: Fugir de qualquer perigo
                if is_dangerous(game, tuple(game["enemy"])):

                    move_enemy_to_safety(game)

                else:

                    # PRIORIDADE 2: Tentar atacar o jogador
                    planted = False

                    ex, ey = game["enemy"]
                    px, py = game["player"]

                    if ex == px or ey == py:

                        blast = get_blast_cells(game, tuple(game["enemy"]))

                        if tuple(game["player"]) in blast:
                            planted = plant_bomb(game, "enemy")

                    if planted:

                        move_enemy_to_safety(game)

                    else:

                        # PRIORIDADE 3: Movimentacao normal
                        directions = [
                            (1, 0),
                            (-1, 0),
                            (0, 1),
                            (0, -1)
                        ]

                        random.shuffle(directions)

                        for dx, dy in directions:

                            nx = game["enemy"][0] + dx
                            ny = game["enemy"][1] + dy

                            if not can_walk(game, nx, ny):
                                continue

                            if [nx, ny] == game["player"]:
                                continue

                            if is_dangerous(game, (nx, ny)):
                                continue

                            game["enemy"][:] = [nx, ny]
                            break

            # Encostar no inimigo causa derrota
            if game["enemy"] and game["enemy"] == game["player"]:
                game["game_state"] = "lost"

            # Vencer eliminando o inimigo
            if not game["enemy"] and game["game_state"] == "playing":
                game["game_state"] = "won"

    # DESENHAR
    draw_game(screen, font, game)


pygame.quit()
