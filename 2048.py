import pygame # type: ignore
import random
pygame.init()

# Initialize the mixer for music
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load('2048_music.mp3')  # Replace 'background.mp3' with your music file
pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely


#initial set up
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Pink 2048")
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)
start_screen = True

# Draw start screen with title and play button
def draw_start_screen():
    screen.fill(colors['bg'])
    title_font = pygame.font.Font('freesansbold.ttf', 36)
    button_font = pygame.font.Font('freesansbold.ttf', 24)
    
    title_text = title_font.render("Pink 2048 <3", True, 'pink')
    play_text = button_font.render("Play Game!", True, 'white')
    
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    play_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 10, 140, 50)  # Button rectangle
    play_text_rect = play_text.get_rect(center=play_rect.center)
    
    screen.blit(title_text, title_rect)
    pygame.draw.rect(screen, 'pink', play_rect, border_radius=10)
    screen.blit(play_text, play_text_rect)

# 2048 game colors
colors = {
    0: (255, 230, 234),          # Background of empty tiles
    2: (255, 218, 225),          # Lighter pink for 2
    4: (255, 200, 215),          # Slightly darker pink for 4
    8: (255, 182, 204),          # Medium pink for 8
    16: (255, 156, 191),         # Deeper pink for 16
    32: (255, 130, 178),         # Vivid pink for 32
    64: (255, 104, 165),         # Bold pink for 64
    128: (255, 78, 152),         # Deep pink for 128
    256: (230, 65, 141),         # Darker pink for 256
    512: (255, 64, 128),         # True pink for 512
    1024: (255, 51, 120),        # Intense pink for 1024
    2048: (255, 20, 100),        # Bright, bold pink for 2048
    'light text': (255, 245, 247), # Light text color
    'dark text': (102, 51, 76),  # Darker text color to match pink theme
    'other': (0, 0, 0),          # Keep black for other
    'bg': (255, 240, 245)        # Soft pinkish background
}


# game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score', 'r')
init_high = 0
file.close()
high_score = init_high


# draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'pink', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


# take your turn based on direction
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board


# spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'white')
    high_score_text = font.render(f'High Score: {high_score}', True, 'white')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    pass


# draw tiles for game
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'white', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)



# Main game loop
run = True
while run:
    timer.tick(fps)
    
    if start_screen:
        draw_start_screen()  # Display start screen
    else:
        screen.fill('pink')
        draw_board()
        draw_pieces(board_values)
        
        if spawn_new or init_count < 2:
            board_values, game_over = new_pieces(board_values)
            spawn_new = False
            init_count += 1
        if direction != '':
            board_values = take_turn(direction, board_values)
            direction = ''
            spawn_new = True
        if game_over:
            draw_over()
            if high_score > init_high:
                file = open('high_score', 'w')
                file.write(f'{high_score}')
                file.close()
                init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if start_screen and event.type == pygame.MOUSEBUTTONDOWN:
            # Check if "Play Game" button is clicked
            if pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 10, 140, 50).collidepoint(event.pos):
                start_screen = False  # Hide start screen and start the game

        if not start_screen and event.type == pygame.KEYUP:
            # Handle direction keys for the game
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'

            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False

    if score > high_score:
        high_score = score

    pygame.display.flip()

pygame.quit()