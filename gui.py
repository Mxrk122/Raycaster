import pygame

def get_font(size):
    return pygame.font.Font("textures/font.ttf", size)

# Clase para botones 
class Button(object):
    def __init__(self, position, text_input, font, color):
        self.x_pos, self.y_pos = position
        self.font = font
        self.color = color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.color)
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    
    def reveal(self, screen):
        screen.blit(self.text, self.rect)
    
    def checkForInput(self, position):
        horizontal_range = range(self.rect.left, self.rect.right)
        vertical_range = range(self.rect.top, self.rect.bottom)
        if position[0] in horizontal_range and position[1] in vertical_range:
            return True
        return False