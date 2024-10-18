import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 800

# Frame rate
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Sound Manager Class
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.jump_sound = pygame.mixer.Sound('jump.mp3')
        self.shoot_sound = pygame.mixer.Sound('shoot.mp3')
        self.collect_sound = pygame.mixer.Sound('collect.mp3')

    def play_jump(self):
        self.jump_sound.play()

    def play_shoot(self):
        self.shoot_sound.play()

    def play_collect(self):
        self.collect_sound.play()

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, sound_manager):
        super().__init__()
        self.sound_manager = sound_manager
        # Load sprite sheet and extract frames for animation
        self.sprite_sheet = pygame.image.load('player_spritesheet.png').convert_alpha()
        self.frames = self.extract_frames(self.sprite_sheet, 1, 4)  # Adjust rows and columns as needed

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 400

        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.5
        self.deceleration = 0.9
        self.max_speed = 7
        self.gravity = 1
        self.jump_power = -15
        self.is_jumping = False
        self.is_running = False
        self.current_frame = 0
        self.frame_counter = 0
        self.health = 100
        self.lives = 3
        self.facing_right = True

    def extract_frames(self, sprite_sheet, rows, columns):
        frame_width = sprite_sheet.get_width() // columns
        frame_height = sprite_sheet.get_height() // rows
        frames = []
        for row in range(rows):
            for col in range(columns):
                frame = sprite_sheet.subsurface(pygame.Rect(
                    col * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height))
                frames.append(frame)
        return frames

    def update(self):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_RIGHT]:
            self.velocity_x += self.acceleration
            self.is_running = True
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.velocity_x -= self.acceleration
            self.is_running = True
            self.facing_right = False
        else:
            self.velocity_x *= self.deceleration
            self.is_running = False

        # Clamp speed
        self.velocity_x = max(-self.max_speed, min(self.max_speed, self.velocity_x))

        # Jumping
        if not self.is_jumping and keys[pygame.K_SPACE]:
            self.is_jumping = True
            self.velocity_y = self.jump_power
            self.sound_manager.play_jump()

        # Apply gravity
        self.velocity_y += self.gravity

        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Floor collision
        if self.rect.y >= 400:
            self.rect.y = 400
            self.is_jumping = False
            self.velocity_y = 0

        # Update animation
        self.animate()

    def animate(self):
        if self.is_running:
            self.frame_counter += 1
            if self.frame_counter >= 5:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.frame_counter = 0
        else:
            self.current_frame = 0

        self.image = self.frames[self.current_frame]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def shoot(self):
        self.sound_manager.play_shoot()
        if self.facing_right:
            direction = 1
        else:
            direction = -1
        return Projectile(self.rect.centerx, self.rect.centery, direction)

# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load('bullet_image.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 10 * direction

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x > SCREEN_WIDTH + 50 or self.rect.x < -50:
            self.kill()

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('enemy_image.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 2
        self.chase_range = 300
        self.patrol_range = (x - 100, x + 100)
        self.health = 50

    def update(self, player):
        # Check distance to player
        distance_to_player = abs(player.rect.x - self.rect.x)

        if distance_to_player < self.chase_range:
            # Chase player
            if player.rect.x > self.rect.x:
                self.rect.x += self.speed_x
            else:
                self.rect.x -= self.speed_x
        else:
            # Patrol
            self.rect.x += self.speed_x
            if self.rect.x < self.patrol_range[0] or self.rect.x > self.patrol_range[1]:
                self.speed_x = -self.speed_x

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

# BossEnemy Class
class BossEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('boss_image.png').convert_alpha()
        self.health = 200
        self.speed_x = 1

# Collectible Class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, collectible_type, sound_manager):
        super().__init__()
        self.image = pygame.image.load(f'{collectible_type}_image.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collectible_type = collectible_type
        self.sound_manager = sound_manager

    def apply(self, player):
        if self.collectible_type == 'health':
            player.health = min(100, player.health + 20)
        elif self.collectible_type == 'extra_life':
            player.lives += 1
        self.sound_manager.play_collect()
        self.kill()

# ParallaxBackground Class
class ParallaxBackground:
    def __init__(self):
        self.background_layers = [
            pygame.image.load('background_layer4.png').convert()
            
        ]
        self.bg_positions = [0, 0, 0]
        self.layer_speeds = [0.2, 0.4, 0.6]

    def update(self, player_velocity_x):
        for i in range(len(self.bg_positions)):
            self.bg_positions[i] -= player_velocity_x * self.layer_speeds[i]
            # Loop the background images
            if self.bg_positions[i] <= -SCREEN_WIDTH:
                self.bg_positions[i] = 0

    def draw(self, screen):
        for i, bg in enumerate(self.background_layers):
            screen.blit(bg, (self.bg_positions[i], 0))
            screen.blit(bg, (self.bg_positions[i] + SCREEN_WIDTH, 0))

# Camera Class
class Camera:
    def __init__(self, width, height):
        self.camera_rect = pygame.Rect(0, 0, width, height)

    def apply(self, entity):
        return entity.rect.move(self.camera_rect.topleft)

    def update(self, target):
        x = -target.rect.x + int(SCREEN_WIDTH / 2)
        y = -target.rect.y + int(SCREEN_HEIGHT / 2)
        # Limit scrolling to the level size if necessary
        self.camera_rect = pygame.Rect(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)

    def smooth_update(self, target):
        x = -target.rect.x + int(SCREEN_WIDTH / 2)
        y = -target.rect.y + int(SCREEN_HEIGHT / 2)
        self.camera_rect.x += (x - self.camera_rect.x) * 0.1
        self.camera_rect.y += (y - self.camera_rect.y) * 0.1

# Function to load levels
def load_level(level_number, sound_manager):
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()

    if level_number == 1:
        enemies.add(Enemy(800, 400), Enemy(1200, 400))
        collectibles.add(
            Collectible(500, 400, 'health', sound_manager),
            Collectible(700, 400, 'extra_life', sound_manager)
        )
    elif level_number == 2:
        enemies.add(Enemy(800, 400), Enemy(1000, 400), Enemy(1200, 400))
        collectibles.add(
            Collectible(600, 400, 'health', sound_manager),
            Collectible(800, 400, 'extra_life', sound_manager)
        )
    elif level_number == 3:
        enemies.add(Enemy(800, 400), Enemy(1000, 400), BossEnemy(1500, 400))
        collectibles.add(
            Collectible(700, 400, 'health', sound_manager)
        )

    return enemies, collectibles

# Functions to display HUD
def display_score(screen, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

def display_health(screen, player):
    font = pygame.font.Font(None, 36)
    text = font.render(f'Health: {player.health}', True, WHITE)
    screen.blit(text, (10, 40))

def display_lives(screen, player):
    font = pygame.font.Font(None, 36)
    text = font.render(f'Lives: {player.lives}', True, WHITE)
    screen.blit(text, (10, 70))

# Main menu screen
def display_menu(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 72)
    title = font.render("Side-Scrolling Adventure", True, WHITE)
    screen.blit(title, (100, 150))

    font = pygame.font.Font(None, 36)
    play_text = font.render("Press ENTER to Play", True, WHITE)
    screen.blit(play_text, (250, 300))

    pygame.display.flip()

# Game over screen
def game_over_screen(screen):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 72)
    game_over = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over, (250, 150))

    font = pygame.font.Font(None, 36)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(restart_text, (200, 300))

    pygame.display.flip()

# Main Game Function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Side-Scrolling Adventure")
    clock = pygame.time.Clock()

    sound_manager = SoundManager()

    # Game states
    game_active = False
    game_over = False
    level_number = 1

    # Main Menu Loop
    while not game_active:
        display_menu(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True

    # Game Loop
    while True:
        # Reset game variables
        player = Player(sound_manager)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)

        projectiles = pygame.sprite.Group()
        enemies, collectibles = load_level(level_number, sound_manager)

        parallax_bg = ParallaxBackground()
        camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        score = 0
        game_over = False

        while not game_over:
            dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_f:
                        # Player shoots
                        projectile = player.shoot()
                        projectiles.add(projectile)
                        all_sprites.add(projectile)

            # Update entities
            player.update()
            projectiles.update()
            enemies.update(player)
            collectibles.update()
            parallax_bg.update(player.velocity_x)

            # Camera update
            camera.smooth_update(player)

            # Collision detection
            for enemy in pygame.sprite.spritecollide(player, enemies, False):
                player.health -= 1
                if player.health <= 0:
                    player.lives -= 1
                    player.health = 100
                    if player.lives <= 0:
                        game_over = True

            for projectile in projectiles:
                hit_enemies = pygame.sprite.spritecollide(projectile, enemies, False)
                for enemy in hit_enemies:
                    enemy.take_damage(25)
                    projectile.kill()
                    score += 100

            collected_items = pygame.sprite.spritecollide(player, collectibles, False)
            for item in collected_items:
                item.apply(player)
                score += 50

            # Drawing
            parallax_bg.draw(screen)

            for sprite in all_sprites:
                screen.blit(sprite.image, camera.apply(sprite))

            for enemy in enemies:
                screen.blit(enemy.image, camera.apply(enemy))

            for item in collectibles:
                screen.blit(item.image, camera.apply(item))

            display_score(screen, score)
            display_health(screen, player)
            display_lives(screen, player)

            pygame.display.flip()
            screen.fill(BLACK)

            # Check if level is complete
            if not enemies:
                level_number += 1
                if level_number > 3:
                    # Game completed
                    game_over = True
                else:
                    # Load next level
                    enemies, collectibles = load_level(level_number, sound_manager)

        # Game Over Screen
        while True:
            game_over_screen(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()
