import pygame
import random
#0 -> Normal 
#1 -> Windy
#Direction
#0 -> Right
#1 -> Left
class weather():
    def __init__(self, screen_w, screen_h):
        self.weather = 0
        self.direction = 0
        self.particles = []
        self.particle_generation_last_update = 0
        self.particle_generation_cooldown = 200
        self.screen_w = screen_w
        self.screen_h = screen_h

    def change_weather(self):
        self.weather = random.randint(0,1)
        if self.weather == 1:
            self.direction = random.radnint(0,1)

    def create_particles(self):
        self.particles.append(particles(random.randint(0,self.screen_w), 0, self))


    def chain_call(self, time, display):
        if time - self.particle_generation_last_update > self.particle_generation_cooldown:
            self.create_particles()
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
                    
            self.particle_generation_last_update = time
    
    def return_weather(self):
        return self.weather
    
    def return_direction(self):
        return self.direction
        

class particles():
    def __init__(self, x , y, weather):
        self.x = x 
        self.y = y 
        self.alive = True
        self.weather = weather.return_weather()
        self.direction = weather.return_direction()
        self.gravity = 9.81
        self.speed = 5
    
    def blit_particles(self, display):
        print(self.x)
        print(self.y)
        pygame.draw.circle(display, (255,0,0), (self.x, self.y), 2)
    
    def move_particles(self):
        self.y += self.gravity
        if self.weather == 1:
            if self.direction == 0:
                self.x += self.speed
            if self.direction == 1:
                self.x -= self.speed
        



