import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 560
SCREEN_HEIGHT = 620
Cell_Size = 20
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (49, 92, 210)

# Pac-Man's starting position
pac_x, pac_y = 1, 1
score = 0
pac_direction = 'Right'
move_delay = 75  # (milliseconds)
last_move_time = pygame.time.get_ticks()

# Food spawn timing
last_food_spawn_time = pygame.time.get_ticks()
food_spawn_delay = random.randint(2, 5) * 1000  # Faster spawn between 2 to 5 seconds

screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PacMan Game')
font = pygame.font.SysFont('Arial', 18)

board = [
    "############################",
    "#            ##            #",
    "#.####.##### ## ##### #### #",
    "# #### ##### ## ##### #### #",
    "# #### ##### ## ##### #### #",
    "#                          #",
    "# #### ## ######## ## #### #",
    "# #### ## ######## ## #### #",
    "#      ##    ##    ##      #",
    "###### ##### ## ##### ######",
    "###### ##### ## ##### ######",
    "###### ##          ## ######",
    "###### ## ###--### ## ######",
    "###### ## #      # ## ######",
    "       ## #      # ##       ",
    "###### ## #      # ## ######",
    "###### ## ######## ## ######",
    "###### ##          ## ######",
    "###### ## ######## ## ######",
    "###### ## ######## ## ######",
    "#            ##            #",
    "# #### ##### ## ##### #### #",
    "# #### ##### ## ##### #### #",
    "#   ##                ##   #",
    "### ## ## ######## ## ## ###",
    "### ## ## ######## ## ## ###",
    "#      ##    ##    ##      #",
    "# ########## ## ########## #",
    "# ########## ## ########## #",
    "# .......         ......   #",
    "############################"
]

# keeps copy of the board for replay
initial_board = board.copy()

pac_image = pygame.image.load('Assets/Pac.png')
pac_image = pygame.transform.scale(pac_image, (Cell_Size, Cell_Size))

def draw_board():
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, BLUE, (x * Cell_Size, y * Cell_Size, Cell_Size, Cell_Size))
            if cell == '.':
                pygame.draw.circle(screen, WHITE, (x * Cell_Size + Cell_Size // 2, y * Cell_Size + Cell_Size // 2), 3)
            if cell == 'o':
                pygame.draw.circle(screen, WHITE, (x * Cell_Size + Cell_Size // 2, y * Cell_Size + Cell_Size // 2), 7)

def draw_pac():
    screen.blit(pac_image, (pac_x * Cell_Size, pac_y * Cell_Size))

def move_pac():
    global pac_x, pac_y, score, last_food_spawn_time, food_spawn_delay

    if pac_direction == 'LEFT':
        if pac_x == 0 and pac_y == 14:
            pac_x = 28
        elif pac_x > 0 and board[pac_y][pac_x - 1] != '#':
            pac_x -= 1

    elif pac_direction == 'RIGHT':
        if pac_x == 27 and pac_y == 14:
            pac_x = 0
        elif pac_x < len(board[pac_y]) - 1 and board[pac_y][pac_x + 1] != '#':
            pac_x += 1

    elif pac_direction == 'UP':
        if pac_y > 0 and board[pac_y - 1][pac_x] != '#':
            pac_y -= 1

    elif pac_direction == 'DOWN':
        if pac_y < len(board) - 1 and board[pac_y + 1][pac_x] != '#':
            pac_y += 1

    pac_x = max(0, min(pac_x, len(board[pac_y]) - 1))


    if board[pac_y][pac_x] == ".":
        board[pac_y] = board[pac_y][:pac_x] + ' ' + board[pac_y][pac_x + 1:]
        score += 10
        last_food_spawn_time = pygame.time.get_ticks()
        food_spawn_delay = random.randint(2, 5) * 1000

    elif board[pac_y][pac_x] == "o":
        board[pac_y] = board[pac_y][:pac_x] + ' ' + board[pac_y][pac_x + 1:]
        score += 50
        last_food_spawn_time = pygame.time.get_ticks()
        food_spawn_delay = random.randint(2, 5) * 1000

def spawn_random_food():
    empty_positions = []
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == ' ':
                empty_positions.append((x, y)) #append adds to the end of a list

    if empty_positions:
        x, y = random.choice(empty_positions)
        food_type = random.choice(['.', 'o'])
        board[y] = board[y][:x] + food_type + board[y][x + 1:]

def check_all_food_eaten():
    for row in board:
        if '.' in row or 'o' in row:
            return False
    return True


clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pac_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                pac_direction = 'RIGHT'
            elif event.key == pygame.K_DOWN:
                pac_direction = 'DOWN'
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                pac_direction = 'UP'
        elif event.type == pygame.KEYUP:
                pac_direction = None

    current_time = pygame.time.get_ticks()
    if current_time - last_food_spawn_time >= food_spawn_delay:
        spawn_random_food()
        last_food_spawn_time = current_time
        food_spawn_delay = random.randint(2, 5) * 1000

    if pac_direction and current_time - last_move_time >= move_delay:
        move_pac()
        last_move_time = current_time

    if check_all_food_eaten():
        # Show win screen
        win_text = font.render("You Win!", True, WHITE)
        inst_text = font.render("Press R to Replay or Q to Quit", True, WHITE)
        screen.blit(win_text, win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        screen.blit(inst_text, inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))
        pygame.display.flip()

        # Wait for player choice
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset game state
                        board = initial_board.copy()
                        pac_x, pac_y = 1, 1
                        pac_direction = 'Right'
                        score = 0
                        last_move_time = pygame.time.get_ticks()
                        last_food_spawn_time = pygame.time.get_ticks()
                        food_spawn_delay = random.randint(2, 5) * 1000
                        waiting = False
                    elif event.key == pygame.K_q:
                        running = False
                        waiting = False
        continue

    screen.fill(BLACK)
    draw_board()
    draw_pac()

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 30))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
