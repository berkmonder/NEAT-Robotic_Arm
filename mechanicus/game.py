import pygame, math
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mechanicus")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 75, 75)
BLUE = (75, 75, 200)
GREEN = (75, 200, 75)

class Arm:
    # COLOR = BLUE
    VEL = .02

    def __init__(self, length, color):
        self.length = length
        self.color = color
        self.x0 = WIDTH/2
        self.y0 = HEIGHT/2
        self.theta = 0
        self.fixed = False

    def draw(self, win, x_orig=None, y_orig=None):
        x0, y0 = self.x0, self.y0
        if not self.fixed:
            x0, y0 = x_orig, y_orig
        x, y = x0 + self.length * math.cos(self.theta), y0 + self.length * math.sin(self.theta)

        pygame.draw.line(win, self.color, (x0, y0), (x, y), 2)
        pygame.draw.circle(win, self.color, (x, y), 5)
        return x, y

    def rotate(self, clockwise=True):
        if clockwise:
            self.theta += self.VEL
        else:
            self.theta -= self.VEL

        print(math.cos(self.theta))


def draw(win, arms):
    win.fill(BLACK)

    x = 0
    y = 0
    for arm in arms:
        x, y = arm.draw(win, x, y)

    number_of_arms = len(arms)
    pygame.draw.circle(win, RED, [WIDTH/2, HEIGHT/2], number_of_arms * arm.length, 2)

    pygame.display.update()

def handle_arm_rotation(keys, *args):
    for i, arg in enumerate(args):
        if keys[pygame.K_l]:
            if keys[pygame.K_1] and i >= 0:
                arg.rotate(clockwise=True)
            if keys[pygame.K_2] and i >= 1:
                arg.rotate(clockwise=True)
            if keys[pygame.K_3] and i >= 2:
                arg.rotate(clockwise=True)
        if keys[pygame.K_h]:
            if keys[pygame.K_1] and i >= 0:
                arg.rotate(clockwise=False)
            if keys[pygame.K_2] and i >= 1:
                arg.rotate(clockwise=False)
            if keys[pygame.K_3] and i >= 2:
                arg.rotate(clockwise=False)


def main():
    run = True
    clock = pygame.time.Clock()

    arm1 = Arm(100, RED)
    arm1.fixed = True
    arm2 = Arm(100, BLUE)
    arm3 = Arm(100, GREEN)

    while run:
        clock.tick(FPS)
        draw(WIN, [arm1, arm2, arm3])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_arm_rotation(keys, arm1, arm2, arm3)

    pygame.quit()

if __name__ == '__main__':
    main()