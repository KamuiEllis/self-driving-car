import pygame
import json

class player:
    def __init__(self, surface, xPos, yPos, width, height, grassTiles):
        with open('settings.json', 'r') as file:
            self.data = json.load(file)
        self.xPos = xPos
        self.yPos = yPos
        self.surface = surface
        self.grassTiles = grassTiles
        self.leftSensor = pygame.Rect(self.data["leftSensor"]["xPos"], self.data["leftSensor"]["yPos"], self.data["leftSensor"]["width"], self.data["leftSensor"]["height"])
        self.rightSensor = pygame.Rect(self.data["rightSensor"]["xPos"], self.data["rightSensor"]["yPos"], self.data["rightSensor"]["width"], self.data["rightSensor"]["height"])
        self.topSensor = pygame.Rect(self.data["topSensor"]["xPos"], self.data["topSensor"]["yPos"], self.data["topSensor"]["width"], self.data["topSensor"]["height"])
        self.bottomSensor = pygame.Rect(self.data["bottomSensor"]["xPos"], self.data["bottomSensor"]["yPos"], self.data["bottomSensor"]["width"], self.data["bottomSensor"]["height"])
        self.facing = 'up'
        self.origin = pygame.transform.scale(pygame.image.load('car.png'), (32, 64))
        self.acceleration = 3
        self.speed = 2.5
        self.moving = False
        self.sensorData = []
        self.rotateOffset = 100
        self.adjustOffset = False
        self.image = pygame.image.load('car.png')
        self.image = pygame.transform.scale(self.image, (32, 64))
        self.playerRect = pygame.Rect(self.data["car"]["xPos"], self.data["car"]["yPos"], width, height)
        self.selectedRect = None
        self.adjustmentMode = False
        self.currentSelectedSensor = ''
        self.currentSensorInformation = [0,0,0,0]
        self.crash = False
        

    def saveData(self):
        data = {
            "leftSensor": {
                "xPos": self.leftSensor.x,
                "yPos": self.leftSensor.y,
                "width":self.leftSensor.width,
                "height": self.leftSensor.height
            },

            "rightSensor": {
                "xPos": self.rightSensor.x,
                "yPos": self.rightSensor.y,
                "width":self.rightSensor.width,
                "height": self.rightSensor.height
            }, 

            "topSensor": {
                "xPos": self.topSensor.x,
                "yPos": self.topSensor.y,
                "width": self.topSensor.width,
                "height": self.topSensor.height
            }, 

            "bottomSensor": {
                "xPos": self.bottomSensor.x,
                "yPos": self.bottomSensor.y,
                "width": self.bottomSensor.width,
                "height": self.bottomSensor.height
            },

            "car": {
                "xPos": self.playerRect.x,
                "yPos": self.playerRect.y
            }  
        }

        with open('settings.json', 'w') as file:
            json.dump(data, file, indent=4)

    def monitorPlayer(self):
        
        playerCollided = self.playerRect.collidelist(self.grassTiles)

        if playerCollided > -1:
            self.crash = True
             # Reset playerRect position
            self.playerRect.x = self.data["car"]["xPos"]
            self.playerRect.y = self.data["car"]["yPos"]

            # Reset leftSensor position
            self.leftSensor.x = self.data['leftSensor']["xPos"]
            self.leftSensor.y = self.data['leftSensor']["yPos"]

            # Reset rightSensor position
            self.rightSensor.x = self.data['rightSensor']["xPos"]
            self.rightSensor.y = self.data['rightSensor']["yPos"]

            # Reset topSensor position
            self.topSensor.x = self.data['topSensor']["xPos"]
            self.topSensor.y = self.data['topSensor']["yPos"]

            # Reset bottomSensor position
            self.bottomSensor.x = self.data['bottomSensor']["xPos"]
            self.bottomSensor.y = self.data['bottomSensor']["yPos"]
        

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
        self.currentSensorInformation = [left, right, top, bottom,]
        self.sensorData = data
        
    def adjustXPos(self, action):
        if action == 'left':
            self.selectedRect.x-=1
 
        if action == 'right':
            self.selectedRect.x+=1

    def adjustYPos(self, action):
        if action == 'up':
            self.selectedRect.y-=1
            
 
        if action == 'down':
            self.selectedRect.y+=1        
            


    def adjustHeight(self, action):
        if action == 'top':
            self.selectedRect.height-=1
 
            # self.leftSensor.height = self.selectedRect.height
        if action == 'bottom':
            self.selectedRect.height+=1
            
            # self.leftSensor.height = self.selectedRect.height
        

    def adjustWidth(self, action):
        if action == 'left':
            self.selectedRect.width-=1
          
            # self.leftSensor.width = self.selectedRect.width
        if action == 'right':
            self.selectedRect.width+=1
           
            # self.leftSensor.width = self.selectedRect.width
         
       

    def selectSensor(self, event): 
       
        if self.leftSensor.collidepoint(event.pos):
            self.adjustmentMode = True
            self.currentSelectedSensor = 'left'
            self.selectedRect = self.leftSensor

        elif self.rightSensor.collidepoint(event.pos):
            self.adjustmentMode = True
            self.currentSelectedSensor = 'right'
            self.selectedRect = self.rightSensor 

        elif self.topSensor.collidepoint(event.pos):
            self.adjustmentMode = True
            self.currentSelectedSensor = 'top'
            self.selectedRect = self.topSensor   

        elif self.bottomSensor.collidepoint(event.pos):
            self.adjustmentMode = True
            self.currentSelectedSensor = 'bottom'
            self.selectedRect = self.bottomSensor  
        elif self.playerRect.collidepoint(event.pos):
            self.adjustmentMode = True
            self.currentSelectedSensor = 'car'
            self.selectedRect = self.playerRect
        else:
            self.adjustmentMode = False
            self.selectedRect = None
            self.currentSelectedSensor = None





    def draw(self):
        self.monitorSensors()
        self.monitorPlayer()
        # Draw sensors with highlighting for the selected one
        if self.currentSelectedSensor == 'left':
            pygame.draw.rect(self.surface, (255, 255, 255), self.leftSensor, 2)
        else:
            pygame.draw.rect(self.surface, (205, 203, 47), self.leftSensor, 2)

        if self.currentSelectedSensor == 'right':
            pygame.draw.rect(self.surface, (255, 255, 255), self.rightSensor, 2)
        else:
            pygame.draw.rect(self.surface, (205, 203, 47), self.rightSensor, 2)

        if self.currentSelectedSensor == 'top':
            pygame.draw.rect(self.surface, (255, 255, 255), self.topSensor, 2)
        else:
            pygame.draw.rect(self.surface, (205, 203, 47), self.topSensor, 2)

        if self.currentSelectedSensor == 'bottom':
            pygame.draw.rect(self.surface, (255, 255, 255), self.bottomSensor, 2)
        else:
            pygame.draw.rect(self.surface, (205, 203, 47), self.bottomSensor, 2)

        # Determine the angle based on facing direction
        angle = 0
        if self.facing == 'down':
            angle = 180
        elif self.facing == 'left':
            angle = 90
        elif self.facing == 'right':
            angle = -90

        # Rotate the image while keeping it centered
        rotated_image = pygame.transform.rotate(self.origin, angle)
        rotated_rect = rotated_image.get_rect(center=self.playerRect.center)

        # Blit the rotated image onto the surface
        self.surface.blit(rotated_image, rotated_rect.topleft)

       

        
            

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
   



        