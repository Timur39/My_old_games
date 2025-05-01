import pygame
import random
from os import path

HP = 100
W = 480
H = 600
FPS = 60
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Starship VS Meteor!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font("arial")


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Ты проиграл:(", 64, W / 2, H / 4)
    draw_text(screen, "Нажмите любую кномку для новой игры", 22,
              W / 2, H / 2)
    draw_text(screen, "Не расстраивайся:)", 18, W / 2, H * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYUP:
                waiting = False


def win_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Ты победил:)", 64, W / 2, H / 4)
    draw_text(screen, "Нажми R для новой игры", 22,
              W / 2, H / 2)
    draw_text(screen, "Радуйся:)", 18, W / 2, H * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
            if events.type == pygame.K_r:
                waiting = False


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player2_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 35
        self.rect.centerx = W / 2
        self.rect.bottom = H - 500
        self.speedx = 0
        self.speedy = 0
        self.shield = HP
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (W / 2, H + 200)

    def update(self):
        # тайм-аут для бонусов
        powerup_time = 5000
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > powerup_time:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > powerup_time:
            self.power -= 100
            self.power_time = pygame.time.get_ticks()

        # показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = W / 2
            self.rect.bottom = H - 500
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_DOWN]:
            self.shoot()
        self.rect.x += self.speedx
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > W:
            self.rect.right = W
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
         now = pygame.time.get_ticks()
         if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet2(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets2.add(bullet)
                shoot_sound.play()
            if self.power >= 2 and self.power < 3:
                bullet1 = Bullet2(self.rect.left, self.rect.centery)
                bullet2 = Bullet2(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets2.add(bullet1)
                bullets2.add(bullet2)
                shoot_sound.play()
            if self.power >= 3:
                bullet1 = Bullet2(self.rect.left, self.rect.centery)
                bullet2 = Bullet2(self.rect.right, self.rect.centery)
                bullet3 = Bullet2(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets2.add(bullet1)
                bullets2.add(bullet2)
                bullets2.add(bullet3)
                shoot_sound.play()


# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 35
        self.rect.centerx = W / 2
        self.rect.bottom = H - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = HP
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (W / 2, H + 200)

    def update(self):
        # тайм-аут для бонусов
        powerup_time = 5000
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > powerup_time:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > powerup_time:
            self.power -= 100
            self.power_time = pygame.time.get_ticks()

        # показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = W / 2
            self.rect.bottom = H - 10
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -8
        if keystate[pygame.K_d]:
            self.speedx = 8
        if keystate[pygame.K_w]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > W:
            self.rect.right = W
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
         now = pygame.time.get_ticks()
         if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2 and self.power < 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                bullet3 = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


class Bullet2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['gun', 'shield'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # убить, если он сдвинется с нижней части экрана
        if self.rect.top > H:
            self.kill()


class Pow2(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['gun', 'shield'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y -= self.speedy
        # убить, если он сдвинется с нижней части экрана
        if self.rect.top > H:
            self.kill()


# настройка папки ассетов
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'img')
snd_folder = path.join(game_folder, 'snd')
heart_img = pygame.image.load(path.join(img_folder, "heart.png"))
player_img = pygame.image.load(path.join(img_folder, "playerShip1_orange.png "))
player2_img = pygame.image.load(path.join(img_folder, "playerShip2_orange.png "))
bullet_img = pygame.image.load(path.join(img_folder, "laserRed16.png"))
background = pygame.image.load(path.join(img_folder, "starfield.png"))
background_rect = background.get_rect()
shoot_sound = pygame.mixer.Sound(path.join(snd_folder, 'pew.wav'))
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim["sm"].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_folder, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_folder, 'bolt_gold.png')).convert()
# Загрузка мелодий игры
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_folder, snd)))
pygame.mixer.music.load(path.join(snd_folder, "tgfcoder-FrozenJam-SeamlessLoop.mp3"))
pygame.mixer.music.set_volume(0.4)
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
heart_mini_img = pygame.transform.scale(heart_img, (26, 23))
heart_mini_img.set_colorkey(BLACK)
power_sound = pygame.mixer.Sound(path.join(snd_folder, 'power_sound.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_folder, 'shield_sound.wav'))

# Цикл игры
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        bullets2 = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        player2 = Player2()
        all_sprites.add(player)
        all_sprites.add(player2)
        score = 0
        score2 = 0
        pygame.mixer.music.play(loops=-1)
    if score >= 2000 or score2 >= 2000:
        win_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        bullets2 = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        player2 = Player2()
        all_sprites.add(player)
        all_sprites.add(player2)
        score = 0
        score2 = 0
        pygame.mixer.music.play(loops=-1)

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()

    # проверьте, не попала ли пуля в противника
    hits = pygame.sprite.spritecollide(player, bullets2, True, pygame.sprite.collide_circle)
    for hit in hits:
        score += 50
        player.shield -= 10
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.8:
            pow = Pow2(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # проверьте, не попала ли пуля в противника
    hits = pygame.sprite.spritecollide(player2, bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        score2 += 50
        player2.shield -= 10
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.8:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        if player2.shield <= 0:
            death_explosion = Explosion(player2.rect.center, 'player')
            all_sprites.add(death_explosion)
            player2.hide()
            player2.lives -= 1
            player2.shield = 100
    # Проверка столкновений игрока и улучшения
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()
    # Проверка столкновений игрока и улучшения
    hits = pygame.sprite.spritecollide(player2, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player2.shield += random.randrange(10, 30)
            if player2.shield >= 100:
                player2.shield = 100
        if hit.type == 'gun':
            player2.powerup()
            power_sound.play()

    # Если игрок умер, игра окончена
    if player.lives <= 0:
        game_over = True
        print('Умер игрок номер 1')
        print('Победил игрок номер 2')
    if player2.lives <= 0:
        game_over = True
        print('Умер игрок номер 2')
        print('Победил игрок номер 1')

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score2), 18, W / 2, 6)
    draw_text(screen, str(score), 18, W / 2, 25)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_shield_bar(screen, 5, 20, player2.shield)
    draw_lives(screen, W - 100, 5, player.lives,
               heart_mini_img)
    draw_lives(screen, W - 100, 30, player2.lives,
               heart_mini_img)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
