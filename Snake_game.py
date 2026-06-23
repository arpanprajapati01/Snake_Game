# to import the library of pygame
import pygame
import random
import os

# to start the module of pygame
pygame.init()
pygame.mixer.init()

# to initialize the dimension of window
WIDTH = 800
HEIGHT = 600

# Initialize in windows interface
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# Caption of the window
pygame.display.set_caption("SNAKE GAME")

snake_x = 300
snake_y = 200

snake_body = []
snake_length = 1
    
snake_size = 20

move_x = 0
move_y = 0

# create food variables
food_size = 20

food_x = random.randrange(0, WIDTH, 20)
food_y = random.randrange(0, HEIGHT, 20)

# create a score variable
score = 0

# create a font on the screen
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 60)

# Load sounds - Place your sound files in the same folder as this script
# You can download free sounds from freesound.org or zapsplat.com
try:
    eat_sound = pygame.mixer.Sound('eat.wav')  # Sound when snake eats food
    collision_sound = pygame.mixer.Sound('collision.wav')  # Sound when snake collides
    background_music = 'background_music.wav'  # Background music file
except:
    print("Sound files not found. Game will run without sounds.")
    print("Place these files in the same folder as this script:")
    print("  - eat.wav")
    print("  - collision.wav")
    print("  - background_music.wav")
    eat_sound = None
    collision_sound = None
    background_music = None

#looping
running = True
game_over = False
game_started = False
clock = pygame.time.Clock()
while running:

    # Start screen
    if not game_started:
        screen.fill((0,0,0))
        
        title_text = big_font.render(
            "SNAKE GAME",
            True,
            (0,255,0)
        )
        
        start_text = font.render(
            "PRESS SPACE TO START",
            True,
            (255,255,255)
        )
        
        title_rect = title_text.get_rect(center=(WIDTH//2, 150))
        start_rect = start_text.get_rect(center=(WIDTH//2, 300))
        
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        
        pygame.display.update()
        
        # Handle start key
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True
                    # Play background music when game starts
                    if background_music and os.path.exists(background_music):
                        pygame.mixer.music.load(background_music)
                        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        
        continue

    # add gameover over screen 
    if game_over:
        screen.fill((0,0,0))

        game_over_text = big_font.render(
            "GAME OVER",
            True,
            (255,0,0)
        )

        score_text = font.render(
        f"Final Score: {score}",
        True,
        (255, 255, 255)
    )
        
        restart_text = font.render(
        "PRESS R TO RESTART",
        True,
        (255, 255, 255)
    )
        
        quit_text = font.render(
        "PRESS Q TO QUIT",
        True,
        (255, 255, 255)
    )
        
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, 100))
        score_rect = score_text.get_rect(center=(WIDTH//2, 180))
        restart_rect = restart_text.get_rect(center=(WIDTH//2, 240))
        quit_rect = quit_text.get_rect(center=(WIDTH//2, 280))
        
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.update()
        
        # Handle restart and quit keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    game_over = False
                    snake_x = 300
                    snake_y = 200
                    snake_body = []
                    snake_length = 1
                    score = 0
                    move_x = 0
                    move_y = 0
                    food_x = random.randrange(0, WIDTH, 20)
                    food_y = random.randrange(0, HEIGHT, 20)
                    # Restart background music
                    if background_music and os.path.exists(background_music):
                        pygame.mixer.music.load(background_music)
                        pygame.mixer.music.play(-1)
                
                elif event.key == pygame.K_q:
                    running = False
        
        continue

    # to handle the event inside the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

            if event.key == pygame.K_LEFT:
                move_x = -20
                move_y = 0
            
            elif event.key == pygame.K_RIGHT:
                move_x = 20
                move_y = 0

            elif event.key == pygame.K_UP:
                move_x = 0
                move_y = -20

            elif event.key == pygame.K_DOWN:
                move_x = 0
                move_y = 20

    # Background colour
    screen.fill((0, 0, 0))   # defines black colour in background

    snake_x += move_x  # this changes the snake position continously
    snake_y += move_y  # this changes the snake position continously

    # left boundary
    if snake_x < 0:
        snake_x = 0

    # right boundary
    if snake_x > WIDTH - snake_size:
        snake_x =  WIDTH - snake_size

    # top boundary
    if snake_y < 0:
        snake_y = 0

    # bottom boundary
    if snake_y > HEIGHT - snake_size:
        snake_y = HEIGHT - snake_size
    
    # to store the current position of the snake
    snake_head =[snake_x, snake_y]
    snake_body.append(snake_head)

    # add new position and delete previous one
    if len(snake_body) > snake_length:
        del snake_body[0]

    # add self collision check
    for part in snake_body[:-1]:
        if part == snake_head:
            game_over = True
            # Play collision sound
            if collision_sound:
                pygame.mixer.music.stop()  # Stop background music on collision
                collision_sound.play()

    # check for food collision
    if snake_x == food_x and snake_y == food_y:
        score += 1
        snake_length += 1
        
        # Play eat sound
        if eat_sound:
            eat_sound.play()

        food_x = random.randrange(0, WIDTH, 20)
        food_y = random.randrange(0, HEIGHT, 20)

        #print("Score: ",score)
        
    # to draw snake
    for part in snake_body:
        pygame.draw.rect(
                screen,
                (0,255,0),
                (part[0], part[1], snake_size, snake_size)   # the snake wherever go its drawn and its size also
          )
    
    pygame.draw.rect(
        screen,
        (255,0,0),
        (food_x, food_y, food_size, food_size)
    )

    score_text = font.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )

    screen.blit(score_text,(10,10))

    # to update the screen regularly
    pygame.display.update()
    clock.tick(10)

pygame.quit()        

