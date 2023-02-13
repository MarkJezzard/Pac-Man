import pygame
import sys
from pygame.locals import *
import os  # to help with finding file path of images
import time
import random
import math
from copy import deepcopy
from pathfinding import *

pygame.init()

# creating  window
WIDTH, HEIGHT = 224, 294
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), SCALED | RESIZABLE)
pygame.display.set_caption("Pac-Man")
pygame.display.set_icon(pygame.image.load(os.path.join('pacman_images', 'icon.png')))

# frame rate
FPS = 60

# images
MAZE_IMAGE = pygame.image.load(os.path.join('pacman_images', 'maze.png'))
ENERGISER_IMAGE = pygame.image.load(os.path.join('pacman_images', 'energiser.png'))
CHERRY_IMAGE = pygame.image.load(os.path.join('pacman_images', 'cherry.png'))
LIFE_INDICATOR_IMAGE = pygame.image.load(os.path.join('pacman_images', 'life_indicator.png'))
PACMAN_MOUTH_SHUT_IMAGE = pygame.image.load(os.path.join('pacman_images', 'pacman_left_1.png'))

# colours
WHITE = (255, 255, 255)
DOT_COLOUR = (250, 185, 176)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (253, 181, 255)
BLUE = (0, 255, 255)
ORANGE = (255, 184, 71)

# font
FONT = pygame.font.Font("pacman_font.ttf", 8)

