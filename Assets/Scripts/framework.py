import pygame

class Player():
    def __init__(self, loc, width, height ) -> None:
        self.rect = pygame.rect.Rect(loc[0], loc[1], width, height)
        self.speed = 5
        self.gravity = 9.81
    def move(self):
        self.rect.y += self.gravity
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speed
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
            x = -1
        
                

