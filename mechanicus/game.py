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
    VEL = 1

    def __init__(self, x0, y0, length, theta, color):
        self.x0 = x0
        self.y0 = y0
        self.length = length
        self.theta = theta
        self.color = color

    def draw(self, win):
        x0, y0 = self.x0, self.y0
        x, y = x0 + self.length * math.cos(self.theta), y0 + self.length * math.sin(self.theta)

        pygame.draw.line(win, self.color, (x0, y0), (x, y), 2)

    def rotate(self, clockwise=True):
        if clockwise:
            self.theta += self.VEL
        else:
            self.theta -= self.VEL

        print(math.cos(self.theta))


def draw(win, arms):
    win.fill(BLACK)

    for arm in arms:
        arm.draw(win)

    number_of_arms = len(arms)
    pygame.draw.circle(win, RED, [WIDTH/2, HEIGHT/2], number_of_arms * arm.length, 2)

    pygame.display.update()

def handle_arm_rotation(keys, *args):
    if keys[pygame.K_1]:
        if keys[pygame.K_l]:
            args[0].rotate(clockwise=True)
        if keys[pygame.K_h]:
            args[0].rotate(clockwise=False)
    if keys[pygame.K_2]:
        if keys[pygame.K_l]:
            args[1].rotate(clockwise=True)
        if keys[pygame.K_h]:
            args[1].rotate(clockwise=False)
    if keys[pygame.K_3]:
        if keys[pygame.K_l]:
            args[2].rotate(clockwise=True)
        if keys[pygame.K_h]:
            args[2].rotate(clockwise=False)


def main():
    run = True
    clock = pygame.time.Clock()

    arm1 = Arm(HEIGHT/2, WIDTH/2, 100, 0, RED)
    arm2 = Arm(HEIGHT/2, WIDTH/2, 100, 90, BLUE)
    arm3 = Arm(HEIGHT/2, WIDTH/2, 100, 180, GREEN)

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