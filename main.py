import pygame

# initializer
pygame.init()

# game setup
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two Player Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 40)
timer = pygame.time.Clock()  # speed at which the game updates
fps = 60

# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

# pieces in [8][8] array with 0-7 rows and 0-7 columns
# each tuple in this list corresponds to the (r,c) of that piece from the pieces list
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

# pieces in [8][8] array with 0-7 rows and 0-7 columns
# each tuple in this list corresponds to the (r,c) of that piece from the pieces list
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_pieces_white = []
captured_pieces_black = []

# 0 - whites turn no selection: 1 - whites turn piece selected: 2 - blacks turn no selection: 3 - blacks turn piece selected
turn_step = 0  # phase of what the user is doing
selection = 100  # will store the index of the selected piece, default/no piece selected case will have 100 stored
# will check for all the valid moves for that selected piece at one turn at a time (gets emptied for the opponent's turn)
valid_moves = []

# load in game piece images (queen, king, rook, bishop, knight, pawn) x2
# for Black pieces (Note: small versions are used to display when pieces are captured)
black_queen = pygame.image.load('assets/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load('assets/images/black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('assets/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('assets/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('assets/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (62, 62))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))

# for White pieces
white_queen = pygame.image.load('assets/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('assets/images/white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('assets/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (62, 62))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

# Lists to store all the images
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small, white_rook_small,
                      white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small, black_rook_small,
                      black_bishop_small]

# matching name index with the index in the images list (i.e. white_images and likewise) to correctly print it
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']  # order matches with white_images and likewise

# check variables / flashing counter
counter = 0


# draw main game board graphic
# color for dark spot = sienna, for light spot = wheat
def draw_board():
    # 64x64 squares on board, but here, we traverse through 32 as every other box is going be a background shade anyway
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'wheat', [540 - (column * 180), row * 90, 90, 90])
        else:
            pygame.draw.rect(screen, 'wheat', [630 - (column * 180), row * 90, 90, 90])

        # right border
        pygame.draw.rect(screen, 'sienna', [720, 0, 280, HEIGHT])
        pygame.draw.rect(screen, 'orange', [720, 0, 280, HEIGHT], 5)

        # bottom border
        pygame.draw.rect(screen, 'wheat', [0, 720, WIDTH, 80])
        pygame.draw.rect(screen, 'orange', [0, 720, WIDTH, 80], 5)

        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 745))

        # borders for each individual spot on board
        for j in range(9):
            # horizontal mini lines
            pygame.draw.line(screen, 'orange', (0, 90 * j), (720, 90 * j), 2)
            # vertical mini lines
            pygame.draw.line(screen, 'orange', (90 * j, 0), (90 * j, 720), 2)


# draw pieces onto the board
def draw_pieces():
    # for white pieces
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])  # get the index for image
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 90 + 14, white_locations[i][1] * 90 + 24))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 90 + 9, white_locations[i][1] * 90 + 9))

        # white player's turn (i.e. selected)
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red',
                                 [white_locations[i][0] * 90 + 1, white_locations[i][1] * 90 + 1, 90, 90], 2)

    # for black pieces
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 90 + 14, black_locations[i][1] * 90 + 24))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 90 + 9, black_locations[i][1] * 90 + 9))

        # black player's turn (i.e. selected)
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue',
                                 [black_locations[i][0] * 90 + 1, black_locations[i][1] * 90 + 1, 90, 90], 2)


# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    # list of all the moves a particular piece can take
    moves_list = []
    # has all the moves for every piece of a specific color
    all_moves_list = []

    # traverse through each piece name and add their moves to all_moves_list at the end of iteration
    for i in range(len(pieces)):
        location = locations[i]  # active piece's location
        piece = pieces[i]  # active piece

        if piece == "pawn":
            moves_list = check_pawn(location, turn)

        elif piece == "rook":
            moves_list = check_rook(location, turn)

        elif piece == "knight":
            moves_list = check_knight(location, turn)

        elif piece == "bishop":
            moves_list = check_bishop(location, turn)

        elif piece == "queen":
            moves_list = check_queen(location, turn)

        elif piece == "king":
            moves_list = check_king(location, turn)

        # append in the all_moves_list and move to the next piece in loop
        all_moves_list.append(moves_list)

    return all_moves_list


