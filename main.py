import pygame
import random

pygame.init()

WINDOWWIDTH = 800
WINDOWHEIGHT = 600

DISPLAY = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])
FPSCLOCK = pygame.time.Clock()

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class HarryPotter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.max_health = 5
        self.attack_damage = 2
        self.move_speed = 20
        self.name = 'HarryPotter'
        self.current_health = self.max_health

        self.image = pygame.Surface([30, 30])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOWWIDTH)
        self.rect.y = random.randint(0, WINDOWHEIGHT)


    def collide_hostile_check(self, hostile_group):  # check if collided with voldy

        collided_hostiles = []
        collided = False

        for hostile in hostile_group:
            if self.rect.colliderect(hostile.rect):
                collided_hostiles.append(hostile)
                collided = True

        return (collided, collided_hostiles)


    def collide_wall_check(self, wall_group):
        for wall in wall_group:
            if self.rect.colliderect(wall.rect):
                return (True, wall)

        return (False, None)


    def damage_or_healing(self, amount):
        self.current_health += amount  # takes damage / adds healing to current health
        if self.current_health <= 0:  # dead
            self.kill()
            print('Harry Potter is dead.')
            return False
        else:
            return True


    def update(self, direction, wall_group):


        collided = harry_potter.collide_wall_check(wall_group)[0]
        wall = harry_potter.collide_wall_check(wall_group)[1]

        if not collided:  # moves if not collided with walls
            if direction == 'left':
                self.rect.x -= self.move_speed
            if direction == 'right':
                self.rect.x += self.move_speed
            if direction == 'up':
                self.rect.y -= self.move_speed
            if direction == 'down':
                self.rect.y += self.move_speed

        else:  # if collided, does not move into wall in that direction
            if direction == 'left' and wall.name != 'wall_left':
                self.rect.x -= self.move_speed
            if direction == 'right' and wall.name != 'wall_right':
                self.rect.x += self.move_speed
            if direction == 'up' and wall.name != 'wall_up':
                self.rect.y -= self.move_speed
            if direction == 'down' and wall.name != 'wall_down':
                self.rect.y += self.move_speed

        collided = harry_potter.collide_hostile_check(bad_group)[0]
        collided_hostiles = harry_potter.collide_hostile_check(bad_group)[1]

        if collided:
            for hostile in collided_hostiles:
                if hostile.name == 'Voldemort':
                    self.damage_or_healing(-2)



class Voldemort(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.name = 'Voldemort'
        self.current_health = 10
        self.move_speed = 1

        self.image = pygame.Surface([30, 30])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOWWIDTH)
        self.rect.y = random.randint(0, WINDOWHEIGHT)


    def collide_hostile_check(self, hostile_group):  # checks if collided with potter

        collided_hostiles = []
        collided = False

        for hostile in hostile_group:
            if self.rect.colliderect(hostile.rect):
                collided_hostiles.append(hostile)
                collided = True

        return (collided, collided_hostiles)


    def collide_wall_check(self, wall_group, direction):
        for wall in wall_group:
            if self.rect.colliderect(wall.rect):
                return (True, wall)

        return (False, None)


    def update(self, hostile_group, wall_group=None, direction=None):  ####
        collided = self.collide_hostile_check(hostile_group)[0]
        collided_hostiles = self.collide_hostile_check(hostile_group)[1]

        if collided:
            for hostile in collided_hostiles:
                if hostile.name == 'HarryPotter':  # if collided with harry, kill voldy
                    self.kill()
                else:
                    self.current_health -= my_attack.damage  # if attacked, remove damage

        if self.current_health <= 0:
            self.kill()

        if self.rect.x <= harry_potter.rect.x:  # enemy moves towards player
            self.rect.x += self.move_speed
        elif self.rect.x >= harry_potter.rect.x:
            self.rect.x -= self.move_speed
        if self.rect.y <= harry_potter.rect.y:
            self.rect.y += self.move_speed
        elif self.rect.y >= harry_potter.rect.y:
            self.rect.y -= self.move_speed



class Attack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.name = 'Expelliarmus'
        self.damage = 1
        self.mode = 'melee'
        self.count = 0
        self.move_speed = 0
        self.direction = None

        self.image = pygame.Surface([70, 70])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = harry_potter.rect.x - 20
        self.rect.y = harry_potter.rect.y - 20


    def collide_hostile_check(self, hostile_group):  # checks if collided with character

        for hostile in hostile_group:
            if self.rect.colliderect(hostile.rect):
                self.kill()  # kill attack sprite if collided


class Wall(pygame.sprite.Sprite):
    def __init__(self, name, width, height, x_pos, y_pos):
        super().__init__()

        self.name = name
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos


all_sprites = pygame.sprite.Group()
good_group = pygame.sprite.Group()
bad_group = pygame.sprite.Group()

wall_group = pygame.sprite.Group()  # make walls

wall_up = Wall('wall_up', 800, 1, 0, -1)
wall_group.add(wall_up)
wall_down = Wall('wall_down', 800, 1, 0, 600)
wall_group.add(wall_down)
wall_left = Wall('wall_left', 1, 600, -1, 0)
wall_group.add(wall_left)
wall_right = Wall('wall_right', 1, 600, 800, 0)
wall_group.add(wall_right)

all_sprites.add(wall_up)
all_sprites.add(wall_down)
all_sprites.add(wall_left)
all_sprites.add(wall_right)

direction = None

while True:
    DISPLAY.fill(BLACK)

    if len(good_group) == 0:  # create harry potter and put him in good group
        harry_potter = HarryPotter()
        all_sprites.add(harry_potter)
        good_group.add(harry_potter)

    if len(bad_group) == 0:
        voldemort = Voldemort()  # create voldy and put him in bad group
        all_sprites.add(voldemort)
        bad_group.add(voldemort)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = 'left'
            if event.key == pygame.K_RIGHT:
                direction = 'right'
            if event.key == pygame.K_UP:
                direction = 'up'
            if event.key == pygame.K_DOWN:
                direction = 'down'
            if event.key == pygame.K_SPACE:
                my_attack = Attack()
                attacks = pygame.sprite.Group()
                attacks.add(my_attack)
                good_group.add(my_attack)
                attacks.draw(DISPLAY)

            harry_potter.update(direction, wall_group)

    all_sprites.draw(DISPLAY)
    Voldemort.update(voldemort, good_group)


    pygame.display.update()
    FPSCLOCK.tick(30)