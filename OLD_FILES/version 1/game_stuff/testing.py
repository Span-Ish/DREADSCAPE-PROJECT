import pygame

pygame.init()

# Map and tile setup
tile_size = 64  # Each tile is 64x64 pixels

# Define the tile map (0 = ground, 1 = wall, "P" = player spawn point)
level_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, "P", 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Calculate screen dimensions based on the map
screen_width = len(level_map[0]) * tile_size
screen_height = len(level_map) * tile_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tile Map Example")

# Define colors for tiles
ground_color = (0, 0, 0)  # Black color for ground
wall_color = (0, 0, 255)  # Blue color for walls

# PLAYER
player_color = (255, 0, 0)  # Red color for the player
player_size = 32
playerX, playerY = 0, 0  # Initial position (will be set based on map)
playerX_change = 0
playerY_change = 0

# Locate player spawn point on the map
for row_index, row in enumerate(level_map):
    print(row_index,row)
    for col_index, tile in enumerate(row):
        print(col_index,tile)
        if tile == "P":
            playerX = col_index * tile_size
            playerY = row_index * tile_size
            level_map[row_index][col_index] = 0  # Convert the spawn point to ground after setting the player position

# Frames per second
fps = 60
timer = pygame.time.Clock()

# Draw the map based on level_map
def draw_map():
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            x = col_index * tile_size
            y = row_index * tile_size
            if tile == 1:
                pygame.draw.rect(screen, wall_color, (x, y, tile_size, tile_size))  # Draws wall tile i.e blue
            else:
                pygame.draw.rect(screen, ground_color, (x, y, tile_size, tile_size))  # Draws ground tile i.e black

def draw_player(x, y):
    pygame.draw.rect(screen, player_color, (x, y, player_size, player_size))  # Draws the player

def can_move(new_x, new_y):
    # Calculate the players edges
    left_edge = new_x
    right_edge = new_x + player_size
    top_edge = new_y
    bottom_edge = new_y + player_size

    # Check the corners of the player against the map
    corners = [
        (left_edge, top_edge),
        (right_edge, top_edge),
        (left_edge, bottom_edge),
        (right_edge, bottom_edge)
    ]

    for corner_x, corner_y in corners:
        tile_x = corner_x // tile_size
        tile_y = corner_y // tile_size

        if level_map[tile_y][tile_x] == 1:  # Wall tile
            return False  # Collision detected

    return True  # No collision

# Game loop
running = True
while running:
    timer.tick(fps)
    screen.fill((0, 0, 0))  # Clear the screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movement events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_UP:
                playerY_change = -1
            if event.key == pygame.K_DOWN:
                playerY_change = 1

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                playerX_change = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                playerY_change = 0

    # Calculate new player position
    new_playerX = playerX + playerX_change
    new_playerY = playerY + playerY_change

    # Check collision for both X and Y movement
    if can_move(new_playerX, playerY):
        playerX = new_playerX
    if can_move(playerX, new_playerY):
        playerY = new_playerY

    # Draw the map and player
    draw_map()
    draw_player(playerX, playerY)

    pygame.display.update()