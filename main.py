import pygame 
import math
import random
import Assets.Scripts.framework as engine
pygame.init()
#Display settings 
screen_w = 1000
screen_h = 600
window = pygame.display.set_mode((screen_w,screen_h))
display = pygame.Surface((screen_w//2, screen_h//2))
pygame.display.set_caption("Vampy")

def draw_health_bar(health, x, y):
	ratio = health / 100
	pygame.draw.rect(display, (255,255,255), (x - 2, y - 2, 204  , 34//2))
	pygame.draw.rect(display, (255,0,0), (x, y, 200  , 30//2))
	pygame.draw.rect(display, (255,255,0), (x, y, 200 * ratio , 30//2))

def game_loop():
    #Game Variables
    run = True
    clock = pygame.time.Clock()
    #Loading images
    tile1 = pygame.image.load("Assets/Tiles/tile1.png").convert_alpha()
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
    #Vampire settings
    vamp_spawn_loc = []
    vamp_spawn_cooldown = 15000
    vamp_spawn_last_update = 0 
    vampires = []
    #Main Game Loop
    while run:
        clock.tick(60)
        time = pygame.time.get_ticks()
        display.fill((0,0,0))
        #Map Blitting
        tiles, vamp_spawn_loc = map.blit_map(display, scroll)
        #Calculating Scroll
        true_scroll[0] += (player.get_rect().x - true_scroll[0] - 262) / 20
        true_scroll[1] += (player.get_rect().y - true_scroll[1] - 162) / 20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
        #Creating vampires
        if time - vamp_spawn_last_update > vamp_spawn_cooldown:
            for loc in vamp_spawn_loc:
                vampires.append(engine.Vampires(loc,0,random.randint(1500,4000)))
            vamp_spawn_last_update = time
        #Moving and blitting Vampires
        for v, vamp in sorted(enumerate(vampires), reverse=True):
            vamp.move([player.get_rect().x - scroll[0], player.get_rect().y - scroll[1]], time, display, scroll, player)
            vamp.draw(display, scroll)
            if not vamp.alive:
                vampires.pop(v)
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
            #Creating moon_bullets object
            moon_bullets.append(engine.Projectile(screen_w, screen_h, [player.get_rect().x - scroll[0], player.get_rect().y - scroll[1]], 4, 4,15, pygame.rect.Rect(player.get_rect().x - scroll[0], player.get_rect().y-scroll[1], 16,16), m_pos, angle))
            click = not click
        #Check for collision
        for moon in moon_bullets:
            for vamp in vampires:
                vamp_x = vamp.get_rect().x
                vamp_y = vamp.get_rect().y
                vamp.get_rect().y -= scroll[1]
                vamp.get_rect().x -= scroll[0]
                if moon.get_rect().colliderect(vamp.get_rect()):
                    vamp.alive = False
                vamp.get_rect().x = vamp_x
                vamp.get_rect().y = vamp_y
        #Printing the health bar
        draw_health_bar(player.life,10,10)
        #Player Blitting
        if player.life > 0:
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