import pygame
import random
from os import path

pygame.init()

WHITE = (255, 255, 255)
YELLOW= (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

W = 800
H = 600
FPS = 30
pygame.mixer.init()
dis = pygame.display.set_mode((W, H))
pygame.display.set_caption("Змейка")
Clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont('"comicsansms', 35)


def your_score(score):
    value = score_font.render("Ваш счёт:" + str(score), True, BLACK)
    dis.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, BLUE, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [W / 3, H / 3])


def message2(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [W / 6, H / 2])

def gameloop():
    game_over = False
    game_close = False
    x1 = W / 2
    y1 = H / 2
    x_sneak = 0
    y_sneak = 0
    snake_list = []
    length_of_snake = 1
    foodx = round(random.randrange(0, W - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, W - snake_block) / 10.0) * 10.0
    # Управление змейкой
    while not game_over:
        while game_close == True:
            dis.fill(GREEN)
            message("Вы проиграли :(", RED)
            message2("Нажмите Q для выхода или R для повторной игры", RED)
            your_score(length_of_snake - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        gameloop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_sneak = -snake_block
                    y_sneak = 0
                elif event.key == pygame.K_d:
                    x_sneak = snake_block
                    y_sneak = 0
                elif event.key == pygame.K_w:
                    y_sneak = -snake_block
                    x_sneak = 0
                elif event.key == pygame.K_s:
                    y_sneak = snake_block
                    x_sneak = 0
        if x1 >= W or x1 < 0 or y1 >= H or y1 < 0:
            game_close = True
        x1 += x_sneak
        y1 += y_sneak
        dis.fill(GREEN)
        pygame.draw.rect(dis, RED, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_list.append(snake_Head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]
        for x in snake_list[:-1]:
            if x == snake_Head:
                game_close = True
        our_snake(snake_block, snake_list)
        your_score(length_of_snake - 1)
        pygame.display.update()
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, W - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, H - snake_block) / 10.0) * 10.0
            length_of_snake += 1
        Clock.tick(snake_speed)

    pygame.quit()
    quit()
gameloop()
