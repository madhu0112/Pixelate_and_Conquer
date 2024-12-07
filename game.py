import pygame
import sys
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("From Kalinga to Kurukshetra")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


try:
    background = pygame.image.load("battlefield.jpg")
    character = pygame.image.load("arjuna.png")
    arrow_img = pygame.image.load("arrow.png")
    duryodhana = pygame.image.load("dhuryodhana.png")
    filled_star = pygame.image.load("filled_star.png")
    empty_star = pygame.image.load("empty_star.png")
except pygame.error as e:
    print(f"Error loading images: {e}. Check file paths and formats.")
    pygame.quit()
    sys.exit()


background = pygame.transform.scale(background, (WIDTH, HEIGHT))
character = pygame.transform.scale(character, (70, 120))
arrow_img = pygame.transform.scale(arrow_img, (90, 50))
duryodhana = pygame.transform.scale(duryodhana, (70, 120))
star_size = (30, 30)
filled_star = pygame.transform.scale(filled_star, star_size)
empty_star = pygame.transform.scale(empty_star, star_size)

char_x, char_y = 100, 300
char_speed = 5

arrow_speed = 10
arrows = []

target_x, target_y = 600, 250
target_speed_x, target_speed_y = 3, 2


score = 0
level = 1
level_score = 60
next_level_increment = level_score + 20
font = pygame.font.Font(None, 36)


start_time = pygame.time.get_ticks()


clock = pygame.time.Clock()


def draw_stars(score):
    """Determine and display stars based on the score."""
    if score >= 50:
        stars = 3
    elif score >= 30:
        stars = 2
    elif score >= 15:
        stars = 1
    else:
        stars = 0

    for i in range(3):
        x = 50 + i * (star_size[0] + 10)
        y = 150
        if i < stars:
            screen.blit(filled_star, (x, y))
        else:
            screen.blit(empty_star, (x, y))

def run_level(level):
    """Run a specific level and handle the game flow."""
    global score, char_x, char_y, arrow_speed, arrows, target_x, target_y, target_speed_x, target_speed_y
    score = 0
    char_x, char_y = 100, 300
    arrows = []
    
    
    if level == 1:
        target_speed_x, target_speed_y = 3, 2
        total_time_limit = 120000
        arrow_speed = 10
    elif level == 2:
        target_speed_x, target_speed_y = 4, 3
        arrow_speed = 12
        total_time_limit = 120000
    elif level == 3:
        target_speed_x, target_speed_y = 5, 4
        arrow_speed = 14
        total_time_limit = 120000
    

    running = True
    while running:
        screen.blit(background, (0, 0))

      
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, total_time_limit - elapsed_time)
        remaining_seconds = remaining_time // 1000

        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if len(arrows) < 3:  
                        arrows.append([char_x + 50, char_y + 20])

        
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            char_x -= char_speed
        if keys[K_RIGHT]:
            char_x += char_speed
        if keys[K_UP]:
            char_y -= char_speed
        if keys[K_DOWN]:
            char_y += char_speed

        
        char_x = max(0, min(WIDTH - 70, char_x))
        char_y = max(0, min(HEIGHT - 120, char_y))

        
        for arrow in arrows:
            arrow[0] += arrow_speed
            if arrow[0] > WIDTH:
                arrows.remove(arrow)

       
        for arrow in arrows:
            arrow_rect = pygame.Rect(arrow[0], arrow[1], 70, 30)
            target_rect = pygame.Rect(target_x, target_y, 70, 120)
            if arrow_rect.colliderect(target_rect):
                print("Hit Duryodhana!")
                arrows.remove(arrow)
                score += 1

        
        target_x += target_speed_x
        target_y += target_speed_y
        if target_x <= 0 or target_x >= WIDTH - 50:
            target_speed_x = -target_speed_x
        if target_y <= 0 or target_y >= HEIGHT - 50:
            target_speed_y = -target_speed_y

       
        if score >= level_score:
            print(f"Level {level} unlocked!")
            level += 1
            if level <= 3:
                run_level(level)  
                return

        
        screen.blit(character, (char_x, char_y))
        for arrow in arrows:
            screen.blit(arrow_img, arrow)
        screen.blit(duryodhana, (target_x, target_y))

        
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        next_level_text = font.render(f"Next Level at: {level_score}", True, WHITE)
        timer_text = font.render(f"Time Left: {remaining_seconds}s", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(next_level_text, (10, 90))
        screen.blit(timer_text, (10, 130))
        draw_stars(score)

        
        if remaining_time <= 0:
           timer_text = font.render(f"Time's up", True, WHITE)
           running = False

       
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

run_level(level)
