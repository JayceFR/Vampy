from turtle import speed
from winreg import KEY_CREATE_SUB_KEY
import pygame

class Player():
    def __init__(self, loc, width, height ) -> None:
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.speed = 5
        self.moving_right = False
        self.moving_left = False
        self.jump = False
        self.jump_cooldown = 200
        self.jump_last_update = 0
        self.gravity = 9.81

    def collision_test(self, tiles):
        hitlist = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hitlist.append(tile)
        return hitlist

    def collision_checker(self, tiles):
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        self.rect.x += self.movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                self.rect.right = tile.left
                collision_types["right"] = True
            elif self.movement[0] < 0:
                self.rect.left = tile.right
                collision_types["left"] = True
        self.rect.y += self.movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types["bottom"] = True
            if self.movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types["top"] = True
        return collision_types

    def move(self, tiles, time):
        self.movement = [0,0]
        if self.moving_right:
            self.movement[0] += self.speed
            self.moving_right = not self.moving_right
        if self.moving_left:
            self.movement[0] -= self.speed
            self.moving_left = not self.moving_left
        if self.jump:
            if time - self.jump_last_update > self.jump_cooldown:
                self.movement[1] -= self.gravity * 6
                self.jump_last_update = time
            self.jump = False
        self.movement[1] += self.gravity
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            self.moving_right = True
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            self.moving_left = True
        if key_pressed[pygame.K_SPACE] or key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            self.jump = True
        collision_type = self.collision_checker(tiles)
    def draw(self, display):
        pygame.draw.rect(display, (255,0,0), self.rect)

class Map():
    def read_map(self, map_loc):
        f = open(map_loc, "r")
        map = f.read()
        f.close()
        map = map.split("\n")
        final_map = []
        for row in map:
            rows = []
            for element in row:
                rows.append(element)
            final_map.append(rows)
        return final_map

    def __init__(self, map_loc, tile1, tile2) -> None:
        self.map = self.read_map(map_loc)
        self.tile1 = tile1
        self.tile2 = tile2
    
    def draw_map(self, display):
        tile_rects = []
        x = -1
        y = -1
        for row in self.map:
            y += 1
            for element in row:
                x += 1
                if element == "1":
                    display.blit(self.tile1, (x * 16 , y * 16))
                if element == "2":
                    display.blit(self.tile2, (x * 16 , y * 16))
                if element != "0":
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))
            x = -1
        return tile_rects
        
                

