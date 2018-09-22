# Snake Game !

import pygame
import sys
import random


WIDTH_IN_BLOCKS = 36
HEIGHT_IN_BLOCKS = 24
BLOCK_SIZE = 20
DEFAULT_SPEED = 10

check_errors = pygame.init()
pygame.display.set_caption('PySnake!')

# (6, 0)
if check_errors[1] > 0:
    print('(!) Erreur, sortie du programme'. format(check_errors[1]))
    sys.exit(-1)
else:
    print('(+) PyGame initialise avec succes !')

# Plateau
playSurface = pygame.display.set_mode((WIDTH_IN_BLOCKS * BLOCK_SIZE, HEIGHT_IN_BLOCKS * BLOCK_SIZE))

# Couleurs
red = pygame.Color(255, 0, 0)        # gameover
green = pygame.Color(0, 255, 0)      # snake
black = pygame.Color(0, 0, 0)        # score
white = pygame.Color(255, 255, 255)  # background
darkblue = pygame.Color('#0B1340')
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
pause = False
gameOver = False
score = 0


# game over :
def game_over():
    header_font = pygame.font.SysFont('Monaco', 72)
    options_font = pygame.font.SysFont('Monaco', 25)
    header_font = header_font.render('Game Over !', True, red)
    options_font = options_font.render('Enter to start new game, Esc to quit', True, red)
    header_rect = header_font.get_rect()
    header_rect.midtop = (360, 175)
    options_rect = options_font.get_rect()
    options_rect.midtop = (360, 135)
    playSurface.blit(header_font, header_rect)
    playSurface.blit(options_font, options_rect)


def show_score(choice=1):
    my_font = pygame.font.SysFont('sana', 24)
    score_surf = my_font.render('Score : {0}'.format(score), True, red)
    score_rect = score_surf.get_rect()
    if choice == 1:
        score_rect.midtop = (60, 10)
    else:
        score_rect.midtop = (360, 120)
    playSurface.blit(score_surf, score_rect)


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
            if event.key == pygame.K_RETURN:
                headPos = [100, 60]
                snakeBody = [[100, 60], [80, 60], [60, 60]]
                foodPos = [random.randrange(1, WIDTH_IN_BLOCKS) * BLOCK_SIZE,
                           random.randrange(1, HEIGHT_IN_BLOCKS) * BLOCK_SIZE]
                foodSpawn = True
                direction = 'RIGHT'
                speed = DEFAULT_SPEED + int(score / 3)
                pause = False
                gameOver = False
                score = 0

    if direction == 'RIGHT' and not pause:
        headPos[0] += BLOCK_SIZE
    elif direction == 'LEFT' and not pause:
        headPos[0] -= BLOCK_SIZE
    elif direction == 'UP' and not pause:
        headPos[1] -= BLOCK_SIZE
    elif direction == 'DOWN' and not pause:
        headPos[1] += BLOCK_SIZE

    # Gestion des collisions
    if headPos[0] > (WIDTH_IN_BLOCKS * BLOCK_SIZE)-BLOCK_SIZE \
            or headPos[0] < 0 \
            or headPos[1] > (HEIGHT_IN_BLOCKS * BLOCK_SIZE)-BLOCK_SIZE \
            or headPos[1] < 0 \
            or headPos in snakeBody[1:]:
        gameOver = True

    # Mecanismes du corp du serpent
    if not pause and not gameOver:
        snakeBody.insert(0, list(headPos))

    if headPos[0] == foodPos[0] and headPos[1] == foodPos[1]:
        foodSpawn = False
        score += 1
        speed = DEFAULT_SPEED
    elif not pause and not gameOver:
        snakeBody.pop()

    # creation du fuit
    if not foodSpawn:
        foodPos = [int(random.randrange(1, WIDTH_IN_BLOCKS) * BLOCK_SIZE), int(random.randrange(1, HEIGHT_IN_BLOCKS) * BLOCK_SIZE)]
        while foodPos in snakeBody:
            foodPos = [int(random.randrange(1, WIDTH_IN_BLOCKS) * BLOCK_SIZE),
                       int(random.randrange(1, HEIGHT_IN_BLOCKS) * BLOCK_SIZE)]
    foodSpawn = True

    playSurface.fill(darkblue)

    # dessin du serpent
    for pos in snakeBody:
        pygame.draw.rect(playSurface, green, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

    # affichage du fruit
    pygame.draw.rect(playSurface, brown, pygame.Rect(foodPos[0], foodPos[1], BLOCK_SIZE, BLOCK_SIZE))

    show_score()
    if gameOver:
        game_over()

    pygame.display.flip()  # update de la window
    fpsController.tick(speed)