# check pawn valid moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':

        # initial 2 jump case for pawn
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and \
                position[1] == 1:
            moves_list.append((position[0], position[1] + 2))

        # else 1 move case for pawn
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and \
                position[1] < 7:
            moves_list.append((position[0], position[1] + 1))

        # diagonal (down + right pointing)
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))

        # diagonal (down + left pointing)
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))

    # black color
    else:

        # initial 2 jump case for pawn
        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and \
                position[1] == 6:
            moves_list.append((position[0], position[1] - 2))

        # else 1 move case for pawn
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and \
                position[1] > 0:
            moves_list.append((position[0], position[1] - 1))

        # diagonal (up + right pointing)
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))

        # diagonal (up + left pointing)
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))

    return moves_list


# check pawn rook moves
def check_rook(position, color):
    moves_list = []

    # our color
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations

    else:
        enemies_list = white_locations
        friends_list = black_locations

    # loop to check for down, up, right, left
    for i in range(4):
        path = True
        chain = 1

        # down line
        if i == 0:
            x = 0
            y = 1
        # up line
        elif i == 1:
            x = 0
            y = -1
        # right line
        elif i == 2:
            x = 1
            y = 0
        # left line
        else:
            x = -1
            y = 0

        # if paths ahead are open/not blocked by some piece
        while path:
            # if box is empty with no friendly piece ahead (can have enemy on box)
            if ((position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7):
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))

                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    # first enemy piece detected in the chain direction, so stop checking in this direction
                    path = False

                # chain in that direction gets longer for next iteration of while
                chain += 1
            else:
                path = False

    return moves_list


# check knight valid moves
def check_knight(position, color):
    moves_list = []

    # our color
    if color == 'white':
        friends_list = white_locations

    else:
        friends_list = black_locations

    # total targets 8 spaces to check for knight (circle pattern, 2 boxes in one direction, 1 box in other direction)
    targets = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, -1), (2, 1), (-2, -1), (-2, 1)]
    for i in range(8):
        # current target tuple
        c_target = (position[0] + targets[i][0], position[1] + targets[i][1])

        if c_target not in friends_list and 0 <= c_target[0] <= 7 and 0 <= c_target[1] <= 7:
            moves_list.append(c_target)

    return moves_list


# check bishop valid moves
def check_bishop(position, color):
    moves_list = []

    # our color
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations

    else:
        enemies_list = white_locations
        friends_list = black_locations

    # loop to check for R-up, R-down, L-up, L-down
    for i in range(4):
        path = True
        chain = 1

        # R-up line
        if i == 0:
            x = 1
            y = -1
        # R-down line
        elif i == 1:
            x = 1
            y = 1
        # L-up line
        elif i == 2:
            x = -1
            y = -1
        # L-down line
        else:
            x = -1
            y = 1

        # if paths ahead are open/not blocked by some piece
        while path:
            # if box is empty with no friendly piece ahead (can have enemy on box)
            if ((position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7):
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))

                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    # first enemy piece detected in the chain direction, so stop checking in this direction
                    path = False

                # chain in that direction gets longer for next iteration of while
                chain += 1
            else:
                path = False

    return moves_list


# check queen valid moves
def check_queen(position, color):
    moves_list = []

    moves_list += check_rook(position, color)
    moves_list += check_bishop(position, color)

    return moves_list


# check king valid moves
def check_king(position, color):
    moves_list = []

    # our color
    if color == 'white':
        friends_list = white_locations

    else:
        friends_list = black_locations

    # total targets 8 spaces to check for king (square pattern)
    targets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    for i in range(8):
        # current target tuple
        c_target = (position[0] + targets[i][0], position[1] + targets[i][1])

        if c_target not in friends_list and 0 <= c_target[0] <= 7 and 0 <= c_target[1] <= 7:
            moves_list.append(c_target)

    return moves_list


