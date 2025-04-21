import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 560
SCREEN_HEIGHT = 620
Cell_Size = 20
FPS = 30


BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (49,92,210)

# Pac-Man's starting position
pac_x, pac_y = 1, 1
score = 0  # Starting Score

pac_direction = 'Right'
move_delay = 100  # time between moves in milliseconds
last_move_time = pygame.time.get_ticks()



screen = pygame.display.set_mode(size = (SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('PacMan Game')
font = pygame.font.SysFont('Arial', 18)

board = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "######.##### ## #####.######",
    "######.##          ##.######",
    "######.## ###--### ##.######",
    "######.## #      # ##.######",
    "       ## #      # ##       ",
    "######.## #      # ##.######",
    "######.## ######## ##.######",
    "######.##          ##.######",
    "######.## ######## ##.######",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#o..##................##..o#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]

pac_image = pygame.image.load('Assets/Pac.png') #Loads Pacman sprite
pac_image = pygame.transform.scale(pac_image, (Cell_Size,Cell_Size)) #Transforms size of Pacman Sprite

def draw_board():           # Rect is a tuple of 4 values: (x,y,width,height)
    for y, row in enumerate(board):
        for x, cell in enumerate(row): # x represents the index (number in a list) of the row, cell represents the item (#,.,o)
            if cell == '#':
                pygame.draw.rect(screen,BLUE, (x * Cell_Size, y * Cell_Size,Cell_Size,Cell_Size))
            if cell == '.':
                pygame.draw.circle(screen,WHITE,(x * Cell_Size + Cell_Size // 2, y * Cell_Size + Cell_Size // 2), 3)
            if cell == 'o':
                pygame.draw.circle(screen, WHITE, (x * Cell_Size + Cell_Size // 2, y * Cell_Size + Cell_Size // 2), 7)

def draw_pac():
    screen.blit(pac_image, (pac_x * Cell_Size, pac_y * Cell_Size))

def move_pac():
    global pac_x, pac_y, score
    if pac_direction == 'LEFT' and board[pac_y][pac_x - 1] != '#': #Tells Pacman to move left if there is not a wall there
        pac_x -= 1                                                  # (!= means not equal to)
    elif pac_direction == 'RIGHT' and board[pac_y][pac_x + 1] != '#':
        pac_x += 1
    elif pac_direction == 'UP' and board[pac_y - 1][pac_x] != '#':
        pac_y -= 1
    elif pac_direction == 'DOWN' and board[pac_y + 1][pac_x] != '#':
        pac_y += 1


    if board[pac_y][pac_x] == ".":   # "If Pacman's position is on a food tile"
        board[pac_y] = board[pac_y][:pac_x] + ' ' + board[pac_y][pac_x +1:]
        score += 10
    elif board[pac_y][pac_x] == "o":   # "If Pacman's position is on a food tile"
        board[pac_y] = board[pac_y][:pac_x] + ' ' + board[pac_y][pac_x +1:]
        score += 50

def check_all_food_eaten(): #This function examines each row of the game board.
    for row in board:       # If it finds any uneaten pellets in any row, it returns false. Otherwise, it returns true.
        if '.' in row or 'o' in row:
            return False
    return True



#This code loop continuously checks for user input( controls Pac-Man’s direction),
# updates the game state(moves Pac-Man, checks for collisions and win/lose conditions),
# redraws the game scene on the screen with updated positions and scores,
# and maintains a consistent frame rate for smooth gameplay.
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pac_direction = 'LEFT'
            if event.key == pygame.K_RIGHT:
                pac_direction = 'RIGHT'
            if event.key == pygame.K_DOWN:
                pac_direction = 'DOWN'
            if event.key == pygame.K_UP:
                pac_direction = 'UP'

        elif event.type == pygame.KEYUP: #stops pac if no keys are being pressed
            pac_direction = None

    current_time = pygame.time.get_ticks()
    if pac_direction and current_time - last_move_time >= move_delay:
        move_pac()
        last_move_time = current_time

    if check_all_food_eaten():
        print("You Win!")
        running = False

    screen.fill(BLACK)
    draw_board()
    draw_pac()

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, SCREEN_HEIGHT - 30))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()








