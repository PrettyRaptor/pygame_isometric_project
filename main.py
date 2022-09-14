import pygame
from pygame.locals import *
import sys
import map

# define things
## sizes??
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

## colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

## others??
VIEW_SET = ["SE", "SW", "NW", "NE"]


def main():
    pygame.init()

    ## SETUP
    framerate = 60
    FPS = pygame.time.Clock()


    logo = pygame.image.load("source/grass_texture_32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("isometryc map drawer test")

    # create a surface on screen that has the size of SCREEN_WIDTH x SCREEN_HEIGHT
    gameScreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    gameScreen.fill(BLACK)

    # initiate map
    game_map = map.Map()
    game_map.load_map_data()
    game_map.load_raw_texture_data()


    # initiate player (?)
    # player = player.Player()




    USER_VIEW_NUMBER = 0
    USER_VIEW_CHOICE = VIEW_SET[USER_VIEW_NUMBER]
    print(f"user view: {USER_VIEW_CHOICE}")
    game_map.set_view(USER_VIEW_CHOICE, gameScreen)

    tiles_near_cursor = []
    under_cursor_tile = {'rect_center': None, 'rect_coord': None}
    selected_tile = {'rect_center': None, 'rect_coord': None}

    mass_selection = []
    is_mass_selection = False

    running = True

    # main loop
    while running:

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_q]:
                    if USER_VIEW_NUMBER < len(VIEW_SET) - 1:
                        USER_VIEW_NUMBER += 1
                    else:
                        USER_VIEW_NUMBER = 0
                if key[pygame.K_e]:
                    if USER_VIEW_NUMBER == 0:
                        USER_VIEW_NUMBER = len(VIEW_SET) - 1
                    else:
                        USER_VIEW_NUMBER -= 1

                USER_VIEW_CHOICE = VIEW_SET[USER_VIEW_NUMBER]
                print(f"user view: {USER_VIEW_CHOICE}")
                game_map.print_all_rects()
                game_map.set_view(USER_VIEW_CHOICE, gameScreen)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                key = pygame.mouse.get_pressed()
                mouse_position = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                print(f"mouse_position: {mouse_position}")
                print(f"lMb: {key[0]} | rMb: {key[2]} | wMb: {key[1]}")
                if key[0]:
                    print("MOUSE LEFT BUTTON CLICKED!")
                    tiles_near_cursor = game_map.get_tiles_near_cursor((mouse_position[0], mouse_position[1]))
                    print(f"tiles_near_cursor contains: {len(tiles_near_cursor)}")
                    selected_tile = game_map.get_tile_under_cursor(mouse_position)
                    print(f"tile_under: {selected_tile}")
                elif key[2]:
                    print("MOUSE RIGHT BUTTON CLICKED!")
                    # game_map.print_centers_cursor((mouse_position[0], mouse_position[1]))
                    # print(game_map.get_centers_cursor((mouse_position[0], mouse_position[1])))
                    selected_tile = game_map.get_tile_under_cursor(mouse_position)
                    print(f"selected_tile: {selected_tile}\n")

            elif event.type == pygame.MOUSEBUTTONUP:
                is_mass_selection = not(is_mass_selection)


            # TODO: сделать выделение сразу множества тайлов.
            # вычисляем selected_tile['rect_coord'] в момент нажатия кнопки мышки = selected_start_tile
            # лови текущее положение курсора и вычисляем tile_under_cursor['rect_coord']
            #
            # Помечаем "выделением" все тайлы, такие что:
            # - tile.coord_x = selected_tile['rect_coord'].x & tile.coord_y IN ( selected_tile['rect_coord'].y; tile_under_cursor['rect_coord'].y - 1 );
            # - tile.coord_x IN ( selected_tile['rect_coord'].x; tile_under_cursor['rect_coord'].x - 1 ) & tile.coord_y = selected_tile['rect_coord'].y;
            # - tile.coord_x = tile_under_cursor['rect_coord'].x & tile.coord_y IN ( selected_tile['rect_coord'].y - 1; tile_under_cursor['rect_coord'].y );
            # - tile.coord_x IN ( selected_tile['rect_coord'].x - 1; tile_under_cursor['rect_coord'].x ) & tile.coord_y = tile_under_cursor['rect_coord'].y;

        gameScreen.fill(BLACK)
        game_map.draw_map_with_angle(USER_VIEW_CHOICE, gameScreen)
        # print(f" selected_tile_relative_coords: {selected_tile['rect_coord']}")
        game_map.draw_selection(selected_tile['rect_coord'], gameScreen)
        # pygame.draw.line(gameScreen, GREEN, selected_tile['rect_coord'], game_map.map_data[selected_tile['rect_coord'][0]][0].get_rect_center())


        pygame.display.update()
        FPS.tick(framerate)

if __name__ == '__main__':
    main()
