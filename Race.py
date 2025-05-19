import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game settings
car_width = 50
car_height = 100
car_speed = 5
obstacle_width = 50
obstacle_height = 100
obstacle_speed = 5

# Load car image
car_img = pygame.Surface((car_width, car_height))
car_img.fill(BLUE)
car_rect = car_img.get_rect()
car_rect.center = (WIDTH // 2, HEIGHT - car_height - 10)

# Function to create obstacles
def create_obstacle():
    return pygame.Rect(random.randint(0, WIDTH - obstacle_width), -obstacle_height, obstacle_width, obstacle_height)

# Function to display the game over screen
def display_game_over(score):
    font = pygame.font.SysFont(None, 55)
    game_over_text = font.render(f"Game Over! Final Score: {score}", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.update()

# Main game loop
def game_loop():
    global obstacle_speed
    obstacles = [create_obstacle() for _ in range(3)]  # Create initial obstacles
    score = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player controls with WASD keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_rect.left > 0:
            car_rect.x -= car_speed
        if keys[pygame.K_RIGHT] and car_rect.right < WIDTH:
            car_rect.x += car_speed
        if keys[pygame.K_UP] and car_rect.top > 0:
            car_rect.y -= car_speed
        if keys[pygame.K_DOWN] and car_rect.bottom < HEIGHT:
            car_rect.y += car_speed

        # Player controls using the cursor (mouse)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        car_rect.centerx = mouse_x
        car_rect.centery = mouse_y

        # Move obstacles down
        for obstacle in obstacles:
            obstacle.y += obstacle_speed
            if obstacle.y > HEIGHT:
                obstacle.y = -obstacle_height
                obstacle.x = random.randint(0, WIDTH - obstacle_width)
                score += 1  # Increase score when an obstacle goes off the screen

            # Collision check (if car collides with obstacle)
            if car_rect.colliderect(obstacle):
                display_game_over(score)
                pygame.time.wait(3000)  # Wait for 3 seconds before closing
                running = False  # End the game if there's a collision

        # Speed up obstacles every 20 points
        if score % 20 == 0 and obstacle_speed < 15:
            obstacle_speed += 15

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, obstacle)

        # Draw the player's car
        screen.blit(car_img, car_rect)

        # Display score
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)  # Set the frame rate to 60 FPS

# Start the game loop
game_loop()

pygame.quit()
