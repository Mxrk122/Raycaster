BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
import pygame

SKY = (25, 25, 25)

map_colors = [
    (6, 201, 223),
    (241, 80, 37),
    (25, 25, 25),
    (255, 210, 63),
    (255, 255, 255)
]

# textura de paredes
wall1 = pygame.image.load("./textures/dum/ROCKRED1.png")
wall2 = pygame.image.load("./textures/dum/ROCKRED3.png")
wall3 = pygame.image.load("./textures/slayer2.png")
wall4 = pygame.image.load("./textures/mcr.png")

#enemies
demon1 = pygame.image.load("./textures/demon1/sp1.png")
demon2 = pygame.image.load("./textures/demon1/sp2.png")
demon3 = pygame.image.load("./textures/demon1/sp3.png")

map_textures = {
    '1': wall1,
    '0': wall2,
    '3': wall3,
    '2': wall4,
}

demon_textures = [
    demon1,
    demon2,
    demon3
]