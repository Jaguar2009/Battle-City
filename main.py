import pygame
from pygame import QUIT, KEYDOWN, K_ESCAPE, display
from random import randint


pygame.init()

info = pygame.display.Info()

clock = pygame.time.Clock()
FPS = 60

WIDTH = info.current_w
HEIGHT = info.current_h

window = pygame.display.set_mode((WIDTH, HEIGHT))
display.set_caption("Battle City")

image_tank = pygame.image.load("image/tank-battle-city.png")
image_bullet = pygame.image.load("image/pulya.jpg")
image_block = pygame.image.load("image/baby.png")

font_information = pygame.font.Font(None, 30)

Direct = [[0, -1], [-1, 0], [0, 1], [1, 0]]


class Tank:
    def __init__(self, player, width, height, speed, health, x, y, direct, keylist):
        objects.append(self)
        self.type = "Tank"
        self.player = player
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image_tank, (width, height))
        self.image_tank = pygame.transform.rotate(self.image, direct * 90)
        self.direct = direct
        self.speed = speed
        self.health = health

        self.bulletDamage = 1
        self.bulletSpeed = 5
        self.timer = 0
        self.delay = 60

        self.keyLEFT = keylist[0]
        self.keyRIGHT = keylist[1]
        self.keyUP = keylist[2]
        self.keyDOWN = keylist[3]
        self.keySHOT = keylist[4]

    def update(self):
        self.image = self.image = pygame.transform.rotate((self.image_tank), self.direct * 90)
        old_x, old_y = self.rect.topleft

        if keys[self.keyUP] and self.rect.y > 0:
            self.rect.y -= self.speed
            self.direct = 0
        if keys[self.keyDOWN] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed
            self.direct = 2
        if keys[self.keyLEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.direct = 1
        if keys[self.keyRIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed
            self.direct = 3
        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = old_x, old_y


        if keys[self.keySHOT] and self.timer == 0:
            direct_x = Direct[self.direct][0] * self.bulletSpeed
            direct_y = Direct[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, direct_x, direct_y, self.bulletDamage, 50, 50, self.direct)
            self.timer = self.delay

        if self.timer > 0:
            self.timer -= 1

    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.health -= value
        if self.speed >= HEIGHT/1500:
            self.speed -= HEIGHT/1750
            self.delay += 40
        if self.health <= 0:
            objects.remove(self)


class Bullet:
    def __init__(self, parent, x, y, direct_x, direct_y, damage, width, height, start_direct):
        bullets.append(self)
        self.parent = parent
        self.x = x - width//2
        self.y = y - height//2
        self.direct_x = direct_x
        self.direct_y = direct_y
        self.damage = damage
        self.image = pygame.transform.scale(image_bullet, (width, height))
        self.start_direct = start_direct

        if self.start_direct == 0:
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.start_direct == 1:
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.start_direct == 2:
            self.image = pygame.transform.rotate(self.image, -90)
        elif self.start_direct == 3:
            self.image = pygame.transform.rotate(self.image, 0)

    def update(self):
        self.x += self.direct_x
        self.y += self.direct_y

        if self.x < -50 or self.x > WIDTH or self.y < -50 or self.y > HEIGHT:
            bullets.remove(self)

        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.x, self.y):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break

    def draw(self):
        window.blit(self.image, (self.x, self.y))


class Block:
    def __init__(self, x, y, size, health):
        objects.append(self)
        self.type = "Block"
        self.rect = pygame.Rect(x, y, size, size)
        self.health = health
        self.image = pygame.transform.scale(image_block, (size, size))
        self.x = x
        self.y = y

    def update(self):
        pass

    def draw(self):
        window.blit(self.image, (self.x, self.y))

    def damage(self, value):
        self.health -= value
        if self.health <= 0:
            objects.remove(self)


class Information:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        count = 0
        for obj in objects:
            if obj.type == "Tank":
                text_player = font_information.render("Player" + str(obj.player) + ": ", 1, "white")
                rect_player = text_player.get_rect(center=(50 + count * 200, 15))

                text = font_information.render(str(obj.health), 1, "white")
                rect = text.get_rect(center=(70 + count * 200 + 32, 5 + 11))

                window.blit(text, rect)
                window.blit(text_player, rect_player)
                count += 1



bullets = []
objects = []

Tank(1, HEIGHT // 10, HEIGHT // 10, HEIGHT // 300, 10, 100, 100, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank(2, HEIGHT // 10, HEIGHT // 10, HEIGHT // 300, 10, 200, 200, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_m))
information = Information()

for i in range(randint(40, 80)):
    while True:
        x = randint(0, WIDTH // (HEIGHT // 10) - 1) * HEIGHT // 10
        y = randint(1, HEIGHT // (HEIGHT // 10) - 1) * HEIGHT // 10
        rect = pygame.Rect(x, y, HEIGHT // 10, HEIGHT // 10)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect):
                fined = True
        if not fined:
            break

    Block(x, y, HEIGHT // 10, 1)


game = True

while game:
    for event in pygame.event.get():
        if event.type == QUIT:
            game = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game = False

    window.fill('black')

    keys = pygame.key.get_pressed()

    for bul in bullets:
        bul.update()

    for obj in objects:
        obj.update()

    information.update()

    for bul in bullets:
        bul.draw()

    for obj in objects:
        obj.draw()

    information.draw()



    pygame.display.update()
    clock.tick(FPS)