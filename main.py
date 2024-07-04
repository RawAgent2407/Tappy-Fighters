import pygame
import os

pygame.font.init()
pygame.mixer.init()

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
VEL = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
BULLET_VEL = 7
MAX_BULLETS = 3
b_HIT = pygame.USEREVENT + 1
a_HIT = pygame.USEREVENT + 2

b_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_b.png'))
b_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(b_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

a_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_a.png'))
a_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(a_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(a, b, b_bullets, a_bullets, b_health, a_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    a_health_text = HEALTH_FONT.render("Health: " + str(a_health), 1, WHITE)
    b_health_text = HEALTH_FONT.render("Health: " + str(b_health), 1, WHITE)
    WIN.blit(a_health_text, (WIDTH - a_health_text.get_width() - 10, 10))
    WIN.blit(b_health_text, (10, 10))

    WIN.blit(b_SPACESHIP, (b.x, b.y))
    WIN.blit(a_SPACESHIP, (a.x, a.y))
    for bullet in a_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in b_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def b_change(keys_pressed, b):
    if keys_pressed[pygame.K_a] and b.x - VEL > 0:
        b.x -= VEL
    if keys_pressed[pygame.K_d] and b.x + VEL + b.width < BORDER.x:
        b.x += VEL
    if keys_pressed[pygame.K_w] and b.y - VEL > 0:
        b.y -= VEL
    if keys_pressed[pygame.K_s] and b.y + VEL + b.height < HEIGHT - 13:
        b.y += VEL


def a_change(keys_pressed, a):
    if keys_pressed[pygame.K_UP] and a.y - VEL > 0:
        a.y -= VEL
    if keys_pressed[pygame.K_DOWN] and a.y + VEL + a.height < HEIGHT - 13:
        a.y += VEL
    if keys_pressed[pygame.K_LEFT] and a.x - VEL > BORDER.x + BORDER.width:
        a.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and a.x + VEL + a.width < WIDTH:
        a.x += VEL


def handle_bullets(b_bullets, a_bullets, b, a):
    for bullet in b_bullets:
        bullet.x += BULLET_VEL
        if a.colliderect(bullet):
            pygame.event.post(pygame.event.Event(a_HIT))
            b_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            b_bullets.remove(bullet)

    for bullet in a_bullets:
        bullet.x -= BULLET_VEL
        if b.colliderect(bullet):
            pygame.event.post(pygame.event.Event(b_HIT))
            a_bullets.remove(bullet)
        elif bullet.x < 0:
            a_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    a = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    b = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    a_bullets = []
    b_bullets = []
    b_health = 10
    a_health = 10
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(b_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(b.x + b.width, b.y + b.height / 2 - 2, 10, 5)
                    b_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_KP0 and len(a_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(a.x, a.y + a.height / 2 - 2, 10, 5)
                    a_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == a_HIT:
                a_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == b_HIT:
                b_health -= 1
                BULLET_HIT_SOUND.play()

        t = ""
        if b_health <= 0:
            t = "RED WINS"
        if a_health <= 0:
            t = "YELLOW WINS"
        if t != "":
            draw_winner(t)
            break

        keys_pressed = pygame.key.get_pressed()
        b_change(keys_pressed, b)
        a_change(keys_pressed, a)
        handle_bullets(b_bullets, a_bullets, b, a)
        draw_window(a, b, b_bullets, a_bullets, b_health, a_health)

    main()


if __name__ == "__main__":
    main()
