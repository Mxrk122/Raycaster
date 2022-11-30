import pygame, sys, gui
import random
from cast import *

pygame.init()

screen = pygame.display.set_mode((1000, 500))
r = Raycaster(screen)


clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)
current_fps = font.render(str(clock.get_fps()), True, (0, 0, 0))
fps_title = font.render('FPS: ', True, (0, 0, 0))

# contador de fps
def update_fps(display):
  current_fps = font.render(str(clock.get_fps()), True, (0, 0, 0))

# sonido
menu_music = pygame.mixer.music.load('./textures/Death.wav', 'menu music')
step = pygame.mixer.Sound('./textures/step.wav')

# Funciones para cada pantalla
def main_menu():
  pygame.mixer.music.set_volume(0.3)
  pygame.mixer.music.play(-1)
  screen.fill(RED)
  title_font = pygame.font.SysFont("Arial", 60)
  subtitle_font = pygame.font.SysFont("Arial", 20)
  title = title_font.render('Bienvenido a DUN METALERO', True, (1, 1, 1))
  title_position = (160, 10)
  instructions = subtitle_font.render('Te mueves con AWSD, mueves la camara con el mouse o las teclas KJ', True, (1, 1, 1))
  while True:
    mouse_position = pygame.mouse.get_pos()
    screen.blit(title, title_position)
    screen.blit(instructions, (230, 90))

    level1_button = gui.Button((470, 400), "Nivel 1", gui.get_font(30), "#ffffff")
    level2_button = gui.Button((470, 300), "Nivel 2", gui.get_font(30), "#ffffff")
    level3_button = gui.Button((470, 200), "Nivel 3", gui.get_font(30), "#ffffff")

    for button in [level1_button, level2_button, level3_button]:
      button.font.render(button.text_input, True, button.color)
      button.reveal(screen)
    
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if level1_button.checkForInput(mouse_position):
          playing('./map1.txt')
        if level2_button.checkForInput(mouse_position):
          playing('./map2.txt')
        if level3_button.checkForInput(mouse_position):
          playing('./map3.txt')
      pygame.display.flip()


# Funcion apra jugar -> recibe como paarametro el mapa seleccionado
def playing(map):
  game_music = pygame.mixer.music.load('./textures/Warzone.wav', 'game music')
  pygame.mixer.music.play(-1)
  running = True
  screen.fill(BLACK)
  r.load_map(map)
  while running:
    
    screen.fill(BLACK, (0, 0, r.width/2, r.height))
    screen.fill(SKY, (r.width/2, 0, r.width, r.height/2))
    screen.fill(BLACK, (r.width/2, r.height/2, r.width, r.height/2))
    
    update_fps(screen)

    r.clearZ()

    r.render()

    for event in pygame.event.get():
      if (event.type == pygame.QUIT):
          running = False
          pygame.quit()
          sys.exit()
          

      # Camara funcional con mouse
      if event.type == pygame.MOUSEMOTION:
          x, y = pygame.mouse.get_pos()
          
          if x < 500:
            r.player["angle"] -= pi/20
          if x > 500:
            r.player["angle"] += pi/20

      # moveset
      if (event.type == pygame.KEYDOWN):
        if event.key == pygame.K_k:
          r.player["angle"] -= pi/10
        if event.key == pygame.K_j:
          r.player["angle"] += pi/10

        if event.key == pygame.K_d:
          step.play()
          r.player["x"] += 5
        if event.key == pygame.K_a:
          step.play()
          r.player["x"] -= 5
        if event.key == pygame.K_w:
          step.play()
          r.player["y"] -= 5
        if event.key == pygame.K_s:
          step.play()
          r.player["y"] += 5
    screen.blit(fps_title, (10, 10))
    screen.blit(current_fps, (10, 30))
    pygame.display.flip()
    clock.tick(60)

main_menu()