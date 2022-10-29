import pygame
import math
class Player():
    def __init__(self, rect_size):
        self.rect = pygame.rect.Rect(50,50,rect_size[0], rect_size[1])
        self.display_x = 0
        self.display_y = 0 
        self.life = 100
        self.speed = 5
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def draw(self, window, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x = self.rect.x - scroll[0]
        self.rect.y = self.rect.y - scroll[1]
        pygame.draw.rect(window, (255,255,0), self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y

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
    
    def move(self, tiles):
        self.movement = [0,0]
        if self.moving_right:
            self.movement[0] += self.speed
            self.moving_right = not self.moving_right
        if self.moving_left:
            self.movement[0] -= self.speed
            self.moving_left = not self.moving_left
        if self.moving_up:
            self.movement[1] -= self.speed
            self.moving_up = not self.moving_up
        if self.moving_down:
            self.movement[1] += self.speed
            self.moving_down = not self.moving_down

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.moving_up = True
        if keys[pygame.K_s]:
            self.moving_down = True
        if keys[pygame.K_a]:
            self.moving_left = True
        if keys[pygame.K_d]:
            self.moving_right = True
        collision_type = self.collision_checker(tiles)

    def get_rect(self):
        return self.rect

class Vampires():
    def __init__(self, spawn_loc, vampire_move_cooldown, vamp_spit_cooldown) -> None:
        self.rect = pygame.rect.Rect(spawn_loc[0], spawn_loc[1], 32, 32)
        self.vampire_move_cooldown = vampire_move_cooldown
        self.vampire_move_last_update = 0
        self.display_x = 0
        self.display_y = 0
        self.alive = True
        self.vamp_spit_cooldown = vamp_spit_cooldown
        self.vamp_spit_last_update = 0 
        self.speed = 2
        self.angle = 0
        self.spit = []
        
    def move(self, player_loc, time, display, scroll, player):
        point = [player_loc[0], self.rect.y - scroll[1]]
        l1 = math.sqrt(math.pow((point[0] - player_loc[0]), 2) + math.pow((point[1] - player_loc[1]), 2))
        l2 = math.sqrt(math.pow((point[1] - (self.rect.y - scroll[1])),2) + math.pow((point[0] - (self.rect.x - scroll[0])),2))
        angle = math.atan2(l1,l2)
        angle = math.degrees(angle)
        if self.rect.y - scroll[1] > player_loc[1]:
            #The vampire is bottom of the player 
            if self.rect.x - scroll[0] > player_loc[0]:
                #The vampire is to the right 
                angle = 180 - angle
        else:
            #The vampire is top of the player 
            if self.rect.x - scroll[0] > player_loc[0]:
                #The vampire is to the top right 
                angle = 180 + angle
            else:
                    #The vampire is to the top left
                angle = 360 - angle
        self.rect.x += math.cos(math.radians(angle)) * self.speed
        self.rect.y -= math.sin(math.radians(angle)) * self.speed
        self.angle = angle
        if time - self.vamp_spit_last_update > self.vamp_spit_cooldown:
            #Spit
            self.spit.append(VampireSpit(1000,600,3,3,5,[self.rect.x - scroll[0], self.rect.y - scroll[1]], self.angle))
            self.vamp_spit_last_update = time
        if self.spit != []:
            player_x = player.get_rect().x
            player_y = player.get_rect().y
            player.get_rect().x -= scroll[0]
            player.get_rect().y -= scroll[1]
            for s, spi in sorted(enumerate(self.spit), reverse=True):
                spi.move()
                spi.draw(display)
                if spi.get_rect().colliderect(player.get_rect()):
                    player.life -= 5
                if not spi.alive:
                    self.spit.pop(s)
            player.get_rect().x = player_x
            player.get_rect().y = player_y

    def draw(self, display, scroll):
        if self.alive:
            self.display_x = self.rect.x
            self.display_y = self.rect.y
            self.rect.x = self.rect.x - scroll[0]
            self.rect.y = self.rect.y - scroll[1]
            pygame.draw.rect(display, (255,0,0), self.rect)
            self.rect.x = self.display_x
            self.rect.y = self.display_y
        else:
            del self

    def get_rect(self):
        return self.rect
    
    def get_angle(self):
        return self.angle

#Map 
class Map():
    def __init__(self, map_loc, tile1):
        self.map = [] 
        self.tile1 = tile1
        #Day Night Converter
        self.tile1.set_alpha(255)
        f = open(map_loc, "r")
        data = f.read()
        f.close()
        data = data.split("\n")
        for row in data:
            self.map.append(list(row))
    
    def blit_map(self, window, scroll):
        tile_rects = []
        vamp_spawn_loc = []
        x = 0
        y = 0 
        for row in self.map:
            x = 0 
            for element in row:
                if element == "1":
                    window.blit(self.tile1, (x * 16 - scroll[0], y * 16 - scroll[1]) )
                if element == "v":
                    vamp_spawn_loc.append(list((x*16,y*16)))
                if element != "1":
                    tile_rects.append(pygame.rect.Rect(x*16, y*16, 16,16))
                x += 1
            y += 1
        return tile_rects, vamp_spawn_loc
#Projectiles
class Projectile():
    def __init__(self, s_width, s_height, pos, width, height, speed, player_rect, m_pos, angle) -> None:
        self.s_width = s_width
        self.s_height = s_height
        self.rect = pygame.rect.Rect(pos[0], pos[1], width, height)
        self.speed = speed
        self.alive = True
        self.player_rect = player_rect
        self.m_pos = m_pos
        self.angle = angle
        if self.player_rect.y > self.m_pos[1]:
            if self.player_rect.x > self.m_pos[0]:
                self.angle = 180 - self.angle
        else:
            if self.player_rect.x > self.m_pos[0]:
                self.angle = 180 + self.angle
            else:
                self.angle = 270 + (90 - self.angle)
    def move(self):
        if self.rect.x < 0 or self.rect.x > self.s_width or self.rect.y < 0 or self.rect.y > self.s_height:
            self.alive = False
        self.rect.x += math.cos(math.radians(self.angle)) * self.speed
        self.rect.y -= math.sin(math.radians(self.angle)) * self.speed
    
    def get_rect(self):
        return self.rect

    def draw(self, display):
        pygame.draw.rect(display, (0,0,255), self.rect)

class VampireSpit():
    def __init__(self, screen_w, screen_h, width, height, speed, start_pos, angle) -> None:
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.rect = pygame.rect.Rect(start_pos[0], start_pos[1], width, height)
        self.speed = speed
        self.start_pos  = start_pos
        self.angle = angle
        self.alive = True

    def move(self):
        if self.rect.x < 0 or self.rect.x > self.screen_w or self.rect.y > self.screen_h or self.rect.y < 0:
            self.alive = False
        self.rect.x += math.cos(math.radians(self.angle)) * self.speed
        self.rect.y -= math.sin(math.radians(self.angle)) * self.speed
        
    def draw(self, display):
        pygame.draw.rect(display,(255,0,0), self.rect)
    
    def get_rect(self):
        return self.rect