# maze representation as tiles
tiles = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 3, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 3, 1],
    [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class Pacman:

    def __init__(self, x, y, maze_tiles):
        self.x = x
        self.y = y
        self.tiles = maze_tiles
        self.direction = 'left'
        self.change_direction = None  # to hold change direction request
        self.image = pygame.image.load(os.path.join('pacman_images', 'pacman_left_1.png'))
        self.image_previous = 1  # for switching between images
        self.image_counter = 0  # for when to switch between images
        self.image_number = 1  # for switching between images
        self.lives_left = 2

    def get_row(self):
        return self.y // 8

    def get_column(self):
        return self.x // 8

    def get_current_tile(self):
        return self.tiles[self.y // 8][self.x // 8]

    def get_next_tile(self, direction):
        if direction == 'left':
            return self.tiles[self.get_row()][self.get_column() - 1]
        elif direction == 'right':
            return self.tiles[self.get_row()][self.get_column() + 1]
        elif direction == 'up':
            return self.tiles[self.get_row() - 1][self.get_column()]
        elif direction == 'down':
            return self.tiles[self.get_row() + 1][self.get_column()]

    def move(self):
        # which mouth
        if self.image_counter % 4 == 0:

            # if mouth closed -> mouth now half open
            if self.image_number == 1:
                self.image_number = 2
                self.image_previous = 1

            # if mouth half open -> either closed or fully open
            # depending on previous
            elif self.image_number == 2:
                if self.image_previous == 1:
                    self.image_number = 3
                elif self.image_previous == 3:
                    self.image_number = 1

            # if mouth fully open -> mouth now half open
            elif self.image_number == 3:
                self.image_number = 2
                self.image_previous = 3

        # tunnel
        if self.get_column() == 0 or self.get_column() == 27:
            if self.change_direction == 'left':
                if self.x != 0:
                    self.direction = 'left'
                    self.x -= 1
                else:
                    self.x = 28 * 8 - 1
                    self.direction = 'left'
            elif self.change_direction == 'right':
                if self.x != 28 * 8 - 1:
                    self.direction = 'right'
                    self.x += 1
                else:
                    self.x = 0
                    self.direction = 'right'
            else:
                if self.direction == 'left':
                    if self.x == 0:
                        self.x = 28 * 8 - 1
                    self.x -= 1
                elif self.direction == 'right':
                    if self.x == 28 * 8 - 1:
                        self.x = 0
                    self.x += 1

        else:
            # horizontal to vertical movement (and horizontal to horizontal)
            if self.direction == 'left' or self.direction == 'right':
                if self.change_direction == 'up' and self.get_next_tile('up') != 1 and self.x % 8 == 3:
                    self.direction = 'up'
                elif self.change_direction == 'down' and self.get_next_tile('down') != 1 and self.x % 8 == 3:
                    self.direction = 'down'
                elif self.change_direction == 'left' or self.change_direction == 'right':
                    self.direction = self.change_direction

            # vertical to horizontal movement (and vertical to vertical)
            elif self.direction == 'up' or self.direction == 'down':
                if self.change_direction == 'left' and self.get_next_tile('left') != 1 and self.y % 8 == 3:
                    self.direction = 'left'
                elif self.change_direction == 'right' and self.get_next_tile('right') != 1 and self.y % 8 == 3:
                    self.direction = 'right'
                elif self.change_direction == 'up' or self.change_direction == 'down':
                    self.direction = self.change_direction

            # move Pac-Man and change image
            next_tile = self.get_next_tile(self.direction)
            if self.direction == 'left':
                if not (next_tile == 1 and self.x % 8 == 3):
                    self.x -= 1
                    self.image = pygame.image.load(os.path.join('pacman_images',
                                                                'pacman_left_'+str(self.image_number)+'.png'))
                    self.image_counter += 1

            elif self.direction == 'right':
                if not (next_tile == 1 and self.x % 8 == 3):
                    self.x += 1
                    self.image = pygame.image.load(os.path.join('pacman_images',
                                                                'pacman_right_' + str(self.image_number) + '.png'))
                    self.image_counter += 1

            elif self.direction == 'up':
                if not (next_tile == 1 and self.y % 8 == 3):
                    self.y -= 1
                    self.image = pygame.image.load(os.path.join('pacman_images',
                                                                'pacman_up_' + str(self.image_number) + '.png'))
                    self.image_counter += 1

            elif self.direction == 'down':
                if not (next_tile == 1 and self.y % 8 == 3):
                    self.y += 1
                    self.image = pygame.image.load(os.path.join('pacman_images',
                                                                'pacman_down_' + str(self.image_number) + '.png'))
                    self.image_counter += 1

    def reset(self):
        self.x = 111  # resets Pac-Man to starting position
        self.y = 211
        self.direction = 'left'
        self.change_direction = None
        self.image = pygame.image.load(os.path.join('pacman_images', 'pacman_left_1.png'))


class Ghost:
    def __init__(self, maze_tiles):
        self.tiles = maze_tiles
        self.x = 111
        self.y = 14 * 8 + 3
        self.path = []
        self.direction = 'left'
        self.colour = 'red'
        self.mode = 'SCATTER'
        self.target_tile_row = None
        self.target_tile_column = None
        self.go_to_tunnel = False
        self.count = 0

        self.image = pygame.image.load(os.path.join('pacman_images', 'red_ghost_left_1.png'))
        self.image_counter = 0
        self.image_number = 1

        self.flash_while_frightened = False
        self.is_white = False
        self.flash_number = 0

        self.enter_maze = False

    def get_row(self):
        return self.y // 8

    def get_column(self):
        return self.x // 8

    def get_current_tile(self):
        return self.tiles[self.y // 8][self.x // 8]

    def get_next_tile(self, direction):
        if direction == 'left':
            return self.tiles[self.get_row()][self.get_column() - 1]
        elif direction == 'right':
            return self.tiles[self.get_row()][self.get_column() + 1]
        elif direction == 'up':
            return self.tiles[self.get_row() - 1][self.get_column()]
        elif direction == 'down':
            return self.tiles[self.get_row() + 1][self.get_column()]

    def get_reverse_direction(self):
        direction = self.direction
        if direction == 'up':
            return 'down'
        elif direction == 'down':
            return 'up'
        elif direction == 'left':
            return 'right'
        elif direction == 'right':
            return 'left'

    def get_possible_directions(self):
        # don't want to turn into wall or reverse direction or continue in current direction
        possible_directions = []
        if self.get_next_tile('up') != 1 and self.direction != 'down' and self.direction != 'up':
            possible_directions.append('up')
        if self.get_next_tile('left') != 1 and self.direction != 'right' and self.direction != 'left':
            possible_directions.append('left')
        if self.get_next_tile('down') != 1 and self.direction != 'up' and self.direction != 'down':
            possible_directions.append('down')
        if self.get_next_tile('right') != 1 and self.direction != 'left' and self.direction != 'right':
            possible_directions.append('right')
        return possible_directions

    def at_tile_center(self):
        if self.direction == 'up' or self.direction == 'down':
            if self.y % 8 == 3:
                return True
        if self.direction == 'left' or self.direction == 'right':
            if self.x % 8 == 3:
                return True
        return False

    def calculate_target_tile(self, pacman_row, pacman_column):
        self.target_tile_row = pacman_row
        self.target_tile_column = pacman_column

    def calculate_path(self, target_tile_row, target_tile_column):
        grid_of_nodes = deepcopy(tiles_nodes)
        self.path = a_star((self.get_row(), self.get_column()), (target_tile_row, target_tile_column), grid_of_nodes)

        if self.path == 'NO PATH':
            # left tunnel
            if target_tile_column < 6:
                self.path = a_star((self.get_row(), self.get_column()), (17, 6), grid_of_nodes)
                self.go_to_tunnel = True
            # right tunnel
            elif target_tile_column > 21:
                self.path = a_star((self.get_row(), self.get_column()), (17, 21), grid_of_nodes)
                self.go_to_tunnel = True

    def draw_target_tile(self):
        if self.mode == 'CHASE':
            x = self.target_tile_column * 8
            y = self.target_tile_row * 8
            if self.colour == 'red':
                pygame.draw.rect(WINDOW, RED, (x, y, 8, 8), 1)
            elif self.colour == 'pink':
                pygame.draw.rect(WINDOW, PINK, (x, y, 8, 8), 1)
            elif self.colour == 'blue':
                pygame.draw.rect(WINDOW, BLUE, (x, y, 8, 8), 1)
            else:
                pygame.draw.rect(WINDOW, ORANGE, (x, y, 8, 8), 1)
        # draws rectangle around target tile

    def chase_or_scatter(self, timer, level):
        previous_mode = self.mode

        # levels 1-4
        if 1 <= level <= 4:
            if timer < 7:
                self.mode = 'SCATTER'
            elif 7 < timer < 27:
                self.mode = 'CHASE'
            elif 27 < timer < 34:
                self.mode = 'SCATTER'
            elif 34 < timer < 54:
                self.mode = 'CHASE'
            elif 54 < timer < 59:
                self.mode = 'SCATTER'
            else:
                if level == 1:
                    if 59 < timer < 79:
                        self.mode = 'CHASE'
                    elif 79 < timer < 84:
                        self.mode = 'SCATTER'
                    else:
                        self.mode = 'CHASE'
                else:
                    self.mode = 'CHASE'

        # levels 5+
        else:
            if timer < 5:
                self.mode = 'SCATTER'
            elif 5 < timer < 25:
                self.mode = 'CHASE'
            elif 25 < timer < 30:
                self.mode = 'SCATTER'
            elif 30 < timer < 50:
                self.mode = 'CHASE'
            elif 50 < timer < 55:
                self.mode = 'SCATTER'
            else:
                self.mode = 'CHASE'

        # if new mode is chase and the mode was just scatter
        if self.mode == 'CHASE' and previous_mode == 'SCATTER':
            self.direction = self.get_reverse_direction()
        # if new mode is scatter and the mode was just chase
        elif self.mode == 'SCATTER' and previous_mode == 'CHASE':
            self.direction = self.get_reverse_direction()

    def move(self):
        # switch image to produce leg animation
        self.image_counter += 1
        if self.image_counter % 8 == 0:
            if self.image_number == 1:
                self.image_number = 2
            elif self.image_number == 2:
                self.image_number = 1

        # if leaving ghost house
        if self.enter_maze:
            # if now in maze
            if self.x == 13.5 * 8 + 3 and self.y == 14 * 8 + 3:
                self.enter_maze = False
                self.direction = 'left'
            # otherwise move up
            else:
                self.direction = 'up'

        # if at end of tunnels, teleport
        elif self.x == 0:
            self.x = 28 * 8 - 1
        elif self.x == 28 * 8 - 1:
            self.x = 0

        # go into ghost house if eaten and at entrance
        elif self.x == 13.5 * 8 + 3 and self.y == 14 * 8 + 3 and self.mode == 'EATEN':
            self.direction = 'down'

        # turn back to chase mode if reached ghost house centre
        elif self.x == 13.5 * 8 + 3 and self.y == 17 * 8 + 3:
            self.enter_maze = True
            self.mode = 'CHASE'
            self.direction = None

        # if at node
        elif tiles_nodes[self.get_row()][self.get_column()] == 8 and self.at_tile_center():
            if self.mode == 'SCATTER':
                # red ghost circles around top right corner
                self.calculate_path(8, 21)

                if self.get_row() == 8 and self.get_column() == 21:
                    self.calculate_path(4, 21)
                elif self.get_row() == 4 and self.get_column() == 21:
                    self.calculate_path(4, 26)
                elif self.get_row() == 4 and self.get_column() == 26:
                    self.calculate_path(8, 26)
                elif self.get_row() == 8 and self.get_column() == 26:
                    self.calculate_path(8, 21)

                # set direction according to calculated path
                if (self.path[-2][0] - self.path[-1][0]) < 0 and 'up' != self.get_reverse_direction():
                    self.direction = 'up'
                elif (self.path[-2][0] - self.path[-1][0]) > 0 and 'down' != self.get_reverse_direction():
                    self.direction = 'down'
                elif (self.path[-2][1] - self.path[-1][1]) > 0 and 'right' != self.get_reverse_direction():
                    self.direction = 'right'
                elif (self.path[-2][1] - self.path[-1][1]) < 0 and 'left' != self.get_reverse_direction():
                    self.direction = 'left'
                else:
                    directions = self.get_possible_directions()
                    if directions:
                        self.direction = directions[0]

            elif self.mode == 'CHASE':
                # at left tunnel entrance
                if self.go_to_tunnel and self.get_row() == 17 and self.get_column() == 6:
                    self.go_to_tunnel = False
                    self.direction = 'left'

                # at right tunnel entrance
                elif self.go_to_tunnel and self.get_row() == 17 and self.get_column() == 21:
                    self.go_to_tunnel = False
                    self.direction = 'right'

                else:
                    # chase target tile
                    self.calculate_path(self.target_tile_row, self.target_tile_column)

                    if len(self.path) == 1:
                        if self.go_to_tunnel and self.get_column() == 6:
                            self.go_to_tunnel = False
                            self.direction = 'left'
                        elif self.go_to_tunnel and self.get_column() == 21:
                            self.go_to_tunnel = False
                            self.direction = 'right'
                        else:
                            self.direction = self.get_possible_directions()[0]

                    elif (self.path[-2][0] - self.path[-1][0]) < 0 and 'up' != self.get_reverse_direction():
                        self.direction = 'up'
                    elif (self.path[-2][0] - self.path[-1][0]) > 0 and 'down' != self.get_reverse_direction():
                        self.direction = 'down'
                    elif (self.path[-2][1] - self.path[-1][1]) > 0 and 'right' != self.get_reverse_direction():
                        self.direction = 'right'
                    elif (self.path[-2][1] - self.path[-1][1]) < 0 and 'left' != self.get_reverse_direction():
                        self.direction = 'left'
                    else:
                        directions = self.get_possible_directions()
                        if directions:
                            self.direction = directions[0]

            # move randomly in frightened mode
            elif self.mode == 'FRIGHTENED':
                possible_directions = self.get_possible_directions()
                if self.get_next_tile(self.direction) != 1:
                    possible_directions.append(self.direction)
                index = random.randint(0, len(possible_directions)-1)
                self.direction = possible_directions[index]

            elif self.mode == 'EATEN':
                # calculates path to ghost house entrance (eyes travel back to ghost house)
                self.calculate_path(14, 13)

                if len(self.path) == 1:
                    print('at ghost house')
                elif (self.path[-2][0] - self.path[-1][0]) < 0 and 'up' != self.get_reverse_direction():
                    self.direction = 'up'
                elif (self.path[-2][0] - self.path[-1][0]) > 0 and 'down' != self.get_reverse_direction():
                    self.direction = 'down'
                elif (self.path[-2][1] - self.path[-1][1]) > 0 and 'right' != self.get_reverse_direction():
                    self.direction = 'right'
                elif (self.path[-2][1] - self.path[-1][1]) < 0 and 'left' != self.get_reverse_direction():
                    self.direction = 'left'
                else:
                    directions = self.get_possible_directions()
                    if directions:
                        self.direction = directions[0]

        # set image
        if self.mode == 'SCATTER' or self.mode == 'CHASE':
            if self.direction:
                self.image = pygame.image.load(os.path.join(
                    'pacman_images', str(self.colour)+'_ghost_'+str(self.direction)+'_'+str(self.image_number)+'.png'))
        elif self.mode == 'FRIGHTENED':
            if not self.flash_while_frightened:
                self.image = pygame.image.load(os.path.join(
                    'pacman_images', 'frightened_ghost_'+str(self.image_number)+'.png'))
            else:
                if self.image_counter % 6 == 0:
                    if self.is_white:
                        self.is_white = False
                        self.flash_number += 1
                        self.image = pygame.image.load(os.path.join(
                            'pacman_images', 'frightened_ghost_'+str(self.image_number)+'.png'))
                    else:
                        self.is_white = True
                        self.image = pygame.image.load(os.path.join(
                            'pacman_images', 'frightened_ghost_flash_'+str(self.image_number)+'.png'))
        elif self.mode == 'EATEN':
            if self.direction:
                self.image = pygame.image.load(os.path.join(
                    'pacman_images', 'eaten_eyes_'+str(self.direction)+'.png'))

        # move according to direction
        if self.direction == 'left':
            self.x -= 1
        elif self.direction == 'right':
            self.x += 1
        elif self.direction == 'up':
            self.y -= 1
        elif self.direction == 'down':
            self.y += 1

    def reset(self):
        self.mode = 'SCATTER'
        self.x = 111
        self.y = 14 * 8 + 3
        self.direction = 'left'
        self.image = pygame.image.load(os.path.join('pacman_images', 'red_ghost_left_1.png'))
        self.flash_while_frightened = False
        self.is_white = False
        self.flash_number = 0
        self.enter_maze = False


class OrangeGhost(Ghost):
    def __init__(self, maze_tiles):
        super().__init__(maze_tiles)
        # attributes that need to be changed from the normal ghost class
        self.x = 127
        self.y = 139
        self.direction = 'up'
        self.colour = 'orange'
        self.image = pygame.image.load(os.path.join('pacman_images', 'orange_ghost_up_1.png'))
        # new attributes
        self.idle = True

    def calculate_target_tile(self, pacman_row, pacman_column):
        distance_to_pacman = math.sqrt(
            ((self.get_row() - pacman_row) ** 2) + ((self.get_column() - pacman_column) ** 2)
        )

        if distance_to_pacman < 8:
            # target tile set to bottom left corner of maze
            self.target_tile_row = 32
            self.target_tile_column = 1
        else:
            # target tile is pacman
            self.target_tile_row = pacman_row
            self.target_tile_column = pacman_column

    def move(self):
        # choosing correct legs
        self.image_counter += 1
        if self.image_counter % 8 == 0:
            if self.image_number == 1:
                self.image_number = 2
            elif self.image_number == 2:
                self.image_number = 1

        # if idle
        if self.idle:
            if self.x == 127:
                # if at side of ghost house move down or up when get too high or low
                if self.y == 143:
                    # move up when at bottom of ghost house
                    self.direction = 'up'
                elif self.y == 135:
                    # move down when at top of ghost house
                    self.direction = 'down'
                # if have been told to enter maze and centred vertically in ghost house
                elif self.y == 139 and self.enter_maze:
                    self.direction = 'left'
            # if below entrance, exit idle. This will take ghost to enter_maze handling
            elif self.x == 111:
                self.idle = False
                self.direction = 'up'

        elif self.enter_maze:
            # if now in maze
            if self.x == 13.5 * 8 + 3 and self.y == 14 * 8 + 3:
                self.enter_maze = False
                self.direction = 'left'
            # otherwise move up
            else:
                self.direction = 'up'

        # if at end of tunnels, teleport
        elif self.x == 0:
            self.x = 28 * 8 - 1
        elif self.x == 28 * 8 - 1:
            self.x = 0

        elif self.x == 13.5 * 8 + 3 and self.y == 14 * 8 + 3 and self.mode == 'EATEN':
            self.direction = 'down'

        elif self.x == 13.5 * 8 + 3 and self.y == 17 * 8 + 3:
            self.enter_maze = True
            self.mode = 'CHASE'
            self.direction = None

        # if at node
        elif tiles_nodes[self.get_row()][self.get_column()] == 8 and self.at_tile_center():
            if self.mode == 'SCATTER':
                # orange ghost circles round bottom left corner of maze
                if self.get_row() == 26 and self.get_column() == 6:
                    self.calculate_path(29, 3)
                elif self.get_row() == 29 and self.get_column() == 3:
                    self.calculate_path(29, 1)
                elif self.get_row() == 29 and self.get_column() == 1:
                    self.calculate_path(32, 1)
                elif self.get_row == 32 and self.get_column() == 1:
                    self.calculate_path(32, 12)
                elif self.get_row == 32 and self.get_column() == 12:
                    self.calculate_path(29, 12)
                elif self.get_row() == 29 and self.get_column() == 12:
                    self.calculate_path(29, 9)
                elif self.get_row() == 29 and self.get_column() == 9:
                    self.calculate_path(26, 9)
                else:
                    self.calculate_path(26, 6)

                if (self.path[-2][0] - self.path[-1][0]) < 0 and 'up' != self.get_reverse_direction():
                    self.direction = 'up'
                elif (self.path[-2][0] - self.path[-1][0]) > 0 and 'down' != self.get_reverse_direction():
                    self.direction = 'down'
                elif (self.path[-2][1] - self.path[-1][1]) > 0 and 'right' != self.get_reverse_direction():
                    self.direction = 'right'
                elif (self.path[-2][1] - self.path[-1][1]) < 0 and 'left' != self.get_reverse_direction():
                    self.direction = 'left'
                else:
                    directions = self.get_possible_directions()
                    if directions:
                        self.direction = directions[0]

            elif self.mode == 'CHASE':
                # at left tunnel entrance
                if self.go_to_tunnel and self.get_row() == 17 and self.get_column() == 6:
                    self.go_to_tunnel = False
                    self.direction = 'left'

                # at right tunnel entrance
                elif self.go_to_tunnel and self.get_row() == 17 and self.get_column() == 21:
                    self.go_to_tunnel = False
                    self.direction = 'right'

                else:
                    self.calculate_path(self.target_tile_row, self.target_tile_column)

                    if len(self.path) == 1:
                        if self.go_to_tunnel and self.get_column() == 6:
                            self.go_to_tunnel = False
                            self.direction = 'left'
                        elif self.go_to_tunnel and self.get_column() == 21:
                            self.go_to_tunnel = False
                            self.direction = 'right'
                        else:
                            self.direction = self.get_possible_directions()[0]

                    elif (self.path[-2][0] - self.path[-1][0]) < 0 and 'up' != self.get_reverse_direction():
                        self.direction = 'up'
                    elif (self.path[-2][0] - self.path[-1][0]) > 0 and 'down' != self.get_reverse_direction():
                        self.direction = 'down'
                    elif (self.path[-2][1] - self.path[-1][1]) > 0 and 'right' != self.get_reverse_direction():
                        self.direction = 'right'
                    elif (self.path[-2][1] - self.path[-1][1]) < 0 and 'left' != self.get_reverse_direction():
                        self.direction = 'left'
                    else:
                        directions = self.get_possible_directions()
                        if directions:
                            self.direction = directions[0]

            elif self.mode == 'FRIGHTENED':
                possible_directions = self.get_possible_directions()
                if self.get_next_tile(self.direction) != 1:
                    possible_directions.append(self.direction)
                index = random.randint(0, len(possible_directions) - 1)
                self.direction = possible_directions[index]

            elif self.mode == 'EATEN':
                # calculates path to ghost house entrance/exit
                self.calculate_path(14, 13)

                if len(self.path) == 1:
                    print('at ghost house')
                elif (self.path[-2][0] - self.path[-1][0]) < 0 and 'up' != self.get_reverse_direction():
                    self.direction = 'up'
                elif (self.path[-2][0] - self.path[-1][0]) > 0 and 'down' != self.get_reverse_direction():
                    self.direction = 'down'
                elif (self.path[-2][1] - self.path[-1][1]) > 0 and 'right' != self.get_reverse_direction():
                    self.direction = 'right'
                elif (self.path[-2][1] - self.path[-1][1]) < 0 and 'left' != self.get_reverse_direction():
                    self.direction = 'left'
                else:
                    directions = self.get_possible_directions()
                    if directions:
                        self.direction = directions[0]

        # set image
        if self.mode == 'SCATTER' or self.mode == 'CHASE':
            if self.direction:
                self.image = pygame.image.load(os.path.join(
                    'pacman_images',
                    str(self.colour) + '_ghost_' + str(self.direction) + '_' + str(self.image_number) + '.png'))
        elif self.mode == 'FRIGHTENED':
            if not self.flash_while_frightened:
                self.image = pygame.image.load(os.path.join(
                    'pacman_images', 'frightened_ghost_' + str(self.image_number) + '.png'))
            else:
                if self.image_counter % 6 == 0:
                    if self.is_white:
                        self.is_white = False
                        self.flash_number += 1
                        self.image = pygame.image.load(os.path.join(
                            'pacman_images', 'frightened_ghost_' + str(self.image_number) + '.png'))
                    else:
                        self.is_white = True
                        self.image = pygame.image.load(os.path.join(
                            'pacman_images', 'frightened_ghost_flash_' + str(self.image_number) + '.png'))
        elif self.mode == 'EATEN':
            if self.direction:
                self.image = pygame.image.load(os.path.join(
                    'pacman_images', 'eaten_eyes_' + str(self.direction) + '.png'))

        if self.direction == 'left':
            self.x -= 1
        elif self.direction == 'right':
            self.x += 1
        elif self.direction == 'up':
            self.y -= 1
        elif self.direction == 'down':
            self.y += 1

    def reset(self):
        self.mode = 'SCATTER'
        self.x = 127
        self.y = 139
        self.direction = 'up'
        self.image = pygame.image.load(os.path.join('pacman_images', 'orange_ghost_up_1.png'))
        self.flash_while_frightened = False
        self.is_white = False
        self.flash_number = 0
        self.enter_maze = False
        self.idle = True


class PinkGhost(Ghost):
    def __init__(self, maze_tiles):
        super().__init__(maze_tiles)
        # attributes that need to be changed from the normal ghost class
        self.x = 111
        self.y = 17 * 8 + 3
        self.direction = 'down'
        self.colour = 'pink'
        self.image = pygame.image.load(os.path.join('pacman_images', 'pink_ghost_down_1.png'))

        # new attributes
        self.idle = True

    def calculate_target_tile_pink(self, pacman_row, pacman_column, pacman_direction):
        # pink ghost targets 4 tiles ahead of Pac-Man

        if pacman_direction == 'left':
            self.target_tile_row = pacman_row
            i = 4
            target_tile_found = False
            # iterate through tiles to the left of Pac-Man starting from 4 tiles ahead and decreasing...
            # ...until find valid target tile
            while i > 0 and not target_tile_found:
                # check index isn't out of range and isn't a wall
                if pacman_column - i > 0 and self.tiles[pacman_row][pacman_column - i] != 1:
                    self.target_tile_column = pacman_column - i
                    target_tile_found = True
                i -= 1
            if not target_tile_found:
                self.target_tile_column = pacman_column

        elif pacman_direction == 'right':
            self.target_tile_row = pacman_row
            i = 4
            target_tile_found = False
            while i > 0 and not target_tile_found:
                if pacman_column + i < 27 and self.tiles[pacman_row][pacman_column + i] != 1:
                    self.target_tile_column = pacman_column + i
                    target_tile_found = True
                i -= 1
            if not target_tile_found:
                self.target_tile_column = pacman_column

        elif pacman_direction == 'up':
            self.target_tile_column = pacman_column
            i = 4
            target_tile_found = False
            while i > 0 and not target_tile_found:
                if pacman_row - i > 0 and self.tiles[pacman_row - i][pacman_column] != 1:
                    self.target_tile_row = pacman_row - i
                    target_tile_found = True
                i -= 1
            if not target_tile_found:
                self.target_tile_row = pacman_row

        else:
            self.target_tile_column = pacman_column
            i = 4
            target_tile_found = False
            while i > 0 and not target_tile_found:
                if pacman_row + i < 36 and self.tiles[pacman_row + i][pacman_column] != 1:
                    self.target_tile_row = pacman_row + i
                    target_tile_found = True
                i -= 1
            if not target_tile_found:
                self.target_tile_row = pacman_row

    def move(self):
        self.image_counter += 1
        if self.image_counter % 8 == 0:
            if self.image_number == 1:
                self.image_number = 2
            elif self.image_number == 2:
                self.image_number = 1

        # if idle
        if self.idle:
            if self.y == 143:
                # move up when at bottom of ghost house
                self.direction = 'up'
            elif self.y == 135:
                # if been told to leave maze, keep moving up
                if self.enter_maze:
                    self.idle = False
                # otherwise, move down when at top of ghost house
                else:
                    self.direction = 'down'

        elif self.enter_maze:
            # if now in maze
            if self.x == 13.5 * 8 + 3 and self.y == 14 * 8 + 3:
                self.enter_maze = False
                self.direction = 'left'
            # otherwise move up
            else:
                self.direction = 'up'

        # if at end of tunnels, teleport
        elif self.x == 0:
            self.x = 28 * 8 - 1
        elif self.x == 28 * 8 - 1:
            self.x = 0

        elif self.x == 13.5 * 8 + 3 and self.y == 14 * 8 + 3 and self.mode == 'EATEN':
            self.direction = 'down'

        elif self.x == 13.5 * 8 + 3 and self.y == 17 * 8 + 3:
            self.enter_maze = True
            self.mode = 'CHASE'
            self.direction = None

        # if at node
        elif tiles_nodes[self.get_row()][self.get_column()] == 8 and self.at_tile_center():
            if self.mode == 'SCATTER':
                # pink ghost circles around top left corner
                if self.get_row() == 8 and self.get_column() == 6:
                    self.calculate_path(4, 6)
                elif self.get_row() == 4 and self.get_column() == 6:
                    self.calculate_path(4, 1)
                elif self.get_row() == 4 and self.get_column() == 1:
                    self.calculate_path(8, 1)
                else:
                    self.calculate_path(8, 6)

                if (self.path[-2][0] - self.path[-1][0]) < 0 and 'up' != self.get_reverse_direction():
                    self.direction = 'up'
                elif (self.path[-2][0] - self.path[-1][0]) > 0 and 'down' != self.get_reverse_direction():
                    self.direction = 'down'
                elif (self.path[-2][1] - self.path[-1][1]) > 0 and 'right' != self.get_reverse_direction():
                    self.direction = 'right'
                elif (self.path[-2][1] - self.path[-1][1]) < 0 and 'left' != self.get_reverse_direction():
                    self.direction = 'left'
                else:
                    directions = self.get_possible_directions()
                    if directions:
                        self.direction = directions[0]

            elif self.mode == 'CHASE':
                # at left tunnel entrance
                if self.go_to_tunnel and self.get_row() == 17 and self.get_column() == 6:
                    self.go_to_tunnel = False
                    self.direction = 'left'

                # at right tunnel entrance
                elif self.go_to_tunnel and self.get_row() == 17 and self.get_column() == 21:
                    self.go_to_tunnel = False
                    self.direction = 'right'

                else:
                    self.calculate_path(self.target_tile_row, self.target_tile_column)

                    if len(self.path) == 1:
                        if self.go_to_tunnel and self.get_column() == 6:
                            self.go_to_tunnel = False
                            self.direction = 'left'
                        elif self.go_to_tunnel and self.get_column() == 21:
                            self.go_to_tunnel = False
                            self.direction = 'right'
                        else:
                            self.direction = self.get_possible_directions()[0]

                    elif (self.path[-2][0] - self.path[-1][0]) < 0 and 'up' != self.get_reverse_direction():
                        self.direction = 'up'
                    elif (self.path[-2][0] - self.path[-1][0]) > 0 and 'down' != self.get_reverse_direction():
                        self.direction = 'down'
                    elif (self.path[-2][1] - self.path[-1][1]) > 0 and 'right' != self.get_reverse_direction():
                        self.direction = 'right'
                    elif (self.path[-2][1] - self.path[-1][1]) < 0 and 'left' != self.get_reverse_direction():
                        self.direction = 'left'
                    else:
                        directions = self.get_possible_directions()
                        if directions:
                            self.direction = directions[0]

            elif self.mode == 'FRIGHTENED':
                possible_directions = self.get_possible_directions()
                if self.get_next_tile(self.direction) != 1:
                    possible_directions.append(self.direction)
                index = random.randint(0, len(possible_directions) - 1)
                self.direction = possible_directions[index]

            elif self.mode == 'EATEN':
                # calculates path to ghost house entrance/exit
                self.calculate_path(14, 13)

                if len(self.path) == 1:
                    print('at ghost house')
                elif (self.path[-2][0] - self.path[-1][0]) < 0 and 'up' != self.get_reverse_direction():
                    self.direction = 'up'
                elif (self.path[-2][0] - self.path[-1][0]) > 0 and 'down' != self.get_reverse_direction():
                    self.direction = 'down'
                elif (self.path[-2][1] - self.path[-1][1]) > 0 and 'right' != self.get_reverse_direction():
                    self.direction = 'right'
                elif (self.path[-2][1] - self.path[-1][1]) < 0 and 'left' != self.get_reverse_direction():
                    self.direction = 'left'
                else:
                    directions = self.get_possible_directions()
                    if directions:
                        self.direction = directions[0]

        # set image
        if self.mode == 'SCATTER' or self.mode == 'CHASE':
            if self.direction:
                self.image = pygame.image.load(os.path.join(
                    'pacman_images',
                    str(self.colour) + '_ghost_' + str(self.direction) + '_' + str(self.image_number) + '.png'))
        elif self.mode == 'FRIGHTENED':
            if not self.flash_while_frightened:
                self.image = pygame.image.load(os.path.join(
                    'pacman_images', 'frightened_ghost_' + str(self.image_number) + '.png'))
            else:
                if self.image_counter % 6 == 0:
                    if self.is_white:
                        self.is_white = False
                        self.flash_number += 1
                        self.image = pygame.image.load(os.path.join(
                            'pacman_images', 'frightened_ghost_' + str(self.image_number) + '.png'))
                    else:
                        self.is_white = True
                        self.image = pygame.image.load(os.path.join(
                            'pacman_images', 'frightened_ghost_flash_' + str(self.image_number) + '.png'))
        elif self.mode == 'EATEN':
            if self.direction:
                self.image = pygame.image.load(os.path.join(
                    'pacman_images', 'eaten_eyes_' + str(self.direction) + '.png'))

        if self.direction == 'left':
            self.x -= 1
        elif self.direction == 'right':
            self.x += 1
        elif self.direction == 'up':
            self.y -= 1
        elif self.direction == 'down':
            self.y += 1

    def reset(self):
        self.mode = 'SCATTER'
        self.x = 111
        self.y = 17 * 8 + 3
        self.direction = 'down'
        self.flash_while_frightened = False
        self.is_white = False
        self.flash_number = 0
        self.enter_maze = False
        self.idle = True
        self.image = pygame.image.load(os.path.join('pacman_images', 'pink_ghost_down_1.png'))


class BlueGhost(Ghost):
    def __init__(self, maze_tiles):
        super().__init__(maze_tiles)
        # attributes that need to be changed from the normal ghost class
        self.x = 95
        self.y = 17 * 8 + 3
        self.direction = 'up'
        self.colour = 'blue'
        self.image = pygame.image.load(os.path.join('pacman_images', 'blue_ghost_up_1.png'))

        # new attributes
        self.idle = True

    def calculate_target_tile(self, pacman_row, pacman_column):
        # choosing random direction
        directions = ['up', 'down', 'left', 'right']
        direction = random.choice(directions)

        # blue ghost chooses random tile 3 tiles away from Pac-Man
        if direction == 'left':
            self.target_tile_row = pacman_row
            i = 3
            target_tile_found = False
            while i > 0 and not target_tile_found:
                # check index isn't out of range and isn't a wall
                if pacman_column - i > 0 and self.tiles[pacman_row][pacman_column - i] != 1:
                    self.target_tile_column = pacman_column - i
                    target_tile_found = True
                i -= 1
            if not target_tile_found:
                self.target_tile_column = pacman_column

        elif direction == 'right':
            self.target_tile_row = pacman_row
            i = 3
            target_tile_found = False
            while i > 0 and not target_tile_found:
                if pacman_column + i < 27 and self.tiles[pacman_row][pacman_column + i] != 1:
                    self.target_tile_column = pacman_column + i
                    target_tile_found = True
                i -= 1
            if not target_tile_found:
                self.target_tile_column = pacman_column

        elif direction == 'up':
            self.target_tile_column = pacman_column
            i = 3
            target_tile_found = False
            while i > 0 and not target_tile_found:
                if pacman_row - i > 0 and self.tiles[pacman_row - i][pacman_column] != 1:
                    self.target_tile_row = pacman_row - i
                    target_tile_found = True
                i -= 1
            if not target_tile_found:
                self.target_tile_row = pacman_row

        else:
            self.target_tile_column = pacman_column
            i = 3
            target_tile_found = False
            while i > 0 and not target_tile_found:
                if pacman_row + i < 36 and self.tiles[pacman_row + i][pacman_column] != 1:
                    self.target_tile_row = pacman_row + i
                    target_tile_found = True
                i -= 1
            if not target_tile_found:
                self.target_tile_row = pacman_row

    def move(self):
        # choosing correct legs
        self.image_counter += 1
        if self.image_counter % 8 == 0:
            if self.image_number == 1:
                self.image_number = 2
            elif self.image_number == 2:
                self.image_number = 1

        # if idle
        if self.idle:
            if self.x == 95:
                # if at side of ghost house move down or up when get too high or low
                if self.y == 143:
                    # move up when at bottom of ghost house
                    self.direction = 'up'
                elif self.y == 135:
                    # move down when at top of ghost house
                    self.direction = 'down'
                # if have been told to enter maze and centred vertically in ghost house
                elif self.y == 139 and self.enter_maze:
                    self.direction = 'right'
            # if below entrance, exit idle. This will take ghost to enter_maze handling
            elif self.x == 111:
                self.idle = False
                self.direction = 'up'

        elif self.enter_maze:
            # if now in maze
            if self.x == 13.5 * 8 + 3 and self.y == 14 * 8 + 3:
                self.enter_maze = False
                self.direction = 'left'
            # otherwise move up
            else:
                self.direction = 'up'

        # if at end of tunnels, teleport
        elif self.x == 0:
            self.x = 28 * 8 - 1
        elif self.x == 28 * 8 - 1:
            self.x = 0

        elif self.x == 13.5 * 8 + 3 and self.y == 14 * 8 + 3 and self.mode == 'EATEN':
            self.direction = 'down'

        elif self.x == 13.5 * 8 + 3 and self.y == 17 * 8 + 3:
            self.enter_maze = True
            self.mode = 'CHASE'
            self.direction = None

        # if at node
        elif tiles_nodes[self.get_row()][self.get_column()] == 8 and self.at_tile_center():
            if self.mode == 'SCATTER':
                # blue ghost circles round bottom right corner of maze
                if self.get_row() == 26 and self.get_column() == 21:
                    self.calculate_path(29, 21)
                elif self.get_row() == 29 and self.get_column() == 21:
                    self.calculate_path(29, 24)
                elif self.get_row() == 29 and self.get_column() == 24:
                    self.calculate_path(29, 26)
                elif self.get_row() == 29 and self.get_column() == 26:
                    self.calculate_path(32, 26)
                elif self.get_row == 32 and self.get_column() == 26:
                    self.calculate_path(32, 15)
                elif self.get_row == 32 and self.get_column() == 15:
                    self.calculate_path(29, 15)
                elif self.get_row() == 29 and self.get_column() == 15:
                    self.calculate_path(29, 18)
                elif self.get_row() == 29 and self.get_column() == 18:
                    self.calculate_path(26, 18)
                else:
                    self.calculate_path(26, 21)

                if (self.path[-2][0] - self.path[-1][0]) < 0 and 'up' != self.get_reverse_direction():
                    self.direction = 'up'
                elif (self.path[-2][0] - self.path[-1][0]) > 0 and 'down' != self.get_reverse_direction():
                    self.direction = 'down'
                elif (self.path[-2][1] - self.path[-1][1]) > 0 and 'right' != self.get_reverse_direction():
                    self.direction = 'right'
                elif (self.path[-2][1] - self.path[-1][1]) < 0 and 'left' != self.get_reverse_direction():
                    self.direction = 'left'
                else:
                    directions = self.get_possible_directions()
                    if directions:
                        self.direction = directions[0]

            elif self.mode == 'CHASE':
                # at left tunnel entrance
                if self.go_to_tunnel and self.get_row() == 17 and self.get_column() == 6:
                    self.go_to_tunnel = False
                    self.direction = 'left'

                # at right tunnel entrance
                elif self.go_to_tunnel and self.get_row() == 17 and self.get_column() == 21:
                    self.go_to_tunnel = False
                    self.direction = 'right'

                else:
                    self.calculate_path(self.target_tile_row, self.target_tile_column)

                    if len(self.path) == 1:
                        if self.go_to_tunnel and self.get_column() == 6:
                            self.go_to_tunnel = False
                            self.direction = 'left'
                        elif self.go_to_tunnel and self.get_column() == 21:
                            self.go_to_tunnel = False
                            self.direction = 'right'
                        else:
                            self.direction = self.get_possible_directions()[0]

                    elif (self.path[-2][0] - self.path[-1][0]) < 0 and 'up' != self.get_reverse_direction():
                        self.direction = 'up'
                    elif (self.path[-2][0] - self.path[-1][0]) > 0 and 'down' != self.get_reverse_direction():
                        self.direction = 'down'
                    elif (self.path[-2][1] - self.path[-1][1]) > 0 and 'right' != self.get_reverse_direction():
                        self.direction = 'right'
                    elif (self.path[-2][1] - self.path[-1][1]) < 0 and 'left' != self.get_reverse_direction():
                        self.direction = 'left'
                    else:
                        directions = self.get_possible_directions()
                        if directions:
                            self.direction = directions[0]

            elif self.mode == 'FRIGHTENED':
                possible_directions = self.get_possible_directions()
                if self.get_next_tile(self.direction) != 1:
                    possible_directions.append(self.direction)
                index = random.randint(0, len(possible_directions) - 1)
                self.direction = possible_directions[index]

            elif self.mode == 'EATEN':
                # calculates path to ghost house entrance/exit
                self.calculate_path(14, 13)

                if len(self.path) == 1:
                    print('at ghost house')
                elif (self.path[-2][0] - self.path[-1][0]) < 0 and 'up' != self.get_reverse_direction():
                    self.direction = 'up'
                elif (self.path[-2][0] - self.path[-1][0]) > 0 and 'down' != self.get_reverse_direction():
                    self.direction = 'down'
                elif (self.path[-2][1] - self.path[-1][1]) > 0 and 'right' != self.get_reverse_direction():
                    self.direction = 'right'
                elif (self.path[-2][1] - self.path[-1][1]) < 0 and 'left' != self.get_reverse_direction():
                    self.direction = 'left'
                else:
                    directions = self.get_possible_directions()
                    if directions:
                        self.direction = directions[0]

        # set image
        if self.mode == 'SCATTER' or self.mode == 'CHASE':
            if self.direction:
                self.image = pygame.image.load(os.path.join(
                    'pacman_images',
                    str(self.colour) + '_ghost_' + str(self.direction) + '_' + str(self.image_number) + '.png'))
        elif self.mode == 'FRIGHTENED':
            if not self.flash_while_frightened:
                self.image = pygame.image.load(os.path.join(
                    'pacman_images', 'frightened_ghost_' + str(self.image_number) + '.png'))
            else:
                if self.image_counter % 6 == 0:
                    if self.is_white:
                        self.is_white = False
                        self.flash_number += 1
                        self.image = pygame.image.load(os.path.join(
                            'pacman_images', 'frightened_ghost_' + str(self.image_number) + '.png'))
                    else:
                        self.is_white = True
                        self.image = pygame.image.load(os.path.join(
                            'pacman_images', 'frightened_ghost_flash_' + str(self.image_number) + '.png'))
        elif self.mode == 'EATEN':
            if self.direction:
                self.image = pygame.image.load(os.path.join(
                    'pacman_images', 'eaten_eyes_' + str(self.direction) + '.png'))

        if self.direction == 'left':
            self.x -= 1
        elif self.direction == 'right':
            self.x += 1
        elif self.direction == 'up':
            self.y -= 1
        elif self.direction == 'down':
            self.y += 1

    def reset(self):
        self.mode = 'SCATTER'
        self.x = 95
        self.y = 17 * 8 + 3
        self.direction = 'up'
        self.image = pygame.image.load(os.path.join('pacman_images', 'blue_ghost_up_1.png'))
        self.flash_while_frightened = False
        self.is_white = False
        self.flash_number = 0
        self.enter_maze = False
        self.idle = True


class Game:
    def __init__(self):
        self.score = 0
        self.tiles = deepcopy(tiles)
        self.pacman = Pacman(111, 211, self.tiles)
        self.red_ghost = Ghost(self.tiles)
        self.pink_ghost = PinkGhost(self.tiles)
        self.blue_ghost = BlueGhost(self.tiles)
        self.orange_ghost = OrangeGhost(self.tiles)
        self.ghosts = [self.orange_ghost, self.blue_ghost,
                       self.pink_ghost, self.red_ghost]

        # timer used to switch between ghost modes
        self.chase_scatter_start_time = time.time()
        self.chase_scatter_timer = None
        self.chase_scatter_timer_previous = 0

        # frightened mode
        self.frightened_start_time = None
        self.frightened_timer = None
        self.ghosts_frightened = False

        # to freeze game when ghost eaten
        self.freeze = False
        self.freeze_counter = 0

        # used to add correct points to score when ghost eaten
        self.num_ghosts_eaten = 0
        # used to display points at correct ghost position
        self.ghost_eaten = None

        # dot count used for when make ghosts leave ghost house & when to display fruit
        self.dots_eaten = 0

        # count used for modular division to get things to happen every x frames
        self.count = 0

        # for energiser flash
        self.energiser_visible = False

        # for fruit, fruit points display, and fruit counter
        self.fruit_visible = False
        self.fruit_eaten = False
        self.fruit_visible_counter = 0
        self.fruit_points_showing = False
        self.fruit_score_show_counter = 0
        self.num_fruits_eaten = 0

        # for Pac-Man death animation
        self.pacman_dead = False
        self.death_image_number = 0

        # for ready screen
        self.ready_screen = True
        self.ready_counter = 0

        # for game over screen
        self.game_over = False
        self.game_over_counter = 0

        # for maze flashing when level up
        self.level_up = False
        self.level_up_counter = 0
        self.level_up_flash_number = 0
        self.level_up_maze_image_number = 1

        # level starts at 1
        self.level = 1

    def update(self):
        self.count += 1

        # energiser flash
        if self.count % 10 == 0:
            if self.energiser_visible:
                self.energiser_visible = False
            else:
                self.energiser_visible = True

        if self.ready_screen:
            self.ready_counter += 1
            # if ready screen lasted for 2 seconds (2 * 60)
            if self.ready_counter > 120:
                self.ready_screen = False
                self.ready_counter = 0
                # reset chase/scatter timer
                self.chase_scatter_start_time = time.time()
                self.chase_scatter_timer_previous = 0

        elif self.level_up:
            self.level_up_counter += 1

        elif self.game_over:
            self.game_over_counter += 1
            # if game over screen lasted for 2 seconds (2 * 60)
            if self.game_over_counter > 180:
                self.game_over = False
                self.game_over_counter = 0
                # reset score
                self.score = 0
                # reset level
                self.level = 1
                # reset dots
                self.tiles = deepcopy(tiles)
                self.dots_eaten = 0
                # reset fruit
                self.fruit_eaten = False
                # reset number of fruits eaten
                self.num_fruits_eaten = 0
                # reset lives
                self.pacman.lives_left = 2
                # ready screen
                self.reset_maze()
                self.ready_screen = True

        else:
            if not self.pacman_dead:
                if self.freeze:
                    self.freeze_counter += 1
                    if self.freeze_counter > 60:
                        self.freeze_counter = 0
                        self.freeze = False
                        self.ghost_eaten = None

                if not self.freeze:
                    self.update_pacman()
                    self.update_timer()
                    self.update_ghosts()
                    self.fruit_handling()
                self.update_dots()

    def update_pacman(self):
        self.pacman.tiles = self.tiles
        self.pacman.move()

        # if pacman eats a fruit
        if self.fruit_visible:
            if (self.pacman.get_column() == 13 or self.pacman.get_column() == 14) and self.pacman.get_row() == 20:
                self.fruit_eaten = True
                self.num_fruits_eaten += 1
                self.fruit_visible = False

                if self.level == 1:
                    self.score += 100
                elif self.level == 2:
                    self.score += 300
                elif self.level == 3:
                    self.score += 500
                elif self.level == 4:
                    self.score += 700
                elif self.level == 5:
                    self.score += 1000
                elif self.level == 6:
                    self.score += 2000
                elif self.level == 7:
                    self.score += 3000
                else:
                    self.score += 5000

                # display score
                self.fruit_points_showing = True

        # if pacman eats an energiser
        if self.pacman.get_current_tile() == 3:
            if not self.ghosts_frightened:
                # tell game that ghosts are frightened
                self.ghosts_frightened = True
                # pause chase/scatter timer
                self.chase_scatter_timer_previous += time.time() - self.chase_scatter_start_time

            for ghost in self.ghosts:
                # only can become frightened if not eaten
                if ghost.mode != 'EATEN':
                    # if not already frightened, reverse direction
                    if ghost.mode != 'FRIGHTENED':
                        ghost.direction = ghost.get_reverse_direction()
                        ghost.mode = 'FRIGHTENED'
                    ghost.flash_while_frightened = False
                    ghost.is_white = False
                    ghost.flash_number = 0

            # start frightened timer
            self.frightened_start_time = time.time()
            # reset ghosts eaten count
            self.num_ghosts_eaten = 0

    def update_timer(self):
        if self.ghosts_frightened:
            self.frightened_timer = time.time() - self.frightened_start_time
        else:
            self.chase_scatter_timer = time.time() - self.chase_scatter_start_time + self.chase_scatter_timer_previous

    def update_ghosts(self):
        # update each ghosts tiles
        for ghost in self.ghosts:
            ghost.tiles = self.tiles

        if self.ghosts_frightened:
            # frightened mode duration and flash number depends on level
            if self.level == 1:
                frightened_duration = 6
                flash_limit = 5
            elif self.level == 2:
                frightened_duration = 5
                flash_limit = 5
            elif self.level == 3:
                frightened_duration = 4
                flash_limit = 4
            elif self.level == 4:
                frightened_duration = 3
                flash_limit = 3
            elif self.level == 5:
                frightened_duration = 2
                flash_limit = 2
            else:
                frightened_duration = 1
                flash_limit = 1

            if self.frightened_timer > frightened_duration:
                # each ghost that is frightened now starts flashing
                for ghost in self.ghosts:
                    if ghost.mode == 'FRIGHTENED':
                        ghost.flash_while_frightened = True

                # find a ghost that is frightened and use its flash number
                if self.red_ghost.mode == 'FRIGHTENED':
                    flash_number = self.red_ghost.flash_number
                elif self.pink_ghost.mode == 'FRIGHTENED':
                    flash_number = self.pink_ghost.flash_number
                elif self.blue_ghost.mode == 'FRIGHTENED':
                    flash_number = self.blue_ghost.flash_number
                elif self.orange_ghost.mode == 'FRIGHTENED':
                    flash_number = self.orange_ghost.flash_number
                # if no ghosts frightened, exit frightened mode
                else:
                    flash_number = flash_limit
                
                # if ghosts have flashed 5 times then end frightened mode
                if flash_number >= flash_limit:
                    # each ghost that is in frightened mode leaves frightened mode
                    for ghost in self.ghosts:
                        if ghost.mode == 'FRIGHTENED':
                            ghost.flash_number = 0
                            ghost.flash_while_frightened = False
                            ghost.chase_or_scatter(self.chase_scatter_timer, self.level)
                        
                    # separately
                    # need to set game's frightened attribute to false
                    self.ghosts_frightened = False
                    self.frightened_start_time = None
                    self.frightened_timer = None
                    self.chase_scatter_start_time = time.time()

        else:
            # call each ghost's chase_or_scatter method if they aren't eaten
            for ghost in self.ghosts:
                if ghost.mode != 'EATEN':
                    ghost.chase_or_scatter(self.chase_scatter_timer, self.level)

        # calculate target tiles

        # red ghost
        if self.red_ghost.mode == 'CHASE':
            self.red_ghost.calculate_target_tile(self.pacman.get_row(), self.pacman.get_column())

        # pink ghost
        if self.dots_eaten >= 0 and self.pink_ghost.idle:
            self.pink_ghost.enter_maze = True
        if self.pink_ghost.mode == 'CHASE':
            self.pink_ghost.calculate_target_tile_pink(
                self.pacman.get_row(), self.pacman.get_column(), self.pacman.direction
            )

        # blue ghost
        if self.dots_eaten >= 30 and self.blue_ghost.idle:
            self.blue_ghost.enter_maze = True
        if self.blue_ghost.mode == 'CHASE':
            self.blue_ghost.calculate_target_tile(self.pacman.get_row(), self.pacman.get_column())

        # orange ghost
        if self.dots_eaten >= 60 and self.orange_ghost.idle:
            self.orange_ghost.enter_maze = True
        if self.orange_ghost.mode == 'CHASE':
            self.orange_ghost.calculate_target_tile(self.pacman.get_row(), self.pacman.get_column())

        # move ghosts
        for ghost in self.ghosts:
            if ghost.mode == 'FRIGHTENED':
                if self.count % 2 == 0:
                    ghost.move()
            else:
                ghost.move()

        # check ghost collision with pacman
        for ghost in self.ghosts:
            # if ghost and pacman share tile (or their centres are 1 pixel away from each other)
            if (ghost.get_row() == self.pacman.get_row() and ghost.get_column() == self.pacman.get_column()) \
                    or \
                    (ghost.get_row() == self.pacman.get_row() and abs(ghost.x - self.pacman.x) == 1) \
                    or \
                    (ghost.get_column() == self.pacman.get_column() and abs(ghost.y - self.pacman.y) == 1):
                if ghost.mode == 'SCATTER' or ghost.mode == 'CHASE':
                    self.pacman_dead = True
                    self.count = 1
                    self.death_image_number = 0
                elif ghost.mode == 'FRIGHTENED':
                    # so that two ghosts can't be eaten on same game loop
                    if self.ghost_eaten is None:
                        self.num_ghosts_eaten += 1
                        self.ghost_eaten = str(ghost.colour)
                        if self.num_ghosts_eaten == 1:
                            self.score += 200
                        elif self.num_ghosts_eaten == 2:
                            self.score += 400
                        elif self.num_ghosts_eaten == 3:
                            self.score += 800
                        else:
                            self.score += 1600

                        ghost.mode = 'EATEN'
                        self.freeze = True
                        self.frightened_start_time += 1

    def render_maze(self):
        # display empty maze
        WINDOW.blit(MAZE_IMAGE, (0, 0))

        # display dots and energisers
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if self.tiles[y][x] == 2:
                    pygame.draw.rect(WINDOW, DOT_COLOUR, (x * 8 + 3, y * 8 + 3, 2, 2))
                elif self.tiles[y][x] == 3:
                    # only display energisers if visible so they flash
                    if self.energiser_visible:
                        WINDOW.blit(ENERGISER_IMAGE, (x * 8, y * 8))

        # ready text
        if self.ready_screen:
            ready_text = FONT.render('READY!', False, YELLOW)
            WINDOW.blit(ready_text, (11 * 8, 20 * 8 - 2))

        # level up
        if self.level_up and self.level_up_counter > 120:  # if 2 second freeze complete
            # alternate between white and blue maze image every 16 frames
            if (self.level_up_counter - 120) % 16 == 0:
                if self.level_up_maze_image_number == 1:  # (white)
                    self.level_up_maze_image_number = 2  # change to blue
                    # increment flash count
                    self.level_up_flash_number += 1
                else:
                    # if maze is blue, check flash count
                    if self.level_up_flash_number == 4:  # if had 4 flashes
                        # end level up flashing
                        self.level_up = False
                        # reset level up attributes
                        self.level_up_counter = 0
                        self.level_up_flash_number = 0
                        self.level_up_maze_image_number = 1
                        # new level
                        self.level += 1
                        # reset character positions etc
                        self.reset_maze()
                        # reset dots
                        self.tiles = deepcopy(tiles)
                        self.dots_eaten = 0
                        # reset fruit
                        self.fruit_eaten = False
                        # change to ready screen
                        self.ready_screen = True
                    else:
                        # if under 4 flashes, change to white
                        self.level_up_maze_image_number = 1

            if self.level_up:
                maze_flash_image = pygame.image.load(os.path.join(
                    'pacman_images', f'maze_flash_{self.level_up_maze_image_number}.png'))
            else:
                maze_flash_image = pygame.image.load(os.path.join('pacman_images', 'maze_flash_2.png'))
            WINDOW.blit(maze_flash_image, (0, 0))
            WINDOW.blit(PACMAN_MOUTH_SHUT_IMAGE, (self.pacman.x - 6, self.pacman.y - 6))

        # death animation
        elif self.pacman_dead:
            if self.death_image_number == 0:
                time.sleep(1)
                self.death_image_number += 1
            if self.count % 8 == 0:
                self.death_image_number += 1

            if self.death_image_number == 13:
                if self.pacman.lives_left > 0:
                    self.reset_maze()
                    self.pacman.lives_left -= 1
                    self.ready_screen = True
                else:
                    self.pacman_dead = False
                    self.game_over = True
            else:
                WINDOW.blit(
                    pygame.image.load(os.path.join(
                        'pacman_images',
                        'pacman_death_'+str(self.death_image_number)+'.png')),
                    (self.pacman.x - 6, self.pacman.y - 6)
                )

        # game over text
        elif self.game_over:
            game_over_text = FONT.render('GAME  OVER', False, RED)
            WINDOW.blit(game_over_text, (9 * 8, 20 * 8 - 2))

        else:
            # display fruit
            if self.fruit_visible:
                WINDOW.blit(CHERRY_IMAGE, (13 * 8, 20 * 8 - 4))

            if self.freeze:
                if self.num_ghosts_eaten == 1:
                    eaten_ghost_score = 200
                elif self.num_ghosts_eaten == 2:
                    eaten_ghost_score = 400
                elif self.num_ghosts_eaten == 3:
                    eaten_ghost_score = 800
                else:
                    eaten_ghost_score = 1600

                if self.ghost_eaten == 'red':
                    x = self.red_ghost.x
                    y = self.red_ghost.y
                elif self.ghost_eaten == 'pink':
                    x = self.pink_ghost.x
                    y = self.pink_ghost.y
                elif self.ghost_eaten == 'blue':
                    x = self.blue_ghost.x
                    y = self.blue_ghost.y
                else:
                    x = self.orange_ghost.x
                    y = self.orange_ghost.y
                WINDOW.blit(
                    pygame.image.load(os.path.join('pacman_images',
                                                   'eaten_ghost_score_'+str(eaten_ghost_score)+'.png')),
                    (x - 8, y - 6))

            else:
                if self.level_up:
                    WINDOW.blit(PACMAN_MOUTH_SHUT_IMAGE, (self.pacman.x - 6, self.pacman.y - 6))
                else:
                    WINDOW.blit(self.pacman.image, (self.pacman.x - 6, self.pacman.y - 6))

            for ghost in self.ghosts:
                if self.ghost_eaten != str(ghost.colour):
                    WINDOW.blit(ghost.image, (ghost.x - 6, ghost.y - 6))

            # show fruit points if just eaten fruit
            if self.fruit_points_showing:
                if self.level == 1:
                    points = 100
                elif self.level == 2:
                    points = 300
                elif self.level == 3:
                    points = 500
                elif self.level == 4:
                    points = 700
                elif self.level == 5:
                    points = 1000
                elif self.level == 6:
                    points = 2000
                elif self.level == 7:
                    points = 3000
                else:
                    points = 5000

                WINDOW.blit(pygame.image.load(os.path.join('pacman_images',
                                                           f'fruit_points_{points}.png')), (13 * 8, 20 * 8 - 4))

            #self.blue_ghost.draw_target_tile()
            #self.pink_ghost.draw_target_tile()
            #self.orange_ghost.draw_target_tile()
            #pygame.draw.circle(WINDOW, ORANGE, (self.pacman.x, self.pacman.y), 8 * 8, 2)

    def reset_maze(self):
        self.pacman.reset()
        for ghost in self.ghosts:
            ghost.reset()
        self.ghosts_frightened = False
        self.num_ghosts_eaten = 0
        self.ghost_eaten = None
        self.energiser_visible = False
        self.count = 0
        self.fruit_visible = False
        self.fruit_points_showing = False
        self.fruit_score_show_counter = 0
        self.pacman_dead = False

    def fruit_handling(self):
        if self.dots_eaten == 50 and not self.fruit_eaten:
            self.fruit_visible_counter = 0
            self.fruit_visible = True

        if self.fruit_visible:
            self.fruit_visible_counter += 1
            if self.fruit_visible_counter > 60 * 9:
                self.fruit_visible = False

        if self.fruit_points_showing:
            self.fruit_score_show_counter += 1
            if self.fruit_score_show_counter == 2 * 60:
                self.fruit_points_showing = False
                self.fruit_score_show_counter = 0

    def update_dots(self):
        if self.pacman.get_current_tile() == 2:  # dot = 10 points
            self.tiles[self.pacman.get_row()][self.pacman.get_column()] = 0
            self.score += 10
            self.dots_eaten += 1
            print(self.dots_eaten)
        elif self.pacman.get_current_tile() == 3:  # energiser = 50 points
            self.tiles[self.pacman.get_row()][self.pacman.get_column()] = 0
            self.score += 50
            self.dots_eaten += 1
            print(self.dots_eaten)

        if self.dots_eaten == 244:
            self.level_up = True

    def display_score(self):
        # display score
        if self.score == 0:
            score = '00'
        else:
            score = str(self.score)

        score_position = 7 - len(score)
        score_text = FONT.render(score, False, WHITE)
        WINDOW.blit(score_text, (score_position * 8, 1 * 8))  # score displayed to the left

        # display high score
        high_score = self.get_high_score()

        high_score_position = 17 - len(str(high_score))
        high_score_text = FONT.render(high_score, False, WHITE)
        WINDOW.blit(high_score_text, (high_score_position * 8, 1 * 8))  # high score displayed to the right

        # display HIGH SCORE text
        high_score_text = FONT.render('HIGH SCORE', False, WHITE)
        WINDOW.blit(high_score_text, (9 * 8, 0 * 8))  # high score text

    def get_high_score(self):
        # get high score file
        try:
            # opens file to be read from
            high_score_file = open('high_score.txt', 'rt')
        except FileNotFoundError:
            # creates file first
            high_score_file = open('high_score.txt', 'xt')
            high_score_file.close()
            # opens file to be read from
            high_score_file = open('high_score.txt', 'rt')

        # reads first line from file which is the saved high score
        high_score = high_score_file.readline()
        # closes file after read from
        high_score_file.close()

        try:
            high_score = int(high_score)
        except ValueError:
            high_score = 0

        if self.score > high_score:
            high_score = self.score
            # opens file to be written to
            high_score_file = open('high_score.txt', 'wt')
            # updates high score
            high_score_file.write(str(self.score))
            high_score_file.close()

        if high_score == 0:
            return '00'
        else:
            return str(high_score)

    def display_lives_left(self):
        for i in range(self.pacman.lives_left):
            WINDOW.blit(LIFE_INDICATOR_IMAGE, ((17 * i) + 8, 34 * 8 + 3))

    def display_fruits_eaten(self):
        num_fruits = str(self.num_fruits_eaten)
        # display cherry image
        WINDOW.blit(CHERRY_IMAGE, (25 * 8 - len(num_fruits) * 8, 34 * 8 + 1))
        # display number next to cherry image
        fruits_eaten_number_text = FONT.render(num_fruits, False, WHITE)
        WINDOW.blit(fruits_eaten_number_text, (27 * 8 - len(num_fruits) * 8, 34 * 8 + 5))

    def display_timer_and_mode(self):
        if self.ghosts_frightened:
            timer_text = round(self.frightened_timer, 1)
        else:
            if self.chase_scatter_timer:
                timer_text = round(self.chase_scatter_timer, 1)
            else:
                timer_text = 0
        timer = FONT.render(f'TIMER: {timer_text}', False, WHITE)
        WINDOW.blit(timer, (1 * 8, 34 * 8))

        # display mode
        mode = FONT.render(f'MODE: {self.red_ghost.mode}', False, WHITE)
        WINDOW.blit(mode, (14 * 8, 34 * 8))

    def draw_window(self):
        self.render_maze()
        self.display_score()
        #self.display_timer_and_mode()
        self.display_lives_left()
        self.display_fruits_eaten()
        pygame.display.update()

    @staticmethod
    def run():
        clock = pygame.time.Clock()
        run = True
        while run:  # game loop
            clock.tick(FPS)  # controls speed of while loop: game won't run too quickly
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # if user wants to quit window, exit while loop
                    run = False
                elif event.type == KEYDOWN:  # key inputs
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        game.pacman.change_direction = 'left'
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        game.pacman.change_direction = 'right'
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        game.pacman.change_direction = 'up'
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        game.pacman.change_direction = 'down'
            game.update()
            game.draw_window()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":  # this is so that the game can only be run from the main file
    game = Game()
    game.run()
