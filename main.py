import pygame
import random
import math
from pygame import mixer
## initialize the pygame
pygame.init()

## create a screen ##
screen = pygame.display.set_mode((800, 600))

## Background ##
background = pygame.image.load('Background.png')

## Background Music ##
mixer.music.load('IM.mp3')
mixer.music.play(-1)   ## to play it continuously


## Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
## using List ##
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(0, 50))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet
## Ready = "you can't see the bullet on the screen
## Fire = The bullet is currently moving
## to find out if the bullet is in motion or not

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

## score ##
score_value = 0
## this is the default font of pygame , for any other you have to download it##
## to download new font use www.dafont.com ##
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

## Game Over #
over_font = pygame.font.Font("freesansbold.ttf",64)

## Play Again ##
play_again_font = pygame.font.Font("freesansbold.ttf", 48)

## first we will have to render the text on the screen then blit it ##
def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (0,255,0))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,250))

def play_again_text():
    play_text = play_again_font.render("PLAY AGAIN", True, (255,255,255))
    screen.blit(play_text, (250, 300))


def player(x, y):
    ## .blit method is use to draw ##
    screen.blit(playerImg, (x, y))

    ### use Ctrl + Alt + l for properly fomatting the code in pyCharm##


def enemy(x, y,i):
    ## .blit method is use to draw ##
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10))  ## this we are doing so that bullet appears on the centre of spaceship

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False


## game loop
running = True
while running:

    ##  RGB red, green, blue, values varies from 0 to 255 ##
    screen.fill((120, 120, 120))

    ## Background Image## it will come after the color ##
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        ## if keystroke is pressed check wheter it is left or right##

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                ## get the current x coordinate of current spaceship
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    ## checking boundaries for spaceship ##
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  ## 800-64 ##
        playerX = 736

    ## checking for boundaries ##
    ## enemy movements ##
    for i in range(num_of_enemies):

        ## Game Over #
        if enemyY[i] >= 440:
            for j in range(num_of_enemies):
                enemyY[j] =2000
            game_over_text()
            play_again_text()
            break

        enemyX[i] +=enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  ## 800-64 ##
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

            ## collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('Explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i],i)   ## we will have to call function multiple times ##


    ## Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"


    if bullet_state == "fire":   ## this function is here to make bullet on the screen if this funcion is not
        fire_bullet(bulletX,bulletY)   ## then bullet won't be on screen
        bulletY-=bulletY_change







    player(playerX, playerY)
    show_score(textX,textX)
    ## anything that you want to persist on the screen has to go into the while loop
    ## here we will have to use update method to update the game
    pygame.display.update()
