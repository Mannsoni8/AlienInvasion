import pygame
import os
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 350, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Invasion")
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load images
BACKGROUND_IMAGE = pygame.image.load(r'C:\Users\hp\Downloads\AlienInvasion-main\AlienInvasion-main\images\background-black.png')
BACKGROUND_SCREEN = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

# Load sounds
SHOOT_SOUND = pygame.mixer.Sound(r'C:\Users\hp\Downloads\AlienInvasion-main\AlienInvasion-main\images\sniper-rifle-5989.mp3')
EXPLOSION_SOUND = pygame.mixer.Sound(r'C:\Users\hp\Downloads\AlienInvasion-main\AlienInvasion-main\images\explosion-sound-effect-1-free-on-gamesfxpackscom-241821.mp3')
SHIELD_ACTIVATION_SOUND = pygame.mixer.Sound(r'C:\Users\hp\Downloads\AlienInvasion-main\AlienInvasion-main\images\shield-block-shortsword-143940.mp3')
PLAYER_ELIMINATION_SOUND = pygame.mixer.Sound(r'C:\Users\hp\Downloads\AlienInvasion-main\AlienInvasion-main\images\kick-kill-83632.mp3')

class SpriteSheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename)

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

sprite_sheet = SpriteSheet(r'C:\Users\hp\Downloads\AlienInvasion-main\AlienInvasion-main\images\sprites.png')

class ShieldPowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.image = sprite_sheet.get_sprite(120, 0, self.width, self.height)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = 3

    def draw(self):
        WIN.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

    def update(self):
        self.y += self.speed
        self.rect.centery = self.y

class Enemy:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.width = 38
        self.height = 43
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.dx = 1
        self.dy = 1
        self.vel_x = 2
        self.vel_y = 1
        self.bullets = []
        self.shot_cooldown = 500
        self.last_shot_time = pygame.time.get_ticks()

    def draw(self):
        WIN.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

    def update(self):
        self.x += self.vel_x * self.dx
        self.y += self.vel_y
        self.rect.center = (self.x, self.y)

        if self.x - self.width / 2 < 0 or self.x + self.width / 2 > WIDTH:
            self.dx = -self.dx

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shot_cooldown:
            bullet = Bullet(self.x, self.y, 1)
            self.bullets.append(bullet)
            self.last_shot_time = current_time

