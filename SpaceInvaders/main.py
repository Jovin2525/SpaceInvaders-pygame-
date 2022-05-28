# Initialise the game
import random
import math

import pygame
from pygame import mixer # Class that handles music

pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))  # width,height

# Background
background = pygame.image.load("background.png")

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("SpaceInvader Game")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Light shade of QUIT button
color_light = (170, 170, 170)

# dark shade of QUIT button
color_dark = (100, 100, 100)
# defining QUIT font
quit_font = pygame.font.Font("freesansbold.ttf", 30)#SysFont('Corbel', 35)


# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Bullet
# Ready - Cannot see bullet
# Fire - Bullet moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)
def quit_button(x,y):
    # Rendering QUIT written in this font
    quit = quit_font.render('QUIT', True, (255, 255, 255))
    # superimposing the text onto our button
    screen.blit(quit, (x, y))

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255)) # Render text on screen
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255)) # Render text on screen
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))  # blit means to draw -> drawing image of player on screen i.e. surface


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # +16 to ensure bullet appears in the center of spaceship


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running:  # anything you want to persistently appear on the screen must be placed in the while loop

    # RGB
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:  # any keystroke pressed down
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    explosion_Sound = mixer.Sound('laser.wav') #use .sound since short sound otherwise .music
                    explosion_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:  # keystroke no longer pressed
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        # Checks if a mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:

            # if the mouse is clicked on the
            # button the game is terminated
            if 705 <= mouse[0] <= 790 and 5 <= mouse[1] <= 40:
                pygame.quit()

    # if mouse is hovered on a button it changes to lighter shade
    if 705 <= mouse[0] <= 790 and 5 <= mouse[1] <= 40:
        pygame.draw.rect(screen, color_light, [705, 5, 85, 35])

    else:
        pygame.draw.rect(screen, color_dark, [705, 5, 85, 35])

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # image is 64 px (800-64)
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000 # all enemies go below screen
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # image is 64 px (800-64)
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bullet_Sound = mixer.Sound('explosion.wav')
            bullet_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":  # ensures bullet persists
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    quit_button(710, 10)
    player(playerX,
           playerY)  # must be called after the screen.fill otherwise player won't appear on screen due to screen drawn first
    show_score(textX, textY)
    pygame.display.update()  # update screen
