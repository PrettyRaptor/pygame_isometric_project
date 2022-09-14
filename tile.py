import pygame

tile_size = 64

class Tile(pygame.sprite.Sprite):
    def __init__(self, type, coords):
        super().__init__()
        self.type = type
        self.state = {"selected": False} # массив для хранения "состояния" тайла. На будущее
        self.coord_x = coords[0]
        self.coord_y = coords[1]
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect_center = self.rect.center

        self.selection_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        self.selection_rect_center = self.selection_rect.center
        # self.rect_center = (self.rect[0] + self.rect[2] / 2, self.rect[1] + self.rect[3] / 2)

    # def update(self, type=self.type, coords=(self.coord_x, self.coord_y), rect=self.rect, rect_center=self.rect_center):
    #     return None

    def get_type(self):
        return self.type

    def get_rect(self):
        return self.rect

    def get_rect_center(self):
        return self.rect_center

    def set_rect(self, new_rect):
        self.rect.update(new_rect)
        self.rect_center = self.rect.center
        self.selection_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        self.selection_rect_center = self.selection_rect.center

    def print_rect(self):
        # print(self.rect, end=" | ")
        print(f"x_0 = {self.rect[0]}, y_0 = {self.rect[1]}, x_1 = {self.rect[0] + self.rect[2]}, y_1 = {self.rect[1] + self.rect[3]}", end=" | ")

    def print_rect_center(self):
        # print(f"X_c: {self.rect[0] + self.rect[2] / 2}, Y_c: {self.rect[1] + self.rect[3] / 2}", end="|")
        print(f"X_c: {self.rect.center[0]}, Y_c: {self.rect.center[1]}", end="|")

    def is_mouse_over(self, mouse_position):
        ### возвращает курсор попал в прямоугольник тайл -> возвращает координаты центра этого тайла и относительные координаты тайла

        if self.selection_rect.collidepoint(mouse_position[0], mouse_position[1]):
            rect_center = (self.selection_rect_center[0], self.selection_rect_center[1] - self.rect.height / 4)
            rect_coord = (self.coord_x, self.coord_y)
            return {"rect_center": rect_center, "rect_coord": rect_coord}

