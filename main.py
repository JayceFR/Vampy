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

def draw_text(text, font, text_col, x, y, display):
    img = font.render(text, True, text_col)
    display.blit(img, (x, y))

def game_loop():
    #Game Variables
    run = True
    clock = pygame.time.Clock()
    num_of_nights_survived = 0 
    game_launch = 0 
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
    #Sparks
    sparks = []
    #Fonts
    font = pygame.font.Font("Assets/Fonts/jayce.ttf", 30)
    font2 = pygame.font.Font("Assets/Fonts/jayce.ttf", 15)
    font3 = pygame.font.Font("Assets/Fonts/jayce.ttf", 50)
    #Texts
    text1 = "Dodge The Blood Spit By The Vampires"
    text2 = "The Blood Is Lethal. Enough Blood Can Turn You Into One Of Them!"
    text3 = "W-A-S-D or Arrow keys for movement"
    text4 = "Left Click to shoot And Kill The Vampires."
    text5 = "Wow! You have survived the night!"
    text6 = "Collect The Correct Random Flower to Gain Health"
    #Music
    shoot_sound = pygame.mixer.Sound("Assets/Music/Shoot.wav")
    shoot_sound.set_volume(0.5)
    vampire_death_sound = pygame.mixer.Sound("Assets/Music/vampire_death_song.wav")
    vampire_death_sound.set_volume(0.5)
    flower_pickup = pygame.mixer.Sound("Assets/Music/flower.wav")
    flower_pickup.set_volume(0.5)
    pygame.mixer.music.load("Assets/Music/Vampy_Theme_Music.wav")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)
    #After death variables 
    after_death = 0 
    j_boy = pygame.image.load("Assets/Sprites/J_Boy.png").convert_alpha()
    j_boy.set_colorkey((255,255,255))
    j_boy_vamp = pygame.image.load("Assets/Sprites/J_Vamp_Boy.png").convert_alpha()
    j_boy_vamp.set_colorkey((255,255,255))
    j_boy_skin = [j_boy, j_boy_vamp]
    skin = 0 
    scale_size = 1
    scale_last_update = 0
    scale_cooldown = 1000
    death_j_boy_cooldown = 4000
    death_display_x = 250
    death_display_y = 150
    death_j_boy_last_update = 0
    change_to_vamp = 0
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
            if player.life > 0:
                if time - day_to_night_last_update > night_cooldown:
                    num_of_nights_survived += 1
                    change_to_day = 0
                    day_to_night_last_update = time
                    day = True
                text = "TIME LEFT FOR DAY: " + str(((day_cooldown + day_to_night_last_update) - time)//1000)
                draw_text(text, font, (255,255,255), 10, 250, display)
            if game_launch == 0:
                if time - day_to_night_last_update < 9000:
                    draw_text(text1, font2, (255,0,0), 130,80, display)
                    draw_text(text2, font2, (255,0,0), 60, 100, display)
                    draw_text(text3, font2, (255,0,255), 130, 120, display)
                    draw_text(text4, font2, (255,0,255), 125, 140, display)
                else:
                    game_launch = 1
            #Creating vampires
            if time - vamp_spawn_last_update > vamp_spawn_cooldown:
                for loc in vamp_spawn_loc:
                    vampires.append(engine.Vampires(loc,0,random.randint(1500,4000), vampire_run_animation))
                vamp_spawn_last_update = time
            #Moving and blitting Vampires
            if player.life > 0:
                for v, vamp in sorted(enumerate(vampires), reverse=True):
                    vamp.move([player.get_rect().x - scroll[0], player.get_rect().y - scroll[1]], time, display, scroll, player)
                    vamp.draw(display, scroll, time)
                    if not vamp.alive:
                        #Spark effect on vampires
                        for x in range(20):
                            sparks.append(engine.Spark([vamp.get_rect().x - scroll[0], vamp.get_rect().y - scroll[1]],math.radians(random.randint(0, 360)), random.randint(2, 4),
                                                            (64, 12, 92), 1, 2))
                        #Deleting vamp from list
                        vampire_death_sound.play()
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
                if player.life > 0:
                    shoot_sound.play()
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
            if player.life > 0:
                if time - day_to_night_last_update > day_cooldown:
                    day_to_night_last_update = time
                    vampires.clear()
                    day = False
                text = "TIME LEFT FOR NIGHT: " + str(((day_cooldown + day_to_night_last_update) - time)//1000)
                draw_text(text, font, (255,0,0), 10, 250, display)
            if game_launch == 1:
                if time - day_to_night_last_update < 9000:
                    draw_text(text5, font2, (0,0,255), 130, 80, display)
                    draw_text(text6, font2, (0,0,255), 100, 100, display)
                else:
                    game_launch = 2
            #Creting flowers
            if change_to_day == 0:
                flowers = create_flowers(flower_images)
                correct_variety = get_correct_variety()
                change_to_day = -1
            if player.life > 0:
                for f, flower in sorted(enumerate(flowers), reverse= True):
                    flower.draw(display, scroll)
                    if flower.get_rect().colliderect(player.get_rect()):
                        flower_pickup.play()
                        if flower.variety == correct_variety:
                            if player.life + 5 > 100:
                                player.life = 100
                            else:
                                player.life += 5
                        else:
                            player.life -= 10
                        #Creating sparks
                        if flower.variety == 0:
                            sparks.append(engine.Spark([flower.get_rect().x - scroll[0], flower.get_rect().y - scroll[1]],math.radians(random.randint(0, 360)), random.randint(2, 4),
                                                            (64, 12, 92), 1, 2))
                        if flower.variety == 1:
                            sparks.append(engine.Spark([flower.get_rect().x - scroll[0], flower.get_rect().y - scroll[1]],math.radians(random.randint(0, 360)), random.randint(2, 4),
                                                            (64, 12, 92), 1, 2))
                        if flower.variety == 2:
                            sparks.append(engine.Spark([flower.get_rect().x - scroll[0], flower.get_rect().y - scroll[1]],math.radians(random.randint(0, 360)), random.randint(2, 4),
                                                            (64, 12, 92), 1, 2))
                        if flower.variety == 3:
                            sparks.append(engine.Spark([flower.get_rect().x - scroll[0], flower.get_rect().y - scroll[1]],math.radians(random.randint(0, 360)), random.randint(2, 4),
                                                            (64, 12, 92), 1, 2))
                        flowers.pop(f)
        #Printing the health bar
        draw_health_bar(player.life,10,10)
        nights_survived = "NIGHTS SURVIVED: " + str(num_of_nights_survived)
        draw_text(nights_survived, font, (180,0,0), 240, 0, display)
        #Sparks Blitting
        if sparks != []:
            for i, spark in sorted(enumerate(sparks), reverse=True):
                spark.move(1)
                spark.draw(display)
                if not spark.alive:
                    sparks.pop(i)
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
        if player.life <= 0:
            if after_death == 0:
                death_j_boy_last_update = time
                scale_last_update = time
                after_death = -1

            if time - death_j_boy_last_update < death_j_boy_cooldown:
                display_j = j_boy_skin[skin].copy()
                display_j = pygame.transform.scale(display_j, (display_j.get_width() * scale_size, display_j.get_height() * scale_size))
                display.blit(display_j, (death_display_x, death_display_y))
                if change_to_vamp == 0:
                    if time - scale_last_update > scale_cooldown:
                        scale_size += 0.5
                        scale_last_update = time
            else:
                if change_to_vamp == 0:
                    death_j_boy_last_update = time
                    skin = 1
                    death_display_x -= 10
                    change_to_vamp = -1
                else:
                    display.fill((0,0,0))
                    draw_text("VAMPY", font3, (64,12,94), 180, 20, display)
                    draw_text("GAME OVER", font3, (255,0,0), 130,80, display )
                    draw_text("A Game By JayceFR (jayjan)", font, (255,255,255), 70, 140, display )
                    draw_text("Art And Music : Janish Jason", font, (0,0,255), 70, 170,display )
                    draw_text("A Game Created Within 3 Days ", font, (0,255,0), 55, 250, display )
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player.life > 0:
                        click = True
        surf = pygame.transform.scale(display, (screen_w, screen_h))
        window.blit(surf, (0, 0))
        pygame.display.update()

game_loop()