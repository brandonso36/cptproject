import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Spaceship dimensions
SPACESHIP_WIDTH = 60
SPACESHIP_HEIGHT = 73

# Bullet dimensions
BULLET_WIDTH = 5
BULLET_HEIGHT = 15

# Enemy dimensions
ENEMY_WIDTH = 64
ENEMY_HEIGHT = 64

# Player setup
player_img = pygame.image.load("spaceship.png")
player_img = pygame.transform.scale(player_img, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
player_x = SCREEN_WIDTH // 2 - SPACESHIP_WIDTH // 2
player_y = SCREEN_HEIGHT - SPACESHIP_HEIGHT - 10
player_speed = 5

# Bullet setup
player_bullets = []
player_bullet_speed = 7

enemy_bullets = []
enemy_bullet_speed = 7  # Adjust bullet speed for enemies

# Enemy setup
enemies = []
enemy_speed = 1
enemy_frequency = 100  # Default enemy frequency
enemy_timer = 0

# Font setup
font = pygame.font.SysFont(None, 40)

# Scoring
score = 0

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Function to create enemies
def create_enemy():
    enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
    enemy_y = random.randint(-100, -ENEMY_HEIGHT)
    return pygame.Rect(enemy_x, enemy_y, ENEMY_WIDTH, ENEMY_HEIGHT)

# Function to shoot bullets
def shoot():
    bullet = pygame.Rect(player_x + SPACESHIP_WIDTH // 2 - BULLET_WIDTH // 2, player_y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
    player_bullets.append(bullet)

# Function for enemy to shoot back
def enemy_shoot(enemy):
    bullet = pygame.Rect(enemy.x + ENEMY_WIDTH // 2 - BULLET_WIDTH // 2, enemy.y + ENEMY_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
    enemy_bullets.append(bullet)

# Function to display game over screen
def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render("Score: " + str(score), True, WHITE)
    play_again_text = font.render("Play Again", True, WHITE)
    leaderboard_text = font.render("Leaderboard", True, WHITE)

    # Centering texts
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    leaderboard_rect = leaderboard_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    screen.blit(play_again_text, play_again_rect)
    screen.blit(leaderboard_text, leaderboard_rect)

    # Create button rects
    play_again_button_rect = pygame.Rect(play_again_rect)
    leaderboard_button_rect = pygame.Rect(leaderboard_rect)
    pygame.draw.rect(screen, WHITE, play_again_button_rect, 2)
    pygame.draw.rect(screen, WHITE, leaderboard_button_rect, 2)

    pygame.display.flip()

    # Wait for the player to click the play again or leaderboard button
    wait_for_buttons(play_again_button_rect, leaderboard_button_rect)

# Function to wait for button clicks
def wait_for_buttons(play_again_button_rect, leaderboard_button_rect):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if play_again_button_rect.collidepoint(event.pos):
                        waiting = False
                        reset_game()
                    elif leaderboard_button_rect.collidepoint(event.pos):
                        waiting = False
                        leaderboard_screen()

# Function to reset the game
def reset_game():
    global player_x, player_y, player_bullets, enemies, score, enemy_bullets
    player_x = SCREEN_WIDTH // 2 - SPACESHIP_WIDTH // 2
    player_y = SCREEN_HEIGHT - SPACESHIP_HEIGHT - 10
    player_bullets = []
    enemy_bullets = []  # Clear enemy bullets
    enemies = []
    score = 0

# Function to display mode selection screen
def mode_selection_screen():
    screen.fill(BLACK)
    title_text = font.render("Select Difficulty", True, WHITE)
    easy_text = font.render("Easy Mode", True, WHITE)
    hard_text = font.render("Hard Mode", True, WHITE)

    # Centering texts
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    easy_rect = easy_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    hard_rect = hard_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.blit(title_text, title_rect)
    screen.blit(easy_text, easy_rect)
    screen.blit(hard_text, hard_rect)

    # Create buttons rect
    easy_button_rect = pygame.Rect(easy_rect)
    hard_button_rect = pygame.Rect(hard_rect)
    pygame.draw.rect(screen, WHITE, easy_button_rect, 2)
    pygame.draw.rect(screen, WHITE, hard_button_rect, 2)

    pygame.display.flip()

    # Wait for the player to click the mode button
    return wait_for_mode_selection(easy_button_rect, hard_button_rect)

# Function to wait for mode selection button click
def wait_for_mode_selection(easy_button_rect, hard_button_rect):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if easy_button_rect.collidepoint(event.pos):
                        return False  # Easy mode selected
                    elif hard_button_rect.collidepoint(event.pos):
                        return True   # Hard mode selected

# Function to move enemies side to side (only for hard mode)
def move_enemies():
    for enemy in enemies:
        if enemy.x <= 0 or enemy.x + ENEMY_WIDTH >= SCREEN_WIDTH:
            enemy_speed *= -1  # Reverse direction when reaching edges
        enemy.x += enemy_speed

# Function to update enemy shooting frequency
def update_enemy_shooting():
    global enemy_timer
    if enemy_timer <= 0:
        for enemy in enemies:
            if random.randint(1, 100) == 1:  # Adjust the probability of each enemy shooting
                enemy_shoot(enemy)
        enemy_timer = enemy_frequency
    else:
        enemy_timer -= 1

# Function to display leaderboard screen
def leaderboard_screen():
    screen.fill(BLACK)
    leaderboard_title_text = font.render("Leaderboard", True, WHITE)
    back_text = font.render("Back", True, WHITE)

    # Centering texts
    leaderboard_title_rect = leaderboard_title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

    screen.blit(leaderboard_title_text, leaderboard_title_rect)

    # Display top 5 scores
    top_scores = get_top_scores()
    for i, score in enumerate(top_scores):
        score_text = font.render(f"{i + 1}. Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 40))
        screen.blit(score_text, score_rect)

    screen.blit(back_text, back_rect)

    # Create button rect
    back_button_rect = pygame.Rect(back_rect)
    pygame.draw.rect(screen, WHITE, back_button_rect, 2)

    pygame.display.flip()

    # Wait for the player to click the back button
    wait_for_back(back_button_rect)

# Function to get top scores from the leaderboard file
def get_top_scores():
    with open("leaderboard.txt", "r") as file:
        scores = [int(score) for score in file.readlines()]
    return sorted(scores, reverse=True)[:5]

# Function to wait for back button click
def wait_for_back(back_button_rect):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if back_button_rect.collidepoint(event.pos):
                        waiting = False

# Function to update the leaderboard file with the new score
def update_leaderboard():
    with open("leaderboard.txt", "a") as file:
        file.write(str(score) + "\n")

# Function to remove off-screen bullets and enemies
def remove_off_screen():
    global player_bullets, enemy_bullets, enemies
    player_bullets = [bullet for bullet in player_bullets if bullet.y > 0]
    enemy_bullets = [bullet for bullet in enemy_bullets if bullet.y < SCREEN_HEIGHT]
    enemies = [enemy for enemy in enemies if enemy.y < SCREEN_HEIGHT]

# Display mode selection screen
mode = mode_selection_screen()

# Set difficulty mode
if mode:  # Hard mode
    enemy_frequency = 40  # Decrease enemy frequency
else:  # Easy mode
    enemy_frequency = 100  # Restore default enemy frequency

enemy_timer = 0  # Reset enemy timer
enemy_speed = 3 if mode else 1  # Set enemy speed based on mode

# Game loop
while True:
    running = True
    reset_game()

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot()

        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - SPACESHIP_WIDTH:
            player_x += player_speed

        # Move player bullets
        for bullet in player_bullets:
            bullet.y -= player_bullet_speed
            pygame.draw.rect(screen, WHITE, bullet)

        # Move enemy bullets
        for bullet in enemy_bullets:
            bullet.y += enemy_bullet_speed
            pygame.draw.rect(screen, WHITE, bullet)

        # Create enemies
        if enemy_timer <= 0:
            enemies.append(create_enemy())
            enemy_timer = enemy_frequency
        else:
            enemy_timer -= 1

        # Move enemies and let them shoot
        for enemy in enemies:
            enemy.y += enemy_speed
            enemy_img_rect = pygame.Rect(enemy.x, enemy.y, ENEMY_WIDTH, ENEMY_HEIGHT)
            enemy_img = pygame.image.load("evilspaceship.png")
            enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
            screen.blit(enemy_img, enemy_img_rect)

            # Enemy shoots
            if random.randint(1, 200) == 1:
                enemy_shoot(enemy)

        # Draw player
        screen.blit(player_img, (player_x, player_y))

        # Collision detection for bullets and enemies
        for bullet in player_bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    player_bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 100

        # Collision detection for enemy bullets and player
        for bullet in enemy_bullets:
            if bullet.colliderect((player_x, player_y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)):
                running = False

        # Remove off-screen bullets and enemies
        remove_off_screen()

        # Draw score
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)

    # Update leaderboard
    update_leaderboard()

    # Game over screen
    game_over_screen()
