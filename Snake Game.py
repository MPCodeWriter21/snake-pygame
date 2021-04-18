"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 10

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Score
def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (frame_size_x / 10, 15)
    rect = pygame.Rect(score_rect[0] - 5, score_rect[1] - 5, score_rect[2] + 10, score_rect[3] + 10)
    pygame.draw.rect(game_window, red, rect, width=4)
    game_window.blit(score_surface, score_rect)
    return rect


# Difficulty
def show_difficulty(color, font, size):
    difficulty_font = pygame.font.SysFont(font, size)
    if difficulty < 25:
        diff = 'Easy'
    elif difficulty < 40:
        diff = 'Medium'
    elif difficulty < 60:
        diff = 'Hard'
    elif difficulty < 120:
        diff = 'Harder'
    else:
        diff = 'Impossible'
    difficulty_surface = difficulty_font.render('Difficulty : ' + diff, True, color)
    difficulty_rect = difficulty_surface.get_rect()
    difficulty_rect.midtop = (frame_size_x * 9 / 10 - difficulty_rect[3], 15)
    game_window.blit(difficulty_surface, difficulty_rect)


# Eating Score
def show_eating_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Stop EATING Score!!', True, color)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (frame_size_x / 2, frame_size_y - 25)
    game_window.blit(score_surface, score_rect)


# Game paused
def show_pause(color, font, size):
    pause_font = pygame.font.SysFont(font, size)
    pause_surface = pause_font.render('Paused', True, color)
    pause_rect = pause_surface.get_rect()
    pause_rect.midtop = (frame_size_x / 2, frame_size_y / 2 - pause_rect[3] / 2)
    game_window.blit(pause_surface, pause_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            if event.key == pygame.K_PAUSE or event.key == ord('p'):
                change_to = 'PAUSE'
                show_pause(red, 'consolas', 30)
                pygame.display.update()
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'PAUSE':
        continue
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # GFX
    game_window.fill(black)
    for pos in snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if snake_pos[0] < 0:
        snake_pos[0] = frame_size_x - 10
    if snake_pos[0] > frame_size_x - 10:
        snake_pos[0] = 0
    if snake_pos[1] < 0:
        snake_pos[1] = frame_size_y - 10
    if snake_pos[1] > frame_size_y - 10:
        snake_pos[1] = 0

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    # Show score
    rect = show_score(white, 'consolas', 16)
    eating_score = False
    # Decrease score if snake is in score box
    if score > 0:
        if snake_pos[0] - rect[0] in range(rect[2]) and snake_pos[1] - rect[1] in range(rect[3]):
            eating_score = True
            show_score(red, 'consolas', 16)
            show_eating_score(red, 'consolas', 20)
            score -= 1
            snake_body.pop()

    # Set difficulty
    difficulty = score * 2.5 + 10

    # Show difficulty
    show_difficulty(white, 'consolas', 16)

    # Spawning food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, frame_size_x // 10) * 10,
                    random.randrange(1 + (rect[1] + rect[3]) // 10, frame_size_y // 10) * 10]
        food_spawn = True

    # Snake food
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    if eating_score:
        fps_controller.tick(10)
    else:
        fps_controller.tick(difficulty)
