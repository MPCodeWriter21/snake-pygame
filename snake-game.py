"""Snake Eater Made with PyGame."""

import sys
import time
import random
from typing import Union, Iterable, Optional

import log21
import pygame

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


class SnakeGame:
    # Difficulty settings
    # Easy      ->  10
    # Medium    ->  25
    # Hard      ->  40
    # Harder    ->  60
    # Impossible->  120
    current_difficulty: int

    def __init__(
        self,
        frame_size_x: int = 720,
        frame_size_y: int = 480,
        font: Union[str, bytes, Iterable[Union[str, bytes]]] = 'consolas',
        base_difficulty: int = 10,
        difficulty_modifier: float = 2.5
    ) -> None:
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.font = font
        self.base_difficulty = base_difficulty
        self.current_difficulty = base_difficulty
        self.difficulty_modifier = difficulty_modifier

        # Checks for errors encountered
        check_errors = pygame.init()
        # pygame.init() example output -> (6, 0)
        # second number in tuple gives number of errors
        if check_errors[1] > 0:
            log21.error(
                f'Had {check_errors[1]} errors when initialising game, exiting...'
            )
            sys.exit(-1)
        else:
            log21.info('Game successfully initialised')

        # Initialise game window
        pygame.display.set_caption('Snake Eater')
        self.game_window = pygame.display.set_mode(
            (self.frame_size_x, self.frame_size_y)
        )

        # FPS (frames per second) controller
        self.fps_controller = pygame.time.Clock()

        # Game variables
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

        self.food_pos = [
            random.randrange(1, (self.frame_size_x // 10)) * 10,
            random.randrange(1, (self.frame_size_y // 10)) * 10
        ]
        self.food_spawn = True

        self.direction = 'RIGHT'
        self.change_to = self.direction

        self.score = 0

    def game_over(self):
        """Game Over function."""
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.frame_size_x // 2, self.frame_size_y // 4)
        self.game_window.fill(black)
        self.game_window.blit(game_over_surface, game_over_rect)
        self.show_score(color=red, font='times', size=20)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    def show_score(
        self,
        *,
        color: pygame.Color = white,
        font: Optional[Union[str, bytes, Iterable[Union[str, bytes]]]] = None,
        size: int = 16
    ):
        """Show score function."""
        font = font or self.font
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.frame_size_x // 10, 15)
        rect = pygame.Rect(
            score_rect[0] - 5, score_rect[1] - 5, score_rect[2] + 10, score_rect[3] + 10
        )
        pygame.draw.rect(self.game_window, red, rect, width=4)
        self.game_window.blit(score_surface, score_rect)
        return rect

    def show_difficulty(
        self,
        *,
        color: pygame.Color = white,
        font: Optional[Union[str, bytes, Iterable[Union[str, bytes]]]] = None,
        size: int = 16
    ):
        """Show difficulty function."""
        font = font or self.font
        difficulty_font = pygame.font.SysFont(font, size)
        if self.current_difficulty < 25:
            diff = 'Easy'
        elif self.current_difficulty < 40:
            diff = 'Medium'
        elif self.current_difficulty < 60:
            diff = 'Hard'
        elif self.current_difficulty < 120:
            diff = 'Harder'
        else:
            diff = 'Impossible'
        difficulty_surface = difficulty_font.render('Difficulty : ' + diff, True, color)
        difficulty_rect = difficulty_surface.get_rect()
        difficulty_rect.midtop = (self.frame_size_x * 9 // 10 - difficulty_rect[3], 15)
        self.game_window.blit(difficulty_surface, difficulty_rect)

    def show_eating_score(
        self,
        *,
        color: pygame.Color = red,
        font: Optional[Union[str, bytes, Iterable[Union[str, bytes]]]] = None,
        size: int = 20
    ):
        """Show eating score function."""
        font = font or self.font
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Stop EATING Score!!', True, color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (self.frame_size_x // 2, self.frame_size_y - 25)
        self.game_window.blit(score_surface, score_rect)

    def show_pause(
        self,
        *,
        color: pygame.Color = red,
        size: int = 30,
        font: Optional[Union[str, bytes, Iterable[Union[str, bytes]]]] = None,
    ):
        """Show pause function."""
        font = font or self.font
        pause_font = pygame.font.SysFont(font, size)
        pause_surface = pause_font.render('Paused', True, color)
        pause_rect = pause_surface.get_rect()
        pause_rect.midtop = (
            self.frame_size_x // 2, self.frame_size_y // 2 - pause_rect[3] // 2
        )
        self.game_window.blit(pause_surface, pause_rect)

    def move_snake(self):
        """Move snake function."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.change_to = 'RIGHT'
                if event.key == pygame.K_PAUSE or event.key == ord('p'):
                    self.change_to = 'PAUSE'
                    self.show_pause(font='consolas')
                    pygame.display.update()
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        if self.change_to == 'PAUSE':
            return 1
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        # Moving the snake
        if self.direction == 'UP':
            self.snake_pos[1] -= 10
        if self.direction == 'DOWN':
            self.snake_pos[1] += 10
        if self.direction == 'LEFT':
            self.snake_pos[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_pos[0] += 10

    def run(self):
        """Run the game."""
        while True:
            if self.move_snake():
                continue

            # Snake body growing mechanism
            self.snake_body.insert(0, list(self.snake_pos))
            if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[
                    1] == self.food_pos[1]:
                self.score += 1
                self.food_spawn = False
            else:
                self.snake_body.pop()

            # GFX
            self.game_window.fill(black)
            for pos in self.snake_body:
                # Snake body
                # .draw.rect(play_surface, color, xy-coordinate)
                # xy-coordinate -> .Rect(x, y, size_x, size_y)
                pygame.draw.rect(
                    self.game_window, green, pygame.Rect(pos[0], pos[1], 10, 10)
                )

            # Game Over conditions
            # Getting out of bounds
            if self.snake_pos[0] < 0:
                self.snake_pos[0] = self.frame_size_x - 10
            if self.snake_pos[0] > self.frame_size_x - 10:
                self.snake_pos[0] = 0
            if self.snake_pos[1] < 0:
                self.snake_pos[1] = self.frame_size_y - 10
            if self.snake_pos[1] > self.frame_size_y - 10:
                self.snake_pos[1] = 0

            # Touching the snake body
            for block in self.snake_body[1:]:
                if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                    self.game_over()

            # Show score
            rect = self.show_score()
            eating_score = False
            # Decrease score if snake is in score box
            if self.score > 0 and self.snake_pos[0] - rect[0] in range(
                    rect[2]) and self.snake_pos[1] - rect[1] in range(rect[3]):
                eating_score = True
                self.show_score(color=red)
                self.show_eating_score(color=red)
                self.score -= 1
                self.snake_body.pop()

            # Set difficulty
            difficulty = self.score * self.difficulty_modifier + self.base_difficulty

            # Show difficulty
            self.show_difficulty()

            # Spawning food on the screen
            if not self.food_spawn:
                self.food_pos = [
                    random.randrange(1, self.frame_size_x // 10) * 10,
                    random
                    .randrange(1 +
                               (rect[1] + rect[3]) // 10, self.frame_size_y // 10) * 10
                ]
                self.food_spawn = True

            # Snake food
            pygame.draw.rect(
                self.game_window, white,
                pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10)
            )

            # Refresh game screen
            pygame.display.update()
            # Refresh rate
            if eating_score:
                self.fps_controller.tick(10)
            else:
                self.fps_controller.tick(difficulty)


if __name__ == '__main__':
    game = SnakeGame(
        frame_size_x=1080,
        frame_size_y=720,
        base_difficulty=20,
        difficulty_modifier=2
    )
    game.run()
