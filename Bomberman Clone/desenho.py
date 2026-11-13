import pygame

import config


# DESENHAR UMA CASA DO MAPA
def draw_cell(screen, x, y, color):

    rect = pygame.Rect(
        x * config.TILE_SIZE,
        y * config.TILE_SIZE,
        config.TILE_SIZE,
        config.TILE_SIZE
    )

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, config.BACKGROUND_COLOR, rect, 1)



# DESENHAR AS OPCOES DO MENU
def draw_menu_options(screen, font, title, options, selected):

    title_font = pygame.font.Font(None, 64)

    # Titulo
    title_text = title_font.render(title, True, config.WHITE)

    title_rect = title_text.get_rect(
        center=(config.WIDTH // 2, config.HEIGHT // 2 - 100)
    )

    screen.blit(title_text, title_rect)

    # Opcoes
    for i, option in enumerate(options):

        color = config.PLAYER_COLOR if i == selected else config.WHITE

        text = font.render(str(option), True, color)

        rect = text.get_rect(
            center=(
                config.WIDTH // 2,
                config.HEIGHT // 2 + i * 55
            )
        )

        if i == selected:

            marker = font.render("> ", True, config.PLAYER_COLOR)

            marker_rect = marker.get_rect(
                midright=(rect.left - 8, rect.centery)
            )

            screen.blit(marker, marker_rect)

        screen.blit(text, rect)

# DESENHAR O JOGO
def draw_game(screen, font, game):

    # MENU INICIAL
    if game["game_state"] == "menu":

        screen.fill(config.BACKGROUND_COLOR)

        draw_menu_options(
            screen,
            font,
            "BOMBERMAN",
            ["JOGAR", "SAIR"],
            game["menu_selection"]
        )

        pygame.display.flip()
        return

    screen.fill(config.BACKGROUND_COLOR)

    # MAPA
    for y in range(config.ROWS):

        for x in range(config.COLS):

            draw_cell(screen, x, y, config.EMPTY_TILE_COLOR)

            if game["grid"][y][x] == config.UNBREAKABLE_WALL:
                draw_cell(screen, x, y, config.UNBREAKABLE_WALL_COLOR)

            elif game["grid"][y][x] == config.BREAKABLE_WALL:
                draw_cell(screen, x, y, config.BREAKABLE_WALL_COLOR)

    # BOMBAS
    for bomb in game["bombs"]:

        x, y = bomb["pos"]

        center = (
            x * config.TILE_SIZE + config.TILE_SIZE // 2,
            y * config.TILE_SIZE + config.TILE_SIZE // 2
        )

        pygame.draw.circle(
            screen,
            config.BACKGROUND_COLOR,
            center,
            config.TILE_SIZE // 3
        )

        pygame.draw.circle(
            screen,
            config.WHITE,
            center,
            config.TILE_SIZE // 3,
            2
        )

    # EXPLOSOES
    for explosion in game["explosions"]:

        for x, y in explosion["cells"]:

            rect = pygame.Rect(
                x * config.TILE_SIZE + 4,
                y * config.TILE_SIZE + 4,
                config.TILE_SIZE - 8,
                config.TILE_SIZE - 8
            )

            pygame.draw.rect(screen, config.INNER_EXPLOSION_COLOR, rect)
            pygame.draw.rect(screen, config.OUTER_EXPLOSION_COLOR, rect, 5)

    # JOGADOR
    if game["game_state"] != "lost":

        px = game["player"][0] * config.TILE_SIZE + config.TILE_SIZE // 2
        py = game["player"][1] * config.TILE_SIZE + config.TILE_SIZE // 2

        pygame.draw.circle(
            screen,
            config.PLAYER_COLOR,
            (px, py),
            config.TILE_SIZE // 3
        )

    # INIMIGO
    if game["enemy"]:

        ex = game["enemy"][0] * config.TILE_SIZE + config.TILE_SIZE // 2
        ey = game["enemy"][1] * config.TILE_SIZE + config.TILE_SIZE // 2

        pygame.draw.circle(
            screen,
            config.ENEMY_COLOR,
            (ex, ey),
            config.TILE_SIZE // 3
        )

    # HUD PERMANENTE
    pygame.draw.rect(
        screen,
        config.BACKGROUND_COLOR,
        (0, config.ROWS * config.TILE_SIZE, config.WIDTH, config.HUD)
    )

    msg = "WASD ou SETAS: mover-se | ESPAÇO: colocar bomba"

    text = font.render(msg, True, config.WHITE)

    screen.blit(
        text,
        (10, config.ROWS * config.TILE_SIZE + 14)
    )

    # SOBREPOSICAO DO MENU DE PAUSA
    if game["game_state"] == "paused":

        overlay = pygame.Surface(
            (config.WIDTH, config.HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))

        draw_menu_options(
            screen,
            font,
            "PAUSADO",
            ["CONTINUAR", "MENU PRINCIPAL", "SAIR"],
            game["menu_selection"]
        )

    # TELA DE VITORIA
    elif game["game_state"] == "won":

        screen.fill(config.BACKGROUND_COLOR)

        draw_menu_options(
            screen,
            font,
            "VITORIA!",
            ["JOGAR NOVAMENTE", "MENU PRINCIPAL", "SAIR"],
            game["menu_selection"]
        )

    # TELA DE DERROTA
    elif game["game_state"] == "lost":

        screen.fill(config.BACKGROUND_COLOR)

        draw_menu_options(
            screen,
            font,
            "DERROTA!",
            ["JOGAR NOVAMENTE", "MENU PRINCIPAL", "SAIR"],
            game["menu_selection"]
        )

    pygame.display.flip()
