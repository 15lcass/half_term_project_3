import pygame

pygame.init()

DISPLAY = pygame.display.set_mode([800, 600])
FPSCLOCK = pygame.time.Clock()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
left = 50
top = 50
width = 10
height = 40

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    DISPLAY.fill(BLACK)

    pygame.draw.rect(DISPLAY, WHITE, [left, top, width, height])

    left += 5
    top += 5

    pygame.display.update()
    FPSCLOCK.tick(30)