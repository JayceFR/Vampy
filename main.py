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

def create_flowers(flower_images):
    flowers = []
    for x in range(50):
        flowers.append(engine.Flowers([random.randint(580,2400)/2, random.randint(500,1190)/2], random.randint(0,3), flower_images))
    return flowers

def get_correct_variety():
    return random.randint(0,3)

def get_image(sheet, frame, width, height, scale):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey((255, 255, 255))
    return image

def game_loop():
    #Game Variables
    run = True
    clock = pygame.time.Clock()
    #Loading images
    tile1 = pygame.image.load("Assets/Tiles/tile1.png").convert_alpha()
    tile2 = pygame.image.load("Assets/Tiles/tile2.png").convert_alpha()
    #Loading the map 
    map = engine.Map("Assets/Maps/map.txt", tile1, tile2)
    #Player animation loading 
    player_idle_spritesheet = pygame.image.load("Assets/Sprites/player_idle.png").convert_alpha()
    player_idle_animation = []
    for x in range(4):
        player_idle_animation.append(get_image(player_idle_spritesheet,x,32,32,1.5))
    player_run_spritesheet = pygame.image.load("Assets/Sprites/player_run.png").convert_alpha()
    player_run_animation = []
    for x in range(6):
        player_run_animation.append(get_image(player_run_spritesheet, x, 32, 32, 1.5))
    player = engine.Player([32,32], player_idle_animation, player_run_animation)
    true_scroll = [0,0]
    scroll = [0,0]
    #Flowers 
    blue_flower = pygame.image.load("Assets/Sprites/blue_flower.png").convert_alpha()
    blue_flower = pygame.transform.scale(blue_flower, (32,32))
    blue_flower.set_colorkey((255,255,255))
    orange_flower = pygame.image.load("Assets/Sprites/orange_flower.png").convert_alpha()
    orange_flower = pygame.transform.scale(orange_flower, (32,32))
    orange_flower.set_colorkey((255,255,255))
    pink_flower = pygame.image.load("Assets/Sprites/pink_flower.png").convert_alpha()
    pink_flower = pygame.transform.scale(pink_flower, (32,32))
    pink_flower.set_colorkey((255,255,255))
    yellow_flower = pygame.image.load("Assets/Sprites/yellow_flower.png").convert_alpha()
    yellow_flower = pygame.transform.scale(yellow_flower, (32,32))
    yellow_flower.set_colorkey((255,255,255))
    flower_images = [orange_flower, yellow_flower, pink_flower, blue_flower]
    flowers = create_flowers(flower_images)
    #gun 
    gun = pygame.image.load("Assets/Sprites/gun.png").convert_alpha()
    gun.set_colorkey((255,255,255))
    bullet = pygame.image.load("Assets/Sprites/bullet.png").convert_alpha()
    bullet.set_colorkey((255,255,255))
    #Moon Bullets
    moon_bullets = []
    #Mouse Settings
    click = False
    #Vampire settings
    vamp_spawn_loc = []
    vamp_spawn_cooldown = 10000
    vamp_spawn_last_update = 0 
    vampires = []
    vampire_animation_spritesheet = pygame.image.load("Assets/Sprites/vampire_run.png").convert_alpha()
    vampire_run_animation = []
    for x in range(6):
        vampire_run_animation.append(get_image(vampire_animation_spritesheet,x,32,32,1.5))
    #day and night 
    day = False
    day_cooldown = 20000
    night_cooldown = 20000
    day_to_night_last_update = 0
    change_to_day = 0 
    #Main Game Loop
    while run:
        clock.tick(60)
        time = pygame.time.get_ticks()
        display.fill((0,0,0))
        #Map Blitting
        tiles, vamp_spawn_loc = map.blit_map(display, scroll, day)
        #Calculating Scroll
        true_scroll[0] += (player.get_rect().x - true_scroll[0] - 262) / 20
        true_scroll[1] += (player.get_rect().y - true_scroll[1] - 162) / 20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
             
        if not day:
            #Switchinbg the day load
            if time - day_to_night_last_update > night_cooldown:
                change_to_day = 0
                day_to_night_last_update = time
                day = True
            #Creating vampires
            if time - vamp_spawn_last_update > vamp_spawn_cooldown:
                for loc in vamp_spawn_loc:
                    vampires.append(engine.Vampires(loc,0,random.randint(1500,4000), vampire_run_animation))
                vamp_spawn_last_update = time
            #Moving and blitting Vampires
            for v, vamp in sorted(enumerate(vampires), reverse=True):
                vamp.move([player.get_rect().x - scroll[0], player.get_rect().y - scroll[1]], time, display, scroll, player)
                vamp.draw(display, scroll, time)
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
            #Getting the mouse position
            mx , my = pygame.mouse.get_pos()
            mx = mx/2
            my = my/2
            m_pos = []
            m_pos.append(mx)
            m_pos.append(my)
            #Getting the 3rd vertex of the triangle
            point = (m_pos[0], player.get_rect().y + 36 - scroll[1])
            #Calculating distance between the points
            l1 = math.sqrt(math.pow((point[1] - (player.get_rect().y + 36 - scroll[1])), 2) + math.pow((point[0] - (player.get_rect().x + 28 - scroll[0])), 2))
            l2 = math.sqrt(math.pow((m_pos[1] - point[1]),2) + math.pow((m_pos[0] - point[0]),2))
            #Calculating the angle between them
            angle = math.atan2(l2,l1)
            angle = math.degrees(angle)
            #pygame.draw.line(display,(255,0,0), m_pos, point)
            #pygame.draw.line(display, (255,0,255), point, ((player.get_rect().x + 28 - scroll[0]), (player.get_rect().y + 36 - scroll[1])))
            if click:
                #Creating moon_bullets object
                moon_bullets.append(engine.Projectile(screen_w, screen_h, [player.get_rect().x + 28 - scroll[0], player.get_rect().y + 36 - scroll[1]], 4, 4,15, pygame.rect.Rect(player.get_rect().x + 28 - scroll[0], player.get_rect().y + 36 -scroll[1], 16,16), m_pos, angle, bullet))
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
        if day:
            #Checking if it is night yet
            if time - day_to_night_last_update > day_cooldown:
                day_to_night_last_update = time
                vampires.clear()
                day = False
            #Creting flowers
            if change_to_day == 0:
                flowers = create_flowers(flower_images)
                correct_variety = get_correct_variety()
                change_to_day = -1
            for f, flower in sorted(enumerate(flowers), reverse= True):
                flower.draw(display, scroll)
                if flower.get_rect().colliderect(player.get_rect()):
                    if flower.variety == correct_variety:
                        if player.life + 5 > 100:
                            player.life = 100
                        else:
                            player.life += 5
                    else:
                        player.life -= 10
                    flowers.pop(f)
        #Printing the health bar
        draw_health_bar(player.life,10,10)
        #Player Blitting
        if player.life > 0:
            player.move(tiles)
            player.draw(display, scroll, time)
            #Gun Transformation 
            #if player.get_rect().y > m_pos[1]:
            #    if player.get_rect().x > m_pos[0]:
            #        angle = 180 - angle
            #else:
            #    if player.get_rect().x > m_pos[0]:
            #        angle = 180 + angle
            #    else:
            #        angle = 270 + (90 - angle)
            if not day:
                gun_angle = angle
                if my - (player.get_rect().y - scroll[1]) > 0:
                    gun_angle = 0 - gun_angle
                gun_copy = gun.copy()
                gun_copy = pygame.transform.rotate(gun_copy, gun_angle)
                if mx > player.get_rect().x - scroll[0]:
                    display.blit(gun_copy,((player.get_rect().x + 28 - scroll[0]) - gun_copy.get_width()/2, (player.get_rect().y + 36 - scroll[1]) - gun_copy.get_height()/2))
                else:
                    flip = gun_copy.copy()
                    flip = pygame.transform.flip(flip, True, False)
                    display.blit(flip,((player.get_rect().x + 28 - scroll[0]) - gun_copy.get_width()/2, (player.get_rect().y + 36 - scroll[1]) - gun_copy.get_height()/2))
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