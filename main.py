import pygame
import Assets.Scripts.framework as engine

pygame.init()
clock = pygame.time.Clock()
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
display = pygame.Surface((screen_width//2, screen_height//2))

def level_1():
    run = True
    #Tiles
    tile1 = pygame.image.load("Assets/Tiles/grass.png").convert()
    tile2 = pygame.image.load("Assets/Tiles/dirt2.png").convert()
    tile3 = pygame.image.load("Assets/Tiles/dirt1.png").convert()
    #Map
    map = engine.Map("Assets/Maps/map1.txt", tile1, tile2)
    #Player 
    player = engine.Player([50,50], 16,16)
    while run:
        time = pygame.time.get_ticks()
        clock.tick(60)
        display.fill((0,0,0))
        #Map
        tile_rects = map.draw_map(display)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #Movement of the player 
        player.move(tile_rects, time)
        #Blitting the player
        player.draw(display)
        #Blitting the display
        surf = pygame.transform.scale(display,(screen_width, screen_height))
        screen.blit(surf,(0,0))
        pygame.display.update()

level_1()