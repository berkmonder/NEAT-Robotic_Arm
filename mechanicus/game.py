from .arm import Arm
from .food import Food
import pygame, math
pygame.init()

class GameInformation:
    def __init__(self, score):
        self.score = score

class Game:
    pygame.display.set_caption("Mechanicus")
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    def __init__(self, window, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        self.arm = Arm(2, window_width//2, window_height//2)
        self.food = Food(window_width//2, window_height//2)

        self.window = window
        self.score = 0

    def _draw_circle(self):
        pygame.draw.circle(self.window, self.WHITE, (self.window_width//2, self.window_height//2),\
                           self.arm.MAX_RADIUS + self.arm.HEAD_RADIUS + 2, 2)

    def _draw_score(self):
        score_text = self.SCORE_FONT.render(f"Score: {self.score}", 1, self.WHITE)
        self.window.blit(score_text, (self.window_width//2 - score_text.get_width()//2, 10))

    def _draw_generation(self, gen):
        generation_text = self.SCORE_FONT.render(f"Gen: {gen}", 1, self.WHITE)
        self.window.blit(generation_text, (self.window_width//4 - generation_text.get_width()//2, 10))

    def _draw_number_of_arms(self, arm):
        number_of_arms_text = self.SCORE_FONT.render(f"Arms: {arm}", 1, self.WHITE)
        self.window.blit(number_of_arms_text, (3*self.window_width//4 - number_of_arms_text.get_width()//2, 10))

    def _handle_colission(self, arm, food, ge):
        if (arm.x[-1] < food.x + food.RADIUS + arm.HEAD_RADIUS and arm.x[-1] > food.x - food.RADIUS - arm.HEAD_RADIUS)\
            and (arm.y[-1] < food.y + food.RADIUS + arm.HEAD_RADIUS and arm.y[-1] > food.y - food.RADIUS - arm.HEAD_RADIUS):
            self.score += 1
            arm.score += 1
            food.reset()
            arm.time = 0
            ge.fitness += 10

    def _kill_lazy(self, arm):
        if arm.time > arm.max_time:
            return True

    def draw(self, arms, foods, gen=None):
        self.window.fill(self.BLACK)

        self._draw_circle()
        self._draw_score()
        self._draw_generation(gen)
        self._draw_number_of_arms(len(arms))

        for food in foods:
            food.draw(self.window)

        for arm in arms:
            arm.draw(self.window)
        
    def rotate_arm(self, arms, arm, clockwise=None):
        """
        Move the arms.

        :returns: boolean indicating if arm rotation is valid.
        """
        arms.rotate(arm, clockwise)

    def loop(self, nets, arms, foods, ge):
        """
        Executes a single game loop.

        :returns: GameInformation instance stating score.
        """
        for i, (arm, food, g) in enumerate(zip(arms, foods, ge)):
            self._handle_colission(arm, food, g)

            if self._kill_lazy(arm):
                arms.pop(i)
                foods.pop(i)
                nets.pop(i)
                ge.pop(i)

        game_info = GameInformation(self.score)

        return game_info

    def reset(self):
        pass
        # """Resets the entire game."""
        # self.score = 0
        # self.time = 0
        # self.food.reset()
        # for arm in self.arms:
        #     arm.reset()