import pygame


class player:
    def __init__(self, surface, xPos, yPos, width, height, grassTiles):
        self.xPos = xPos
        self.yPos = yPos
        self.surface = surface
        self.grassTiles = grassTiles
        self.leftSensor = pygame.Rect(self.xPos - 70, self.yPos + 20, 70, 10)
        self.rightSensor = pygame.Rect(self.xPos + 20, self.yPos + 20, 70, 10)
        self.topSensor = pygame.Rect(self.xPos + 10, self.yPos - 70, 10, 70)
        self.bottomSensor = pygame.Rect(self.xPos + 10, self.yPos + 70, 10, 70)
        self.facing = 'up'
        self.origin = pygame.transform.scale(pygame.image.load('car.png'), (32, 64))
        self.acceleration = 3
        self.speed = 2.5
        self.moving = False
        self.sensorData = []
        self.image = pygame.image.load('car.png')
        self.image = pygame.transform.scale(self.image, (32, 64))
        self.playerRect = pygame.Rect(self.xPos, self.yPos, width, height)
        

    def monitorSensors(self):
        data = self.sensorData
        left = self.leftSensor.collidelist(self.grassTiles)
        if left > -1:
            left = 1
        else:
            left = 0    
        right = self.rightSensor.collidelist(self.grassTiles)
        if right > -1:
            right = 1
        else:
            right = 0    
        top = self.topSensor.collidelist(self.grassTiles)
        if top > -1:
            top = 1
        else:
            top = 0    
        bottom = self.bottomSensor.collidelist(self.grassTiles)
        if bottom > -1:
            bottom = 1
        else:
            bottom = 0    

        result = 0

        if self.facing == 'left':
            result = 0
        elif self.facing == 'right':
            result = 1    
        elif self.facing == 'top':
            result = 2
        elif self.facing == 'down':
            result = 3    

        data.append([left, right, top, bottom,result])
        self.sensorData = data
        


    def draw(self):
        self.monitorSensors()
        pygame.draw.rect(self.surface, (255, 255, 255),self.leftSensor, 2)
        pygame.draw.rect(self.surface, (255, 255, 255),self.rightSensor, 2)
        pygame.draw.rect(self.surface, (255, 255, 255),self.topSensor, 2)
        pygame.draw.rect(self.surface, (255, 255, 255),self.bottomSensor, 2)

        if self.facing == 'up':
            self.image = pygame.transform.rotate(self.origin, 0)
        elif self.facing == 'down':
             self.image = pygame.transform.rotate(self.origin, 180)
        elif self.facing == 'left':
            self.image = pygame.transform.rotate(self.origin, -90)  
        elif self.facing == 'right':
            self.image = pygame.transform.rotate(self.origin, 90)       
  
        self.surface.blit(self.image, (self.playerRect.x, self.playerRect.y))
        

    def moveUp(self):   
        self.facing = 'up'
        self.playerRect.y -= self.speed * self.acceleration 
        self.leftSensor.y  -= self.speed * self.acceleration 
        self.rightSensor.y  -= self.speed * self.acceleration 
        self.topSensor.y  -= self.speed * self.acceleration 
        self.bottomSensor.y  -= self.speed * self.acceleration

    def moveDown(self):           
        self.facing = 'down'
        self.playerRect.y += self.speed * self.acceleration
        self.leftSensor.y  += self.speed * self.acceleration   
        self.rightSensor.y  += self.speed * self.acceleration 
        self.topSensor.y  += self.speed * self.acceleration
        self.bottomSensor.y  += self.speed * self.acceleration


    def moveLeft(self):       
        self.facing = 'left'
        self.playerRect.x -= self.speed * self.acceleration  
        self.leftSensor.x  -= self.speed * self.acceleration   
        self.rightSensor.x  -= self.speed * self.acceleration   
        self.topSensor.x  -= self.speed * self.acceleration
        self.bottomSensor.x  -= self.speed * self.acceleration
  

    def moveRight(self):   
        self.facing = 'right'
        self.playerRect.x += self.speed * self.acceleration    
        self.leftSensor.x  += self.speed * self.acceleration   
        self.rightSensor.x  += self.speed * self.acceleration 
        self.topSensor.x  += self.speed * self.acceleration 
        self.bottomSensor.x  += self.speed * self.acceleration
   



        