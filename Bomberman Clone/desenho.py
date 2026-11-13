import pygame

from config import (
    TILE_SIZE,
    COLS,
    ROWS,
    HUD,
    WIDTH,
    BACKGROUND_COLOR,
    PLAYER_COLOR,
    ENEMY_COLOR,
    EMPTY_TILE_COLOR,
    UNBREAKABLE_WALL_COLOR,
    BREAKABLE_WALL_COLOR,
    OUTER_EXPLOSION_COLOR,
    INNER_EXPLOSION_COLOR,
    WHITE,
    UNBREAKABLE_WALL,
    BREAKABLE_WALL
)


# Desenha uma casa do mapa
def draw_cell(screen, x, y, color):

    rect = pygame.Rect(
        x * TILE_SIZE,
        y * TILE_SIZE,
        TILE_SIZE,
        TILE_SIZE
    )

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BACKGROUND_COLOR, rect, 1)


# Desenha o jogo inteiro
def draw_game(screen, font, game):

    screen.fill(BACKGROUND_COLOR)

    # Mapa
    for y in range(ROWS):

        for x in range(COLS):

            draw_cell(screen, x, y, EMPTY_TILE_COLOR)

            if game["grid"][y][x] == UNBREAKABLE_WALL:
                draw_cell(screen, x, y, UNBREAKABLE_WALL_COLOR)

            elif game["grid"][y][x] == BREAKABLE_WALL:
                draw_cell(screen, x, y, BREAKABLE_WALL_COLOR)

    # Bombas
    for bomb in game["bombs"]:

        x, y = bomb["pos"]

        center = (
            x * TILE_SIZE + TILE_SIZE // 2,
            y * TILE_SIZE + TILE_SIZE // 2
        )

        pygame.draw.circle(
            screen,
            BACKGROUND_COLOR,
            center,
            TILE_SIZE // 3
        )

        pygame.draw.circle(
            screen,
            WHITE,
            center,
            TILE_SIZE // 3,
            2
        )

    # Explosoes
    for explosion in game["explosions"]:

        for x, y in explosion["cells"]:

            rect = pygame.Rect(
                x * TILE_SIZE + 4,
                y * TILE_SIZE + 4,
                TILE_SIZE - 8,
                TILE_SIZE - 8
            )

            pygame.draw.rect(screen, INNER_EXPLOSION_COLOR, rect)
            pygame.draw.rect(screen, OUTER_EXPLOSION_COLOR, rect, 5)

    # Jogador
    if game["game_state"] != "lost":

        px = game["player"][0] * TILE_SIZE + TILE_SIZE // 2
        py = game["player"][1] * TILE_SIZE + TILE_SIZE // 2

        pygame.draw.circle(
            screen,
            PLAYER_COLOR,
            (px, py),
            TILE_SIZE // 3
        )

    # Inimigo
    if game["enemy"]:

        ex = game["enemy"][0] * TILE_SIZE + TILE_SIZE // 2
        ey = game["enemy"][1] * TILE_SIZE + TILE_SIZE // 2

        pygame.draw.circle(
            screen,
            ENEMY_COLOR,
            (ex, ey),
            TILE_SIZE // 3
        )

    # HUD
    pygame.draw.rect(
        screen,
        BACKGROUND_COLOR,
        (0, ROWS * TILE_SIZE, WIDTH, HUD)
    )

    if game["game_state"] == "playing":
        msg = "WASD ou Setas: mover | ESPACO: bomba"

    elif game["game_state"] == "won":
        msg = "VITORIA! Aperte R para reiniciar"

    else:
        msg = "DERROTA! Aperte R para reiniciar"

    text = font.render(msg, True, WHITE)

    screen.blit(
        text,
        (10, ROWS * TILE_SIZE + 14)
    )

    pygame.display.flip()
