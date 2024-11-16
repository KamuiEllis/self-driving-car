import pygame


class menu:
    def __init__(self, surface):
        self.mode = 'manual'
        self.surface = surface
        self.training = False
        self.itemDetailsRect = pygame.Rect(400, 30, 200, 90)
        self.detailsRect = pygame.Rect(100, 30, 250, 70)


    def drawSelectedItemDetails(self,xPos, yPos, width, height):
        font = pygame.font.Font(None, 20)  # Use None to select the default font, 36 is the font size
        text_color = (255, 255, 255)
        # Define text
        text_color = (221, 219, 67)
        xposition = font.render(f'X position: {xPos}', True, text_color)
        yposition = font.render(f'Y position: {yPos}', True, text_color)
        widthData = font.render(f'Width: {width}', True, text_color)
        heightData = font.render(f'Height: {height}', True, text_color)

        text_rectx =  pygame.Rect(410, 35, 180, 80)
        text_recty =  pygame.Rect(410, 55, 180, 80)
        text_width =  pygame.Rect(410, 75, 180, 80)
        text_height =  pygame.Rect(410, 95, 180, 80)

        pygame.draw.rect(self.surface, (46, 46, 46), self.itemDetailsRect)
        self.surface.blit(xposition, text_rectx)
        self.surface.blit(yposition, text_recty)
        self.surface.blit(widthData, text_width)
        self.surface.blit(heightData, text_height)

    def draw(self, training):
        self.training = training
        font = pygame.font.Font(None, 36) 
        text_color = (255, 255, 255)
 
        text_color = (221, 219, 67)
        text_surface = font.render(f'Mode: {self.mode}', True, text_color)
        text_rect =  pygame.Rect(110, 35, 180, 80)

        text_surface2 = font.render(f'Training Mode: {"On" if self.training == True else "Off"}', True, text_color)
        text_rect2 =  pygame.Rect(110, 70, 216, 80)
       
        pygame.draw.rect(self.surface, (46, 46, 46), self.detailsRect)
        self.surface.blit(text_surface,  text_rect)
        self.surface.blit(text_surface2,  text_rect2)

            


