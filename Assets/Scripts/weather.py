import pygame
import random
#0 -> Normal 
#1 -> Windy
#Direction
#0 -> Right
#1 -> Left
class weather():
    def __init__(self, screen_w, screen_h, particle_img):
        self.weather = 0
        self.direction = 0
        self.particle_img = particle_img
        self.particles = []
        self.particle_generation_last_update = 0
        self.particle_generation_cooldown = 200
        self.wind_change_last_update = 0 
        self.wind_change_cooldown = 10000
        self.screen_w = screen_w
        self.screen_h = screen_h

    def change_weather(self):
        self.weather = random.randint(0,1)
        if self.weather == 1:
            self.direction = random.randint(0,1)

    def create_particles(self):
        self.particles.append(particles(random.randint(0,self.screen_w*2)//2, 0, self.weather, self.direction, self.particle_img))


    def chain_call(self, time, display):
        if time - self.particle_generation_last_update > self.particle_generation_cooldown:
            self.create_particles()
            self.particle_generation_last_update = time
        if time - self.wind_change_last_update > self.wind_change_cooldown:
            self.change_weather()
            self.wind_change_last_update = time
        if self.particles != []:
            for pos, particle in sorted(enumerate(self.particles), reverse=True):
                particle.move_particles()
                particle.blit_particles(display)
                if particle.y > self.screen_h or particle.y < 0 :
                    self.alive = False
                if particle.x > self.screen_w or particle.x < 0:
                    self.alive = False
                if particle.alive == False:
                    self.particles.pop(pos)
    
    def return_weather(self):
        return self.weather
    
    def return_direction(self):
        return self.direction
        

class particles():
    def __init__(self, x , y, weather, direction, particle_img):
        self.x = x 
        self.y = y 
        self.alive = True
        self.weather = weather
        self.direction = direction
        self.image = particle_img
        self.rect = pygame.rect.Rect(x,y,self.image.get_width(), self.image.get_height())
        self.gravity = 5
        self.speed = 5
    
    def blit_particles(self, display):
        display.blit(self.image, self.rect)
    
    def move_particles(self):
        self.rect.y += self.gravity
        if self.weather == 1:
            if self.direction == 0:
                self.rect.x += self.speed
            if self.direction == 1:
                self.rect.x -= self.speed