class Bullet:
    def __init__(self, x, y, dy):
        self.x = x
        self.y = y
        self.dy = dy
        self.width = 3
        self.height = 20
        self.speed = 5
        self.image = sprite_sheet.get_sprite(0, 45, self.width, self.height)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        WIN.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

    def update(self):
        self.y += self.speed * self.dy
        self.rect.centery = self.y

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 38
        self.height = 43
        self.image = sprite_sheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.bullets = []
        self.is_alive = True
        self.shot_cooldown = 500
        self.last_shot_time = pygame.time.get_ticks()
        self.speed = 5
        self.shield_active = False  # Flag for shield status
        self.shield_timer = 0  # Timer for shield duration
        self.shield_duration = 5000  # Shield duration in milliseconds

    def draw(self):
        WIN.blit(self.image, (self.x - self.width / 2, self.y - self.height / 2))

        if self.shield_active:  # Draw shield when active
            pygame.draw.circle(WIN, BLUE, self.rect.center, self.width // 2, 3)  # Blue shield around player

            # Display shield timer as a countdown circle
            elapsed_time = pygame.time.get_ticks() - self.shield_timer
            remaining_time = max(0, self.shield_duration - elapsed_time)

            shield_time_percentage = remaining_time / self.shield_duration
            shield_time_color = (255 * (1 - shield_time_percentage), 255 * shield_time_percentage, 0)  # Color fades from green to red

            pygame.draw.arc(WIN, shield_time_color, self.rect, -1.5708, 1.5708, 5)  # Top arc
            pygame.draw.arc(WIN, shield_time_color, self.rect, 1.5708, 3.14159, 5)  # Bottom arc

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - self.width / 2 > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.width / 2 < WIDTH:
            self.x += self.speed

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shot_cooldown:
            bullet1 = Bullet(self.x - self.width / 3, self.y, -1)
            bullet2 = Bullet(self.x + self.width / 3, self.y, -1)
            self.bullets.append((bullet1, bullet2))
            self.last_shot_time = current_time
            SHOOT_SOUND.play()

    def update(self):
        if self.shield_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.shield_timer > self.shield_duration:  # Shield lasts for 5 seconds
                self.shield_active = False
        self.rect.center = (self.x, self.y)

# Additional Helper Functions
def spawn_shield_power_up():
    x = random.randint(20, WIDTH - 20)
    y = -30
    return ShieldPowerUp(x, y)

def draw_window():
    WIN.blit(BACKGROUND_SCREEN, (0, 0))

def draw_score(score, shield_active, shield_time_left):
    font = pygame.font.SysFont(None, 30)
    img = font.render(f"Score: {score}", True, WHITE)
    WIN.blit(img, (20, 20))

    # Display shield status and remaining time
    if shield_active:
        time_left_text = pygame.font.SysFont(None, 20).render(f"Shield Time: {shield_time_left // 1000}s", True, GREEN)
        WIN.blit(time_left_text, (WIDTH - time_left_text.get_width() - 20, 20))

def game_over_screen():
    PLAYER_ELIMINATION_SOUND.play()  # Play elimination sound
    font = pygame.font.SysFont(None, 50)
    img = font.render("GAME OVER", True, WHITE)
    WIN.blit(img, (WIDTH // 2 - img.get_width() // 2, HEIGHT // 2 - img.get_height() // 2))

    play_again_font = pygame.font.SysFont(None, 30)
    play_again_text = play_again_font.render("Press R to Play Again", True, WHITE)
    WIN.blit(play_again_text, (WIDTH // 2 - play_again_text.get_width() // 2, HEIGHT // 2 + 40))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False

def main():
    run = True
    clock = pygame.time.Clock()
    score = 0
    shield_power_ups = []

    player = Player(WIDTH // 2, HEIGHT - 60)
    enemies = []
    frames = 0

    while run:
        clock.tick(FPS)
        draw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        player.move(keys)
        if keys[pygame.K_SPACE]:
            player.shoot()

        for bullet1, bullet2 in player.bullets[:]:
            bullet1.update()
            bullet2.update()
            bullet1.draw()
            bullet2.draw()
            if bullet1.y < 0 or bullet2.y < 0:
                player.bullets.remove((bullet1, bullet2))

        if frames % 60 == 0:
            x = random.randint(20, WIDTH - 20)
            enemy = Enemy(x, -50, sprite_sheet.get_sprite(160, 0, 38, 43))
            enemies.append(enemy)

        if frames % 300 == 0:
            shield_power_ups.append(spawn_shield_power_up())

        for power_up in shield_power_ups[:]:
            power_up.update()
            power_up.draw()
            if power_up.y > HEIGHT:
                shield_power_ups.remove(power_up)
            if player.rect.colliderect(power_up.rect):
                SHIELD_ACTIVATION_SOUND.play()
                shield_power_ups.remove(power_up)
                player.shield_active = True
                player.shield_timer = pygame.time.get_ticks()  # Start shield timer

        for enemy in enemies[:]:
            enemy.update()
            enemy.draw()

            enemy.shoot()
            for bullet in enemy.bullets[:]:
                bullet.update()
                bullet.draw()
                if bullet.y > HEIGHT:
                    enemy.bullets.remove(bullet)
                if player.rect.colliderect(bullet.rect) and not player.shield_active:
                    player.is_alive = False
            if player.rect.colliderect(enemy.rect) and not player.shield_active:
                player.is_alive = False
            for bullet1, bullet2 in player.bullets[:]:
                if enemy.rect.colliderect(bullet1.rect) or enemy.rect.colliderect(bullet2.rect):
                    enemies.remove(enemy)
                    player.bullets.remove((bullet1, bullet2))
                    score += 10
                    EXPLOSION_SOUND.play()

        if not player.is_alive:
            game_over_screen()
            main()
            return

        player.draw()
        player.update()
        shield_time_left = pygame.time.get_ticks() - player.shield_timer
        draw_score(score, player.shield_active, player.shield_duration - shield_time_left)
        pygame.display.update()
        frames += 1

    pygame.quit()

main()
