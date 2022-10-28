import pygame 
import math
import Assets.Scripts.framework as engine
pygame.init()
#Display settings 
screen_w = 1000
screen_h = 600
window = pygame.display.set_mode((screen_w,screen_h))
display = pygame.Surface((screen_w//2, screen_h//2))
pygame.display.set_caption("Vampy")

def game_loop():
    #Game Variables
    run = True
    clock = pygame.time.Clock()
    #Loading images
    tile1 = pygame.image.load("Assets/Tiles/tile1.png")
    #Loading the map 
    map = engine.Map("Assets/Maps/map.txt", tile1)
    #Player 
    player = engine.Player([16,16])
    true_scroll = [0,0]
    scroll = [0,0]
    #Moon Bullets
    moon_bullets = []
    #Mouse Settings
    click = False

    #Main Game Loop
    while run:
        clock.tick(60)
        display.fill((0,0,0))
        #Map Blitting
        tiles = map.blit_map(display, scroll)
        #Calculating Scroll
        true_scroll[0] += (player.get_rect().x - true_scroll[0] - 262) / 20
        true_scroll[1] += (player.get_rect().y - true_scroll[1] - 162) / 20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
        #Bliitng the moon bullets
        if moon_bullets != []:
            for s, moon in sorted(enumerate(moon_bullets), reverse=True):
                moon.move()
                moon.draw(display)
                if not moon.alive:
                    moon_bullets.pop(s)       
        #Shooting mechanics
        if click:
            #Getting the mouse position
            mx , my = pygame.mouse.get_pos()
            mx = mx/2
            my = my/2
            m_pos = []
            m_pos.append(mx)
            m_pos.append(my)
            #Getting the 3rd vertex of the triangle
            point = (m_pos[0], player.get_rect().y - scroll[1])
            #Calculating distance between the points
            l1 = math.sqrt(math.pow((point[1] - (player.get_rect().y - scroll[1])), 2) + math.pow((point[0] - (player.get_rect().x - scroll[0])), 2))
            l2 = math.sqrt(math.pow((m_pos[1] - point[1]),2) + math.pow((m_pos[0] - point[0]),2))
            #Calculating the angle between them
            angle = math.atan2(l2,l1)
            angle = math.degrees(angle)
            #Creating stone object
            moon_bullets.append(engine.Projectile(screen_w, screen_h, [player.get_rect().x - scroll[0], player.get_rect().y - scroll[1]], 4, 4, 15, pygame.rect.Rect(player.get_rect().x - scroll[0], player.get_rect().y-scroll[1], 16,16), m_pos, angle))
            click = not click
        #Player Blitting
        player.move(tiles)
        player.draw(display, scroll)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        surf = pygame.transform.scale(display, (screen_w, screen_h))
        window.blit(surf, (0, 0))
        pygame.display.update()

game_loop()