import pygame
import random
import math
from pygame import mixer

# Initialisation
pygame.init()

#Screen
screen=pygame.display.set_mode((800,600))

#Speeds depend on the device you're using, alter them using this:
speed_enemy=1.5
speed_player=2
speed_bullet=3.5

#Background
background=pygame.image.load("bg2.png").convert()

#Background music
mixer.music.load('Game bg music.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Rocket gang")
icon=pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Butt-player
playerImg=pygame.image.load('Ass.png')
playerX=368
playerY=60
playerX_change=0

#Toilet-enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
number=20
for i in range (number):
    enemyImg.append(pygame.image.load('toilet.png'))
    enemyX.append(random.randint(20,715))
    enemyY.append(random.randint(360,480))
    enemyX_change.append(random.choice([speed_enemy,-speed_enemy]))
    enemyY_change.append(40)

#Poop-bullet
bulletImg=pygame.image.load('poop.png')
bulletX=0
bulletY=60
bulletX_change=0           #Bullet's not going to move in the x-direction
bulletY_change=speed_bullet
bullet_state="ready"

def player(x,y):
    screen.blit(playerImg,(x,y))


def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state='fired'
    screen.blit(bulletImg,(x+16,y+20))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    dist=math.sqrt(math.pow((enemyX-bulletX),2) + math.pow((enemyY-bulletY),2))
    if (dist<=27):
        return True


#Keeping score
score_val=0
font=pygame.font.Font("freesansbold.ttf",32)
textX=10
textY=10

def show_score(x,y):
    score=font.render("Score: "+str(score_val), True, (0,0,0))
    screen.blit(score,(x,y))

#End screen
last_font=pygame.font.Font("freesansbold.ttf",64)

def gameover():
    gameover_text=last_font.render("GAME OVER", True, (0,0,0))
    screen.blit(gameover_text,(200,268))

#Main game loop
running=True
while running:

    #Putting the bg using the while loop
    screen.blit(background,(0,0))

    #To quit the window on pressing the 'X'button
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        #To check if any key stroke is done:
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:                   #This part is to 
                playerX_change=-(speed_player)             #move the butt           
            elif event.key==pygame.K_RIGHT:                #left or right
                playerX_change=speed_player
            #To shoot bullet:
            elif event.key==pygame.K_SPACE:
                if bullet_state=="ready":
                    poop_sound=mixer.Sound('poop.wav')
                    poop_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
            
        elif event.type==pygame.KEYUP:
            if (event.key==pygame.K_LEFT) or (event.key==pygame.K_RIGHT):
                playerX_change=0



    #Adding imaginary boundaries
    if (playerX <=20):
        playerX=20
    elif (playerX >=716):
        playerX=716  
    
    #moving the player    
    playerX+=playerX_change
   
    #Drawing the player
    player(playerX,playerY)

    #moving the enemy
    for i in range(number):
        enemyX[i]+=enemyX_change[i]
    
    for i in range (number):
        if (enemyX[i] <=20):
            enemyX_change[i]=-(enemyX_change[i])
            enemyY[i]-=enemyY_change[i]
        if (enemyX[i] >=716):
            enemyX_change[i]=-(enemyX_change[i])
            enemyY[i]-=enemyY_change[i]

    #moving the bullet
    if bulletY>=600:
        bulletY=60
        bullet_state="ready"
    if bullet_state=="fired":
        fire_bullet(bulletX,bulletY)
        bulletY+=bulletY_change
    
    #Checking for collision using the user-made function
    for i in range (number):
        collision=iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            coll_sound=mixer.Sound("flushcut.wav")
            coll_sound.play()
            score_val+=1
            bulletY=60
            bullet_state='ready'
            enemyX[i]=random.randint(20,716)
            enemyY[i]=random.randint(360,480)


    #Drawing the enemy
    for i in range (number):
        enemy(enemyX[i],enemyY[i],i)

    #Showing the Game Over
    for i in range (number):
        if enemyY[i]<=92:
            for j in range (number):
                enemyY[j]=-1000
            gameover()
            break
    #Showing the score
    show_score(textX,textY)

    pygame.display.update()
    

