import pygame
import math
import Assets.Scripts.framework as engine

pygame.init()
clock = pygame.time.Clock()
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
display = pygame.Surface((screen_width//2, screen_height//2))

def level_1():
    run = True
    #Stone
    stones = []
    #Mouse Input
    click = False
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if stones != []:
            for s, stone in sorted(enumerate(stones), reverse=True):
                stone.move()
                stone.draw(display)
                if not stone.alive:
                    stones.pop(s)
        #Shooting mechanism
        if click:
            #Getting the mouse position
            mx , my = pygame.mouse.get_pos()
            mx = mx/2
            my = my/2
            m_pos = []
            m_pos.append(mx)
            m_pos.append(my)
            #Getting the 3rd vertex of the triangle
            point = (m_pos[0], player.get_rect().y)
            #Calculating distance between the points
            l1 = math.sqrt(math.pow((point[1] - player.get_rect().y), 2) + math.pow((point[0] - player.get_rect().x + 16), 2))
            l2 = math.sqrt(math.pow((m_pos[1] - point[1]),2) + math.pow((m_pos[0] - point[0]),2))
            #Calculating the angle between them
            angle = math.atan2(l2,l1)
            angle = math.degrees(angle)
            #Creating stone object
            stones.append(engine.Projectile(screen_width, screen_height, [player.get_rect().x + 16, player.get_rect().y], 4, 4, 15, player.get_rect(), m_pos, angle))
            click = not click
        #Movement of the player 
        player.move(tile_rects, time)
        #Blitting the player
        player.draw(display)
        #Blitting the display
        surf = pygame.transform.scale(display,(screen_width, screen_height))
        screen.blit(surf,(0,0))
        pygame.display.update()

level_1()