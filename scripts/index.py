import pygame
import pytmx
from nn import nn
from menu import menu
import time
import pandas as pd
import asyncio
import tensorflow as tf
import numpy as np

pygame.init()
from player import player

screen = pygame.display.set_mode((1666, 768)) 
menu = menu(screen)

tmx_data = pytmx.load_pygame("./map.tmx")


collision_rects = []
training = False
manual = True
seconds = 0

grass = tmx_data.get_layer_by_name('grass')
if isinstance(grass, pytmx.TiledTileLayer):
    for x, y, gid in grass:
        tile = tmx_data.get_tile_image_by_gid(gid)
        # tileProperties = tmx_data.get_tile_properties_by_gid(gid)
        if tile:
                # Create a rectangle for the collidable tile's position
                rect = pygame.Rect(
                    x * tmx_data.tilewidth,
                    y * tmx_data.tileheight,
                    tmx_data.tilewidth,
                    tmx_data.tileheight
                )
                collision_rects.append(rect)

playerObj = player(screen, 500, 600, 32,32, collision_rects)

def draw_layer(layer_name, alpha=255):
    # Find the layer by name
    layer = tmx_data.get_layer_by_name(layer_name)
    
    # Set a transparency level if desired
    if alpha < 255:
        surface = pygame.Surface((tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight), pygame.SRCALPHA)
        surface.set_alpha(alpha)
    else:
        surface = screen

    # Render only if it's a tile layer
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid in layer:
            tile = tmx_data.get_tile_image_by_gid(gid)
            if tile:
                # Draw each tile at the correct position
              
                surface.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

    # If using a separate surface for transparency, blit it onto the main screen
    if alpha < 255:
        screen.blit(surface, (0, 0))

try:
    model = tf.keras.models.load_model('car.keras')
except:
    print('no model found')


def deduce(data):
    first = 0
    for x in range(0, len(data)):
        if data[x] > data[first]:
            first = x
    return first        


clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():  # Handle events like key presses
        if event.type == pygame.QUIT:  # Close the game window
            running = False
    

    keys = pygame.key.get_pressed()

       


    # Fill the screen with a color (RGB format)
    screen.fill((0, 0, 0))  # Black background
    draw_layer("road")
    draw_layer("grass")

    if event.type == pygame.MOUSEBUTTONDOWN:
        playerObj.selectSensor(event)

    if keys[pygame.K_TAB]:
        if seconds > 150:
            training = not training  
            seconds = 0
           
    if keys[pygame.K_LSHIFT]:
        if seconds > 150:
            manual = not manual 
            seconds = 0      
    if manual == True:
        if playerObj.adjustmentMode == False:
            if keys[pygame.K_UP]:
                playerObj.moveUp()
            elif keys[pygame.K_LEFT]:
                playerObj.moveLeft()
            elif keys[pygame.K_RIGHT]:
                playerObj.moveRight()
            elif keys[pygame.K_DOWN]:
                playerObj.moveDown()    
        else:
            if keys[pygame.K_LEFT]:
                playerObj.adjustWidth('left') 
            elif keys[pygame.K_RIGHT]:
                playerObj.adjustWidth('right')   
            elif keys[pygame.K_UP]:
                playerObj.adjustHeight('top') 
            elif keys[pygame.K_DOWN]:
                playerObj.adjustHeight('bottom')   
            elif keys[pygame.K_i]:
                playerObj.adjustYPos('up') 
            elif keys[pygame.K_k]:
                playerObj.adjustYPos('down')
            elif keys[pygame.K_j]:
                playerObj.adjustXPos('left')
            elif keys[pygame.K_l]:
                playerObj.adjustXPos('right') 
    else:

        result = model.predict(np.array([playerObj.currentSensorInformation]))
        direction = deduce(result[0])
        if direction == 0:
            playerObj.moveLeft()
        elif direction == 1:
            playerObj.moveRight()
        elif playerObj == 2:
            playerObj.moveUp()     
        else:
            playerObj.moveDown()       

                                        

    menu.draw(training, manual)
  
    if playerObj.selectedRect != None:
        menu.drawSelectedItemDetails(playerObj.selectedRect.x, playerObj.selectedRect.y, playerObj.selectedRect.width, playerObj.selectedRect.height)
    playerObj.draw() 
   
    if playerObj.crash == True:
        if training == True:
            menu.drawTrainingRect() 
          
            # time.sleep(5)
            # print('crashed')
        else:
            playerObj.crash = False;    
            
            
    
    # Update the display
    pygame.display.flip()
    clock.tick(30)
    seconds+=30

    if training == True:
        if playerObj.crash == True:
          
            # time.sleep(5)
            # print('crashed')
            # menu.drawTrainingRect() 
            model2 = nn(playerObj.sensorData)
            
            asyncio.run(model2.train())
            playerObj.crash = False


pygame.quit()
playerObj.saveData()
# print(playerObj.sensorData)
# model = nn(playerObj.sensorData)
# model.train()
