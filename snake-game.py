"""Snake Eater Made with PyGame."""

import sys
import time
import random
from typing import Union, Iterable, Optional
from threading import Thread

import log21
import pygame

# Colors (R, G, B)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)


class SnakeGame:
    # Difficulty settings
    # Easy      ->  10
    # Medium    ->  25
    # Hard      ->  40
    # Harder    ->  60
    # Impossible->  120
    current_difficulty: float

    def __init__(
        self,
        frame_size_x: int = 720,
        frame_size_y: int = 480,
        font: Union[str, bytes, Iterable[Union[str, bytes]]] = 'consolas',
        base_difficulty: float = 10,
        difficulty_modifier: float = 2.5,
        fps: int = 60,
        big_food_chance: float = 0.03,
        big_food_score: int = 3,
        big_food_time: float = 6
    ) -> None:
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.font = font
        self.base_difficulty = base_difficulty
        self.current_difficulty = base_difficulty
        self.difficulty_modifier = difficulty_modifier
        self.fps = fps
        self.big_food_chance = big_food_chance
        self.big_food_score = big_food_score
        self.big_food_time = big_food_time
        self.big_food_time_left = 0
        self.getting_big_score = 0

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

        # Game variables
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

        self.food_pos = [
            random.randrange(1, (self.frame_size_x // 10)) * 10,
            random.randrange(1, (self.frame_size_y // 10)) * 10
        ]
        self.food_spawn = True
        self.big_food_pos = [0, 0]

        self.direction = 'RIGHT'
        self.change_to = self.direction

        self.score = 0
        self.eating_score = False

        self.__running = False

    def game_over(self):
        """Game Over function."""
        self.__running = False
        my_font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = my_font.render('YOU DIED', True, RED)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.frame_size_x // 2, self.frame_size_y // 4)
        self.game_window.fill(BLACK)
        self.game_window.blit(game_over_surface, game_over_rect)
        self.show_score(color=RED, font='times', size=20)
        pygame.display.flip()
        time.sleep(3)

    def show_score(
        self,
        *,
        color: pygame.Color = WHITE,
        font: Optional[Union[str, bytes, Iterable[Union[str, bytes]]]] = None,
        size: int = 16,
        draw: bool = True
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
        if draw:
            pygame.draw.rect(self.game_window, RED, rect, width=4)
            self.game_window.blit(score_surface, score_rect)
        return rect

    def show_difficulty(
        self,
        *,
        color: pygame.Color = WHITE,
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
        color: pygame.Color = RED,
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
        color: pygame.Color = RED,
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

    def do_drawings(self):
        """Draw the things that need to be drawn."""
        self.game_window.fill(BLACK)
        for pos in self.snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(
                self.game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10)
            )

        # Show score
        self.show_score()

        # Show difficulty
        self.show_difficulty()

        # Snake food
        pygame.draw.rect(
            self.game_window, WHITE,
            pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10)
        )

        # Big food
        if self.big_food_time_left > 0:
            pygame.draw.rect(
                self.game_window, WHITE,
                pygame.Rect(self.big_food_pos[0], self.big_food_pos[1], 20, 20)
            )

    def main_loop(self):
        """Main loop function."""
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    return
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

            self.do_drawings()

            # Making sure the snake cannot move in the opposite direction
            # instantaneously
            if self.change_to == 'PAUSE':
                time.sleep(self.tick)
                continue
            if self.change_to == 'UP' and self.direction != 'DOWN':
                self.direction = 'UP'
            if self.change_to == 'DOWN' and self.direction != 'UP':
                self.direction = 'DOWN'
            if self.change_to == 'LEFT' and self.direction != 'RIGHT':
                self.direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.direction != 'LEFT':
                self.direction = 'RIGHT'

            # Refresh game screen
            pygame.display.update()
            # Refresh rate
            # if self.eating_score:
            #     # self.fps_controller.tick(10)
            #     time.sleep(1 / self.base_difficulty)
            # else:
            #     # self.fps_controller.tick(difficulty)
            time.sleep(self.tick)

    def __run(self):
        while self.__running:
            if self.change_to == 'PAUSE':
                time.sleep(self.tick)
                continue

            # Moving the snake
            if self.direction == 'UP':
                self.snake_pos[1] -= 10
            if self.direction == 'DOWN':
                self.snake_pos[1] += 10
            if self.direction == 'LEFT':
                self.snake_pos[0] -= 10
            if self.direction == 'RIGHT':
                self.snake_pos[0] += 10

            # Snake eating and growing mechanism
            self.snake_body.insert(0, list(self.snake_pos))
            if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[
                    1] == self.food_pos[1]:
                self.score += 1
                self.food_spawn = False
            elif self.getting_big_score > 0:
                self.getting_big_score -= 1
                self.score += 1
            else:
                self.snake_body.pop()
            if self.big_food_time_left > 0:
                if ((self.snake_pos[0] == self.big_food_pos[0]
                     and self.snake_pos[1] == self.big_food_pos[1])
                        or (self.snake_pos[0] == self.big_food_pos[0] + 10
                            and self.snake_pos[1] == self.big_food_pos[1])
                        or (self.snake_pos[0] == self.big_food_pos[0]
                            and self.snake_pos[1] == self.big_food_pos[1] + 10)
                        or (self.snake_pos[0] == self.big_food_pos[0] + 10
                            and self.snake_pos[1] == self.big_food_pos[1] + 10)):
                    self.getting_big_score = self.big_food_score
                    self.big_food_time_left = 0
                    self.big_food_pos = [0, 0]

            # Getting out of bounds
            if self.snake_pos[0] < 0:
                self.snake_pos[0] = self.frame_size_x - 10
            if self.snake_pos[0] > self.frame_size_x - 10:
                self.snake_pos[0] = 0
            if self.snake_pos[1] < 0:
                self.snake_pos[1] = self.frame_size_y - 10
            if self.snake_pos[1] > self.frame_size_y - 10:
                self.snake_pos[1] = 0

            # Game Over condition
            # Touching the snake body
            for block in self.snake_body[1:]:
                if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                    self.game_over()

            # Show score
            rect = self.show_score(draw=False)
            self.eating_score = False
            # Decrease score if snake is in score box
            if self.score > 0 and self.snake_pos[0] - rect[0] in range(
                    rect[2]) and self.snake_pos[1] - rect[1] in range(rect[3]):
                self.eating_score = True
                self.show_score(color=RED)
                self.show_eating_score(color=RED)
                self.score -= 1
                self.snake_body.pop()

            # Set difficulty
            self.current_difficulty = (
                self.score * self.difficulty_modifier + self.base_difficulty
            )

            # Spawning food on the screen
            if not self.food_spawn:
                self.food_pos = [
                    random.randrange(1, self.frame_size_x // 10) * 10,
                    random
                    .randrange(1 +
                               (rect[1] + rect[3]) // 10, self.frame_size_y // 10) * 10
                ]
                self.food_spawn = True

            if self.eating_score:
                time.sleep(1 / self.base_difficulty)
            else:
                time.sleep(1 / self.current_difficulty)

    def big_food_handler(self):
        """Spawn big food every few seconds."""
        while self.__running:
            if self.change_to == 'PAUSE':
                time.sleep(self.tick)
                continue

            if self.big_food_time_left > 0:
                self.big_food_time_left -= 0.1
                time.sleep(0.1)
                continue

            spawn_big_food = random.random() <= self.big_food_chance
            if spawn_big_food:
                rect = self.show_score(draw=False)
                self.big_food_pos = [
                    random.randrange(1, self.frame_size_x // 20) * 20,
                    random
                    .randrange(1 +
                               (rect[1] + rect[3]) // 20, self.frame_size_y // 20) * 20
                ]

                self.big_food_pos[0] += 10
                if self.big_food_pos[0] > self.frame_size_x - 10:
                    self.big_food_pos[0] = 0

                self.big_food_time_left = self.big_food_time

            time.sleep(1)

    def run(self):
        """Run the game."""
        threads = []
        self.__running = True
        threads.append(Thread(target=self.__run, daemon=True))
        threads[-1].start()
        if 0 < self.big_food_chance < 1:
            threads.append(Thread(target=self.big_food_handler, daemon=True))
            threads[-1].start()

        self.main_loop()
        self.__running = False
        for thread in threads:
            thread.join()

    @property
    def fps(self) -> int:
        """Get the number of frames per second."""
        return self.__fps

    @fps.setter
    def fps(self, value: int):
        self.__fps = value
        self.__tick = 1 / value

    @property
    def tick(self) -> float:
        """Get the time between each frame."""
        return self.__tick

    def __del__(self):
        pygame.quit()


if __name__ == '__main__':
    game = SnakeGame(
        frame_size_x=1080,
        frame_size_y=720,
        base_difficulty=10,
        difficulty_modifier=2,
        fps=144,
    )
    game.run()