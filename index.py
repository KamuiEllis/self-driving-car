import pygame
import pytmx
from nn import nn
import pandas as pd
pygame.init()
from player import player

screen = pygame.display.set_mode((1000, 700)) 

tmx_data = pytmx.load_pygame("map.tmx")

collision_rects = []

mode = "manual"

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


    if keys[pygame.K_UP]:
        playerObj.moveUp()
    elif keys[pygame.K_LEFT]:
        playerObj.moveLeft()
    elif keys[pygame.K_RIGHT]:
        playerObj.moveRight()
    elif keys[pygame.K_DOWN]:
        playerObj.moveDown()    

    playerObj.draw() 
   
    
    # Update the display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
# print(playerObj.sensorData)
model = nn(playerObj.sensorData)
model.train()
