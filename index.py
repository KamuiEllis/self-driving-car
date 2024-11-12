import pygame
import pytmx
from nn import nn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
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
array = playerObj.sensorData

# data = pd.DataFrame(array)
# x = data.iloc[:, :4].values
# y = data.iloc[:, -1].values
# y = tf.keras.utils.to_categorical(y, num_classes=4)


# x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.1, random_state=0)



# try:
#     ann = tf.keras.models.load_model('car.keras')
#     print('loading existing model')
# except:  
#     print('creating new model')  
#     ann = tf.keras.models.Sequential()
#     ann.add(tf.keras.layers.Dense(units=6, activation='relu'))
#     ann.add(tf.keras.layers.Dense(units=6, activation='relu'))
#     ann.add(tf.keras.layers.Dense(units=4, activation='softmax')) 

# ann.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss = 'categorical_crossentropy' , metrics = ['accuracy'])
    
# ann.fit(x_train, y_train, batch_size = 32, epochs = 500)

# result = ann.predict(np.array([[1, 0, 0, 0,]]))
# print(result)
