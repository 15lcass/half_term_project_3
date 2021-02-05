import pygame

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

        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50


    def collide_hostile_check(self, hostile_group):  # check if collided with voldy

        collided_hostiles = []
        collided = False

        for hostile in hostile_group:
            if self.rect.colliderect(hostile.rect):
                collided_hostiles.append(hostile)
                collided = True

        return (collided, collided_hostiles)


    '''def collide_wall_check(self, wall_group, direction):  # how to make walls?
        return (False, None)'''

    def damage_or_healing(self, amount):
        self.current_health += amount  # takes damage / adds healing to current health
        if self.current_health <= 0:  # dead
            return False
        else:
            return True


    def update(self, direction=None): #hostile_group, wall_group, direction):
        if direction == 'left':
            self.rect.x -= self.move_speed
        if direction == 'right':
            self.rect.x += self.move_speed
        if direction == 'up':
            self.rect.y -= self.move_speed
        if direction == 'down':
            self.rect.y += self.move_speed


class Voldemort(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.current_health = 10
        self.move_speed = 10

        self.image = pygame.Surface([20, 20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()


    def collide_hostile_check(self, hostile_group):  # checks if collided with potter

        collided_hostiles = []
        collided = False

        for hostile in hostile_group:
            if self.rect.colliderect(hostile.rect):
                collided_hostiles.append(hostile)
                collided = True

        return (collided, collided_hostiles)


    '''def collide_wall_check(self, wall_group, direction):
            return (False, None)'''

    def update(self, hostile_group, wall_group, direction):  ####
        collided = self.collide_hostile_check(hostile_group)[0]
        collided_hostiles = self.collide_hostile_check(hostile_group)[1]

        if collided:
            if 'HarryPotter' in collided_hostiles:  # this is wrong
                self.current_health -= 1
            #if 'Attack' in collided_hostiles:
                #self.current_health -=



class Attack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.damage = 5
        self.mode = 'melee'
        self.count = 0
        self.move_speed = 0
        self.direction = None

        self.image = pygame.Surface([50, 50])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50


    def collide_hostile_check(self, hostile_group):  # checks if collided with character

        for hostile in hostile_group:
            if self.rect.colliderect(hostile.rect):
                hostile.kill()  ###
                self.kill()


    def update(self):  # is this necessary for a melee attack?
        pass



harry_potter = HarryPotter()  # create harry potter and put him in good group
all_sprites = pygame.sprite.Group()
all_sprites.add(harry_potter)
good_group = pygame.sprite.Group()
good_group.add(harry_potter)

voldemort = Voldemort()  # create voldy and put him in bad group
all_sprites.add(voldemort)
bad_group = pygame.sprite.Group()
bad_group.add(voldemort)

my_attack = Attack()
attacks = pygame.sprite.Group()
attacks.add(my_attack)

direction = None


while True:

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
                attacks.draw(DISPLAY)  # why does this not work

            harry_potter.update(direction)


        '''if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                print('left stop')
            if event.key == pygame.K_RIGHT:
                print('right stop')
            if event.key == pygame.K_UP:
                print('up stop')
            if event.key == pygame.K_DOWN:
                print('down stop')'''

    print(HarryPotter.collide_hostile_check(harry_potter, bad_group))
    print(Voldemort.collide_hostile_check(voldemort, good_group))


    DISPLAY.fill(BLACK)

    all_sprites.draw(DISPLAY)

    pygame.display.update()
    FPSCLOCK.tick(30)