# check for valid moves for just the selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options

    valid_options = options_list[selection]

    return valid_options


# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'

    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 90 + 45, moves[i][1] * 90 + 45), 5)


# draw captured pieces on screen side
def draw_captured():
    # Constants for spacing
    max_pieces_per_column = 8
    y_increment = 55
    x_white_start = 720 + 45
    x_black_start = 820 + 45

    # Draw captured pieces for white that captured black pieces
    for i in range(len(captured_pieces_white)):
        index = piece_list.index(captured_pieces_white[i])  # get the index for image
        x_offset = (i // max_pieces_per_column) * 50  # Move to the next column after 8 pieces
        y_offset = (i % max_pieces_per_column) * y_increment  # Calculate y offset
        screen.blit(small_black_images[index],
                    (x_white_start + x_offset, 40 + y_offset))  # Draw in a vertical line with smaller gap

    # Draw captured pieces for black that captured white pieces
    for i in range(len(captured_pieces_black)):
        index = piece_list.index(captured_pieces_black[i])
        x_offset = (i // max_pieces_per_column) * 50  # Move to the next column after 8 pieces
        y_offset = (i % max_pieces_per_column) * y_increment  # Calculate y offset
        screen.blit(small_white_images[index],
                    (x_black_start + x_offset, 40 + y_offset))  # Draw in a vertical line with smaller gap


# draw flashing king for check
def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 90 + 1,
                                                              white_locations[king_index][1] * 90 + 1, 90, 90], 5)

    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 90 + 1,
                                                               black_locations[king_index][1] * 90 + 1, 90, 90], 5)


# main game loop

# Populate all the available next valid options once (gets updated at the end of each turn)
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')

run = True
while run:
    timer.tick(fps)
    # for the king check flashing
    if counter < 30:
        counter += 1
    else:
        counter = 0

    screen.fill('sienna')  # background color for the screen
    draw_board()
    draw_pieces()
    # drawing captured pieces on screen
    draw_captured()
    # drawing flashing king for check
    draw_check()

    # if a piece is actually selected, draw dots
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    # event handling that gets everything that occurs like mouse input etc
    for event in pygame.event.get():

        # if X at the title bar is clicked
        if event.type == pygame.QUIT:
            run = False

        # remaining event handling cases
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x_coord = event.pos[0] // 90  # cause each box is 90 px wide
            y_coord = event.pos[1] // 90  # cause each box is 90 px long
            click_coords = (x_coord, y_coord)  # This is to easily update the tuples in the locations list

            # white's turn
            if turn_step < 2:
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)  # what piece we just selected
                    if turn_step == 0:
                        turn_step = 1  # update turn_step so to move to next stage

                # if the move is valid, update the location of the selected piece to new selection tuple
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords  # update the tuple/location
                    # if eating the opponents piece
                    if click_coords in black_locations:
                        black_piece_killed = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece_killed])
                        black_pieces.pop(black_piece_killed)  # remove that piece from the list
                        black_locations.pop(black_piece_killed)  # remove the location corresponding to that piece

                    # update all the available next valid options
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')

                    turn_step = 2  # update turn_step to 2 so as to change to black's turn
                    selection = 100  # back to default
                    valid_moves = []  # gets recalculated each turn

            # black's turn
            if turn_step >= 2:
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)  # what piece we just selected
                    if turn_step == 2:
                        turn_step = 3  # update turn_step so to move to next stage

                # if the move is valid, update the location of the selected piece to new selection tuple
                if click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords  # update the tuple/location
                    if click_coords in white_locations:
                        white_piece_killed = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece_killed])
                        white_pieces.pop(white_piece_killed)
                        white_locations.pop(white_piece_killed)

                    # update all the available next valid options
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')

                    turn_step = 0  # update turn_step to 2 so as to change to black's turn
                    selection = 100  # back to default
                    valid_moves = []  # gets recalculated each turn

    # displays everything on the screen
    pygame.display.flip()
pygame.quit()  # ends the program
