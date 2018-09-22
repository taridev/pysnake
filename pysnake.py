# Snake Game !

import pygame
import sys
import random
import time


WIDTH_IN_BLOCKS = 72
HEIGHT_IN_BLOCKS = 48
BLOCK_SIZE = 10
DEFAULT_SPEED = 15

check_errors = pygame.init()
pygame.display.set_caption('PySnake!')

# (6, 0)
if check_errors[1] > 0:
    print('(!) Erreur, sortie du programme'. format(check_errors[1]))
    sys.exit(-1)
else:
    print('(+) PyGame initialisé avec succes !')

# Plateau
playSurface = pygame.display.set_mode((WIDTH_IN_BLOCKS * BLOCK_SIZE, HEIGHT_IN_BLOCKS * BLOCK_SIZE))

# Couleurs
red = pygame.Color(255, 0, 0)        # gameover
green = pygame.Color(0, 255, 0)      # snake
black = pygame.Color(0, 0, 0)        # score
white = pygame.Color(255, 255, 255)  # background
brown = pygame.Color(165, 42, 42)    # food

# FPS
fpsController = pygame.time.Clock()

# Serpent
headPos = [100, 60]
snakeBody = [[100, 60], [80, 60], [60, 60]]
foodPos = [random.randrange(1, WIDTH_IN_BLOCKS) * BLOCK_SIZE, random.randrange(1, HEIGHT_IN_BLOCKS) * BLOCK_SIZE]
foodSpawn = True
direction = 'RIGHT'
speed = DEFAULT_SPEED
foodCounter = 0
pause = False
collision = False


# game over :
def game_over():
    my_font = pygame.font.SysFont('Monaco', 72)
    go_surf = my_font.render('Game Over !', True, red)
    go_rect = go_surf.get_rect()
    go_rect.midtop = (360, 15)
    playSurface.blit(go_surf, go_rect)
    pygame.display.flip()  # update de la window
    time.sleep(14)
    pygame.quit()
    sys.exit()


# Jeu
while True:
    for event in pygame.event.get():
        # Condition de sortie
        if event.type == pygame.QUIT:
            game_over()
            pygame.quit()
            sys.exit()

        # Gestion et controle de direction
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RIGHT or event.key == ord('d')) \
                    and not direction == 'LEFT':
                direction = 'RIGHT'
            if (event.key == pygame.K_LEFT or event.key == ord('q')) \
                    and not direction == 'RIGHT':
                direction = 'LEFT'
            if (event.key == pygame.K_UP or event.key == ord('z')) \
                    and not direction == 'DOWN':
                direction = 'UP'
            if (event.key == pygame.K_DOWN or event.key == ord('s')) \
                    and not direction == 'UP':
                direction = 'DOWN'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if event.key == pygame.K_SPACE:
                pause = not pause

    if direction == 'RIGHT' and not pause:
        headPos[0] += BLOCK_SIZE
    elif direction == 'LEFT' and not pause:
        headPos[0] -= BLOCK_SIZE
    elif direction == 'UP' and not pause:
        headPos[1] -= BLOCK_SIZE
    elif direction == 'DOWN' and not pause:
        headPos[1] += BLOCK_SIZE

    # Gestion des collisions
    if (headPos[0] > WIDTH_IN_BLOCKS * BLOCK_SIZE or headPos[0] < 0
            or headPos[1] > HEIGHT_IN_BLOCKS * BLOCK_SIZE or headPos[1] < 0
            or headPos in snakeBody[1:]):
        collision = True
        game_over()

    # Mécanismes du corp du serpent
    if not pause and not collision:
        snakeBody.insert(0, list(headPos))

    if headPos[0] == foodPos[0] and headPos[1] == foodPos[1]:
        foodSpawn = False
        foodCounter += 1
        speed = DEFAULT_SPEED + foodCounter % 5
    elif not pause and not collision:
        snakeBody.pop()

    # création du 
    if not foodSpawn:
        foodPos = [int(random.randrange(1, WIDTH_IN_BLOCKS) * BLOCK_SIZE), int(random.randrange(1, HEIGHT_IN_BLOCKS) * BLOCK_SIZE)]
        while foodPos in snakeBody:
            foodPos = [int(random.randrange(1, WIDTH_IN_BLOCKS) * BLOCK_SIZE),
                       int(random.randrange(1, HEIGHT_IN_BLOCKS) * BLOCK_SIZE)]
    foodSpawn = True

    playSurface.fill(black)

    # dessin du serpent
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # affichage du fruit
    if foodSpawn:
        pygame.draw.rect(playSurface, red, pygame.Rect(foodPos[0], foodPos[1], BLOCK_SIZE, BLOCK_SIZE))

    pygame.display.flip()
    fpsController.tick(speed)
