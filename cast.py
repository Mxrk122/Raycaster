import pygame
from color import *
from math import *
from enemy import *

class Raycaster(object):
    def __init__(self, screen):
        _, _, self.width, self.height = screen.get_rect()
        self.screen = screen
        self.blocksize = 50
        self.player = {
            "x": self.blocksize + 10,
            "y": self.blocksize + 10,
            "angle": pi/2.2,
            "fov": pi/3
        }
        self.map = []
        self.clearZ()
        self.clear(BLACK)

        self.enemies = [
            Enemy(90, 90, demon_textures[1]),
            Enemy(400, 100, demon_textures[0]),
            Enemy(300, 250, demon_textures[2])
        ]
        

    def clear(self, bg_color):
        for x in range(self.width):
            for y in range(self.height):
                r = int((x/self.width)*255) if x/self.width < 1 else 1
                g = int((y/self.height)*255) if y/self.height < 1 else 1
                b = 0
                color = (r, g, b)
                self.point(x, y, bg_color)
    
    def clearZ(self):
        self.zbuffer = [99999 for z in range(0, 500)]

    def point(self, x, y, c = WHITE):
        self.screen.set_at((x, y), c)

    def draw_rectangle(self, x, y, c = WHITE, wall = None):
        for cx in range(x, x + self.blocksize + 1):
            for cy in range(y, y + self.blocksize + 1):
                if wall:
                    tx = int((cx - x) * 128 / self.blocksize)
                    ty = int((cy - y) * 128 / self.blocksize)
                    c = wall.get_at((tx, ty))
                else:
                    c = c
                self.point(cx, cy, c)

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))
    
    def draw_object(self, object):
        sprite_x = 500
        sprite_y = 0
        sprite_size = 128

        # distancia del jugador
        sprite_a = atan2(object.y - self.player["y"],
        object.x - self.player["x"])

        sprite_d = ((self.player["x"] - object.x)**2 + (self.player["y"] - object.y)**2)**0.5
        sprite_size = (500/sprite_d) * self.height/10

        sprite_x = 500 + (sprite_a - self.player["angle"]) * 500/self.player["fov"] + 250 - sprite_size/2
        sprite_y = 250 - sprite_size/2

        sprite_x = int(sprite_x)
        sprite_y = int(sprite_y)
        sprite_size = int(sprite_size)

        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                tx = int((x - sprite_x) * 128/sprite_size)
                ty = int((y - sprite_y) * 128/sprite_size)
                c = object.sprite.get_at((tx, ty))
                #quitar fondo
                if c != (0, 0, 0, 0):
                    if x > 500 and x < 1000:
                        if self.zbuffer[x - 500] >= sprite_d:
                            self.point(x, y, c)
                            self.zbuffer[x - 500] = sprite_d

    def draw_player(self):
        self.point(self.player["x"], self.player["y"], (255, 255, 255))
    
    def draw_enemies(self):
        for enemy in self.enemies:
            self.point(enemy.x, enemy.y, RED)

        for enemy in self.enemies:
            self.draw_object(enemy)

    def cast_ray(self, a):
        d = 0
        while True:
            x = self.player["x"] + d*cos(a)
            y = self.player["y"] + d*sin(a)
            x = int(x)
            y = int(y)

            i = int(x/50)
            j = int(y/50)

            if self.map[j][i] != ' ':
                hitx = x - i * self.blocksize
                hity = y - j * self.blocksize

                if 1 < hitx < self.blocksize - 1:
                    maxhit = hitx
                else:
                    maxhit = hity
                
                tx = int(maxhit * 128 / self.blocksize)
                # el rayo golpea
                return d, self.map[j][i], tx

            self.point(x, y, (255, 255, 255))

            d += 1

    def draw_stake(self, x, h, c, tx, texture = None):
        # draw a stake with x, y at the middle
        start_y = int(((500 / 2) - (h / 2)))
        end_y = int(((500 / 2) + (h / 2)))
        height = end_y - start_y

        for y in range(start_y, end_y):

            if texture:
                ty = int((y - start_y) * 128 / height)
                c = texture.get_at((tx, ty)) 
                self.point(x, y, c)
            else:
                self.point(x, y, c)
    
    def draw_map(self):
        for x in range(0, 500, 50):
            for y in range(0, 500, 50):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                if self.map[j][i] != ' ':
                    try:
                        block_color = int(self.map[j][i])
                    except:
                        block_color = 4
                    
                    #modo textura -> si enecuntra una textura en diccionario
                    try:
                        self.draw_rectangle(x, y, map_colors[block_color], map_textures[self.map[j][i]])
                    except:
                        self.draw_rectangle(x, y, map_colors[block_color])
    
    def draw_minimap(self):
        for x in range(0, 500, 50):
            for y in range(0, 500, 50):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                if self.map[j][i] != ' ':
                    try:
                        block_color = int(self.map[j][i])
                    except:
                        block_color = 4
                    
                    #modo textura -> si enecuntra una textura en diccionario
                    try:
                        self.draw_rectangle(x, y, map_colors[block_color], map_textures[self.map[j][i]])
                    except:
                        self.draw_rectangle(x, y, map_colors[block_color])
    
    def threedimensions_brah(self):
        # 3d
        screen_width = int(self.width/2)
        for i in range(0, screen_width):
            a =  self.player["angle"] - self.player["fov"]/2 + self.player["fov"]*i/screen_width
            d, color, tx = self.cast_ray(a)

            x = int(self.width/2) + i
            h = (self.height/(d * cos(a - self.player["angle"]))) * self.height/10
            
            if self.zbuffer[i] >= d:
                #modo textura -> si enecuntra una textura en diccionario
                try:
                    texture = map_textures[color]
                    self.draw_stake(x, h, color, tx, texture)
                except:
                    self.draw_stake(x, h, map_colors[int(color)], tx)
                self.zbuffer[i] = d

        
    def render(self):
        self.draw_map()
        self.draw_player()
        

        density = 100
        # Campo de vision -> minimapa
        for i in range(0, density):
            a =  self.player["angle"] - self.player["fov"]/2 + self.player["fov"]*i/density
            self.cast_ray(a)
        
        
        for i in range(0, 500):
            self.point(500, i, BLUE)
            self.point(501, i, BLUE)
            self.point(499, i, BLUE)

        # 3d
        self.threedimensions_brah()
        self.draw_enemies()
        

        
    