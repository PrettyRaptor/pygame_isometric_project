import pygame
import tile
from math import sqrt

# задаем размеры тайлов карты
# TODO вынести это в конфиг
tile_size_x = 64
tile_size_y = 64
x_shift = tile_size_x / 2
y_shift = tile_size_y / 4

left_intend = 0
top_intend = 0

class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.map_raw_data = []
        self.textures = {}
        self.map_data = []
        self.map_sprite_group = pygame.sprite.Group()

    # TODO: переделать загрузку карты. По "сырым" данным карты мы генерируем тайлы (единожды)
    def load_map_data(self):
        map_data_source = open("source/map_example", "r")
        coord_y = 0
        for row in map_data_source:
            map_raw_data_row = []
            map_data_row = []
            coord_x = 0
            for cell in row:
                if cell != '\n':
                    map_raw_data_row.append(cell)
                    b_tile = tile.Tile(cell, (coord_x, coord_y))
                    map_data_row.append(b_tile)
                    self.map_sprite_group.add(b_tile)
                    coord_x += 1

                    # print(f'type: {cell}, coords: {b_tile.coord_x, b_tile.coord_y}, abs_coords: {b_tile.get_rect().x, b_tile.get_rect().y}')
            self.map_raw_data.append(map_raw_data_row)
            self.map_data.append(map_data_row)
            coord_y += 1

            # print("end of row")
        map_data_source.close()

    def draw_tile_sprite_group(self, screen):
        self.map_sprite_group.draw(screen)

    def load_raw_texture_data(self):
        none_texture = pygame.surface.Surface((64, 64))
        none_texture.fill((0, 0, 0))
        none_texture.set_alpha(0)

        self.textures[" "] = none_texture
        self.textures["0"] = none_texture
        self.textures["1"] = pygame.image.load("source/grass_texture_64.png").convert_alpha()
        self.textures["2"] = pygame.image.load("source/water_texture_64.png").convert_alpha()
        self.textures["3"] = pygame.image.load("source/pupik_64.png").convert_alpha()
        self.textures["4"] = pygame.image.load("source/tile_selection_64.png").convert_alpha()

    def generate_rect_SE(self):
        ### generate rects for South-East view

        left_intend = x_shift * (len(self.map_data) - 1)
        top_intend = 0
        # print(f"left_intend = {left_intend}; top_intend = {top_intend}")

        # cell.setrect((cell.coord_x - cell.coord_y) * x_shift, (cell.coord_y + cell.coord_x) * y_shift, tile_size_x, tile_size_y)

        for i_index in range(len(self.map_data)):
            for j_index in range(len(self.map_data[i_index])):
                b_rect = (left_intend + (self.map_data[i_index][j_index].coord_x - self.map_data[i_index][j_index].coord_y) * x_shift,
                          top_intend + (self.map_data[i_index][j_index].coord_y + self.map_data[i_index][j_index].coord_x) * y_shift,
                          tile_size_x, tile_size_y)
                # print(f"row_index: {i_index}, col_index: {j_index} | SE rect: x_0 = {b_rect[0]}, y_0 = {b_rect[1]}, x_1 = {b_rect[0] + b_rect[2]}, y_1 = {b_rect[1] + b_rect[3]}")
                self.map_data[i_index][j_index].set_rect(b_rect)

    def generate_rect_SW(self):
        ### generate rects for South-West view

        left_intend = 0
        top_intend = y_shift * (len(self.map_data[0]) - 1)
        # print(f"left_intend = {left_intend}; top_intend = {top_intend}")

        # cell.set_rect((cell.coord_x + cell.coord_y) * x_shift, (cell.coord_y - cell.coord_x) * y_shift, tile_size_x, tile_size_y)

        for i_index in range(len(self.map_data)):
            for j_index in range(len(self.map_data[i_index])):
                b_rect = (left_intend + (self.map_data[i_index][j_index].coord_x + self.map_data[i_index][j_index].coord_y) * x_shift,
                          top_intend + (self.map_data[i_index][j_index].coord_y - self.map_data[i_index][j_index].coord_x) * y_shift,
                          tile_size_x, tile_size_y)
                # print(f"row_index: {i_index}, col_index: {j_index} | SW rect: x_0 = {b_rect[0]}, y_0 = {b_rect[1]}, x_1 = {b_rect[0] + b_rect[2]}, y_1 = {b_rect[1] + b_rect[3]}")
                self.map_data[i_index][j_index].set_rect(b_rect)

    def generate_rect_NW(self):
        ### generate rects for North-East view

        left_intend = x_shift * (len(self.map_data[0]) - 1)
        top_intend = y_shift * ((len(self.map_data) - 1) + (len(self.map_data[0]) - 1))
        # print(f"left_intend = {left_intend}; top_intend = {top_intend}")

        # cell.set_rect(((- tile.coord_x + tile.coord_y) * x_shift, ( - tile.coord_y - tile.coord_x) * y_shift, tile_size_x, tile_size_y)

        for i_index in range(len(self.map_data)):
            for j_index in range(len(self.map_data[i_index])):
                b_rect = (left_intend + (-self.map_data[i_index][j_index].coord_x + self.map_data[i_index][j_index].coord_y) * x_shift,
                          top_intend + (-self.map_data[i_index][j_index].coord_y - self.map_data[i_index][j_index].coord_x) * y_shift,
                          tile_size_x, tile_size_y)
                # print(f"row_index: {i_index}, col_index: {j_index} | SE rect: x_0 = {b_rect[0]}, y_0 = {b_rect[1]}, x_1 = {b_rect[0] + b_rect[2]}, y_1 = {b_rect[1] + b_rect[3]}")
                self.map_data[i_index][j_index].set_rect(b_rect)

    def generate_rect_NE(self):
        ### generate rects for North-West view

        left_intend = x_shift * ((len(self.map_data) - 1) + (len(self.map_data[0]) - 1))
        top_intend = y_shift * (len(self.map_data) - 1)
        # print(f"left_intend = {left_intend}; top_intend = {top_intend}")

        # cell.set_rect(((- tile.coord_x - tile.coord_y) * x_shift, (- tile.coord_y + tile.coord_x) * y_shift, tile_size_x, tile_size_y)

        for i_index in range(len(self.map_data)):
            for j_index in range(len(self.map_data[i_index])):
                b_rect = (left_intend + (-self.map_data[i_index][j_index].coord_x - self.map_data[i_index][j_index].coord_y) * x_shift,
                          top_intend + (-self.map_data[i_index][j_index].coord_y + self.map_data[i_index][j_index].coord_x) * y_shift,
                          tile_size_x, tile_size_y)
                # print(f"row_index: {i_index}, col_index: {j_index} | SE rect: x_0 = {b_rect[0]}, y_0 = {b_rect[1]}, x_1 = {b_rect[0] + b_rect[2]}, y_1 = {b_rect[1] + b_rect[3]}")
                self.map_data[i_index][j_index].set_rect(b_rect)

    def draw_map_SE(self, screen):
        for i_index in range(len(self.map_data)):
            for j_index in range(len(self.map_data[i_index])):
                # print(f"coords (x, y): {i_index}, {j_index} ")
                b_tile = self.map_data[i_index][j_index]
                if b_tile is not None:
                    screen.blit(self.textures.get(str(b_tile.type)), b_tile.get_rect())

    def draw_map_SW(self, screen):
        for i_index in range(len(self.map_data)):
            for j_index in range(len(self.map_data[i_index]) - 1, -1, -1):
                # print(f"coords (x, y): {i_index}, {j_index} ")
                b_tile = self.map_data[i_index][j_index]
                if b_tile is not None:
                    screen.blit(self.textures.get(str(b_tile.type)), b_tile.get_rect())

    def draw_map_NW(self, screen):
        for i_index in range(len(self.map_data) - 1, -1, -1):
            for j_index in range(len(self.map_data[i_index]) - 1, -1, -1):
                # print(f"coords (x, y): {i_index}, {j_index} ")
                b_tile = self.map_data[i_index][j_index]
                if b_tile is not None:
                    screen.blit(self.textures.get(str(b_tile.type)), b_tile.get_rect())

    def draw_map_NE(self, screen):
        for i_index in range(len(self.map_data) - 1, -1, -1):
            for j_index in range(len(self.map_data[i_index])):
                b_tile = self.map_data[i_index][j_index]
                if b_tile is not None:
                    screen.blit(self.textures.get(str(b_tile.type)), b_tile.get_rect())

    def set_view(self, view_angle, screen):
        if view_angle == "SE":
            self.generate_rect_SE()
            self.draw_map_SE(screen)
        elif view_angle == "SW":
            self.generate_rect_SW()
            self.draw_map_SW(screen)
        elif view_angle == "NW":
            self.generate_rect_NW()
            self.draw_map_NW(screen)
        elif view_angle == "NE":
            self.generate_rect_NE()
            self.draw_map_NE(screen)

    def draw_map_with_angle(self, view_angle, screen):
        if view_angle == "SE":
            self.draw_map_SE(screen)
        elif view_angle == "SW":
            self.draw_map_SW(screen)
        elif view_angle == "NW":
            self.draw_map_NW(screen)
        elif view_angle == "NE":
            self.draw_map_NE(screen)

    def draw_selection(self, coords, screen):
        if coords is not None:
            screen.blit(self.textures.get("4"), self.map_data[coords[1]][coords[0]].get_rect())

    def print_centers_cursor(self, mouse_position):
        ### печатаем позицию курсора и позиции центров тайла

        for row in self.map_data:
            for cell in row:
                sel_tile_coords = cell.is_mouse_over()
                if cell.is_mouse_over():
                    print("+-===========-+")
                    print(f"mouse_position: ({mouse_position[0]};{mouse_position[1]})")
                    print(f"near_tile: ({sel_tile_coords['rect_coord'][0]};{sel_tile_coords['rect_coord'][1]})")

    def get_tiles_near_cursor(self, mouse_position):
        ### получаем ближайщие к курсору тайлы

        # mouse_position = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        nearest_tiles = []
        for row in self.map_data:
            for cell in row:
                sel_tile_coords = cell.is_mouse_over(mouse_position)
                if sel_tile_coords:
                    nearest_tiles.append(sel_tile_coords)

        return nearest_tiles

    def get_tile_under_cursor(self, mouse_position):
        ### вычисляем выделяемый тайл

        nearest_tiles = []
        for row in self.map_data:
            for cell in row:
                sel_tile_coords = cell.is_mouse_over(mouse_position)
                # print(f"selected tile coordinate: {sel_tile_coords}")
                if sel_tile_coords:
                    nearest_tiles.append(sel_tile_coords)

        if len(nearest_tiles) > 0:
            tile_under_cursor = nearest_tiles[0]
            minimal_length = sqrt(((mouse_position[0] - tile_under_cursor['rect_center'][0]) ** 2) + ((mouse_position[1] - tile_under_cursor['rect_center'][1]) ** 2))
            # print(f"default minimal length: {minimal_length}")

            for near_tile in nearest_tiles:
                b_length = sqrt(((mouse_position[0] - near_tile['rect_center'][0]) ** 2) + ((mouse_position[1] - near_tile['rect_center'][1]) ** 2))
                # print(f"near_tile: {near_tile}| length: {b_length}")
                if b_length <= minimal_length:
                    minimal_length = b_length
                    tile_under_cursor = near_tile

        return tile_under_cursor

    def print_all_rects(self):
        for row in self.map_data:
            for cell in row:
                cell.print_rect_center()
            print("\n")

    def raw_print(self):
        for row in self.map_data:
            for cell in row:
                print(cell.type, end="_")
            print()
