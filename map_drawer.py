import pygame

tile = pygame.image.load("source/grass_texture_64.png")	# TODO сделать отдельную загрузку текстур и прочего
tile_rect = tile.get_rect()
grid_cell = pygame.image.load("source/color_grid_64.png")

step_x = tile.get_width() / 2
step_y = tile.get_height() / 4

left_indent = 20  # отступ от левого края
top_indent = 20  # отступ от верхнего края

def draw(screen, map):
	rect_width = (screen.get_width() - 2 * left_indent) / len(map)
	rect_height = (screen.get_height() - 2 * top_indent) / len(map[0])

	# left_isometric_shift = len(map) * (step_x / 2)
	# print(left_isometric_shift)

	y = 0
	for row in map:
		x = 0
		for cell in row:
			if cell:
				tile_rect = (left_indent + (x - y) * (step_x), top_indent + (y + x) * (step_y), 32, 32)
				screen.blit(tile, tile_rect)

				# grid_cell_rect = tile_rect
				# screen.blit(grid_cell, grid_cell_rect)
			x = x + 1
		y = y + 1




def coord_convert_to_iso(coords):
	#
	return_x = int(((coords[0] - left_indent) / (step_x) + (coords[1] - top_indent) / (step_y / 2)))
	return_y = int((coords[1] - top_indent) / (step_y / 2) - ((coords[0] - left_indent)) / (step_x))

	return (return_x, return_y)

