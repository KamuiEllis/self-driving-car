import pygame


class menu:
    def __init__(self, surface):
        self.mode = 'manual'
        self.surface = surface
        self.detailsRect = pygame.Rect(100, 30, 200, 40)



    def draw(self):
        font = pygame.font.Font(None, 36)  # Use None to select the default font, 36 is the font size
        text_color = (255, 255, 255)
        # Define text
        text_color = (221, 219, 67)
        text_surface = font.render(f'Mode: {self.mode}', True, text_color)
        text_rect =  pygame.Rect(110, 35, 180, 80)

        pygame.draw.rect(self.surface, (46, 46, 46), self.detailsRect)
        self.surface.blit(text_surface,  text_rect)

            


