import pygame
import time
import random

WIDTH, HEIGHT = 800,800
WINDOW=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Battleship")

GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE

EMPTY= "Empty"
CARRIER= "Carrier"
BATTLESHIP= "Battleship"
CRUISER= "Cruiser"
DESTROYER= "Destroyer"

#Create a 10x10 grid
grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(WINDOW,(255,255,255),(x,0),(x,HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(WINDOW,(255,255,255),(0,y),(WIDTH,y))
    # Draw ships on the grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == CARRIER:  # Carrier
                color = (255, 255, 255)  # White
            elif grid[row][col] == BATTLESHIP:  # Battleship
                color = (0, 255, 0)  # Green
            elif grid[row][col] == CRUISER:  # Cruiser
                color = (0, 0, 255)  # Blue
            elif grid[row][col] == DESTROYER:  # Destroyer
                color = (255, 0, 0)  # Red
            else:
                continue  # Skip empty cells

            # Draw the ship cell
            pygame.draw.rect(
                WINDOW,
                color,
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

def place_ships_randomly(grid):
    """
    Randomly place all ships on the grid.
    """
    ship_types = [
        (CARRIER, 5),       # 1 Carrier
        (BATTLESHIP, 4),    # 2 Battleships
        (CRUISER, 3),       # 3 Cruisers
        (DESTROYER, 1)      # 4 Destroyers
    ]
    ship_counts = [1, 2, 3, 4]  # Number of each ship type to place

    for (ship_type, ship_length), count in zip(ship_types, ship_counts):
        for _ in range(count):
            placed = False
            max_attempts = 100  # Limit the number of placement attempts
            attempts = 0

            while not placed and attempts < max_attempts:
                attempts += 1
                # Randomly choose orientation: 0 = horizontal, 1 = vertical
                orientation = random.choice([0, 1])
                if orientation == 0:  # Horizontal
                    row = random.randint(0, GRID_SIZE - 1)
                    col = random.randint(0, GRID_SIZE - ship_length)
                    # Check if the cells and surrounding cells are empty
                    if all(
                        grid[row][col + i] == EMPTY and
                        all(
                            grid[row + dr][col + i + dc] == EMPTY
                            for dr in [-1, 0, 1] if 0 <= row + dr < GRID_SIZE
                            for dc in [-1, 0, 1] if 0 <= col + i + dc < GRID_SIZE
                        )
                        for i in range(ship_length)
                    ):
                        for i in range(ship_length):
                            grid[row][col + i] = ship_type
                        placed = True
                else:  # Vertical
                    row = random.randint(0, GRID_SIZE - ship_length)
                    col = random.randint(0, GRID_SIZE - 1)
                    # Check if the cells and surrounding cells are empty
                    if all(
                        grid[row + i][col] == EMPTY and
                        all(
                            grid[row + i + dr][col + dc] == EMPTY
                            for dr in [-1, 0, 1] if 0 <= row + i + dr < GRID_SIZE
                            for dc in [-1, 0, 1] if 0 <= col + dc < GRID_SIZE
                        )
                        for i in range(ship_length)
                    ):
                        for i in range(ship_length):
                            grid[row + i][col] = ship_type
                        placed = True

            if not placed:
                print(f"Failed to place ship of type {ship_type} and length {ship_length} after {max_attempts} attempts.")
                return False  # Return failure if a ship cannot be placed

    return True  # Return success if all ships are placed

def manual_place_ship(grid, ship_type, ship_length, start_row, start_col, orientation):
    # Check if the ship can be placed at the selected position
    if orientation == 0:  # Horizontal
        if start_col + ship_length > GRID_SIZE:
            return False  # Ship goes out of bounds
        if all(
            grid[start_row][start_col + i] == EMPTY and
            all(grid[start_row + dr][start_col + i + dc] == EMPTY
                for dr in [-1, 0, 1] if 0 <= start_row + dr < GRID_SIZE
                for dc in [-1, 0, 1] if 0 <= start_col + i + dc < GRID_SIZE)
            for i in range(ship_length)
        ):
            for i in range(ship_length):
                grid[start_row][start_col + i] = ship_type
            return True
    else:  # Vertical
        if start_row + ship_length > GRID_SIZE:
            return False  # Ship goes out of bounds
        if all(
            grid[start_row + i][start_col] == EMPTY and
            all(grid[start_row + i + dr][start_col + dc] == EMPTY
                for dr in [-1, 0, 1] if 0 <= start_row + i + dr < GRID_SIZE
                for dc in [-1, 0, 1] if 0 <= start_col + dc < GRID_SIZE)
            for i in range(ship_length)
        ):
            for i in range(ship_length):
                grid[start_row + i][start_col] = ship_type
            return True
    return False


def manual_setup(grid):
    # Define ship types, lengths, and limits
    ship_types = {
        pygame.K_1: (DESTROYER, 1, 4),  # Key 1 for Destroyer (4 allowed)
        pygame.K_2: (CRUISER, 3, 3),   # Key 2 for Cruiser (3 allowed)
        pygame.K_3: (BATTLESHIP, 4, 2),  # Key 3 for Battleship (2 allowed)
        pygame.K_4: (CARRIER, 5, 1)    # Key 4 for Carrier (1 allowed)
    }
    ship_counts = {key: 0 for key in ship_types}  # Track how many of each ship have been placed
    selected_ship = None  # Currently selected ship type and length
    cells_to_place = 0  # Number of cells left to place for the current ship
    placed_cells = []  # Track the cells already placed for the current ship
    orientation = None  # Orientation is determined dynamically (None initially)
    font = pygame.font.Font(None, 36)  # Font for displaying text
    message = ""  # Message to display on the screen

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in ship_types and cells_to_place == 0:  # Select a ship type only if no ship is currently being placed
                    ship_type, ship_length, ship_limit = ship_types[event.key]
                    if ship_counts[event.key] < ship_limit:  # Check if the limit is reached
                        selected_ship = (ship_type, ship_length)
                        cells_to_place = ship_length  # Set the number of cells to place
                        placed_cells = []  # Reset the placed cells for the new ship
                        orientation = None  # Reset orientation for the new ship
                        message = f"{ship_type} selected! Place the ship."
                        print(f"Selected {ship_type} with length {ship_length}")
                    else:
                        message = f"Limit reached for {ship_type}!"
                        print(f"Limit reached for {ship_type}!")
            elif event.type == pygame.MOUSEBUTTONDOWN and selected_ship:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE
                ship_type, ship_length = selected_ship

                # Validate the placement of the current cell
                if cells_to_place > 0 and grid[row][col] == EMPTY and is_valid_cell(grid, row, col, placed_cells, orientation, ship_length):
                    grid[row][col] = ship_type
                    placed_cells.append((row, col))  # Add the cell to the placed cells
                    cells_to_place -= 1  # Decrease the number of cells left to place
                    print(f"Placed part of {ship_type} at ({row}, {col})")

                    # Determine orientation after placing the second cell
                    if len(placed_cells) == 2:
                        first_row, first_col = placed_cells[0]
                        second_row, second_col = placed_cells[1]
                        if first_row == second_row:
                            orientation = 0  # Horizontal
                        elif first_col == second_col:
                            orientation = 1  # Vertical

                    # If all cells for the current ship are placed
                    if cells_to_place == 0:
                        print(f"Finished placing {ship_type}")
                        message = f"{ship_type} placed!"
                        # Increment the count for the placed ship
                        for key, value in ship_types.items():
                            if value[0] == ship_type:
                                ship_counts[key] += 1
                                break
                        selected_ship = None  # Reset selection after placing the ship
                else:
                    message = "Invalid placement. Ensure the cell follows the rules."
                    print("Invalid placement. Ensure the cell follows the rules.")

        # Check if all ships have been placed
        if all(ship_counts[key] == ship_types[key][2] for key in ship_types):
            print("All ships placed!")
            message = "All ships placed!"
            WINDOW.fill((0, 0, 0))
            draw_grid()
            rendered_text = font.render(message, True, (255, 255, 255))
            WINDOW.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(3000)  # Display the message for 3 seconds
            return True  # Indicate that manual setup is complete

        # Draw the grid and update the display
        WINDOW.fill((0, 0, 0))
        draw_grid()
        rendered_text = font.render(message, True, (255, 255, 255))
        WINDOW.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, HEIGHT - 50))
        pygame.display.update()
        
def is_valid_cell(grid, row, col, placed_cells, orientation, ship_length):
    """
    Check if the cell is valid for placement based on the rules:
    - The cell must be adjacent to the previously placed cell (if any).
    - The cell must not overlap with other ships.
    - The cell must not be adjacent to other ships.
    - There must be enough space to place the full ship.
    """
    # Ensure the cell is within bounds
    if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
        return False

    # Ensure the cell is empty
    if grid[row][col] != EMPTY:
        return False

    # Ensure the cell is not adjacent to other ships
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            adj_row, adj_col = row + dr, col + dc
            if 0 <= adj_row < GRID_SIZE and 0 <= adj_col < GRID_SIZE:
                if grid[adj_row][adj_col] != EMPTY and (adj_row, adj_col) not in placed_cells:
                    return False

    # If this is the first cell, no need to check adjacency to the last placed cell
    if not placed_cells:
        return True

    # Get the last placed cell
    last_row, last_col = placed_cells[-1]

    # Check if the cell is adjacent to the last placed cell
    if orientation is None:  # No orientation determined yet
        if abs(row - last_row) + abs(col - last_col) != 1:
            return False

        # Check if there is enough space in both directions for the full ship
        remaining_cells = ship_length - len(placed_cells)
        if row == last_row:  # Horizontal placement
            # Check left and right
            right_space = col + remaining_cells - 1 < GRID_SIZE
            left_space = col - (remaining_cells - 1) >= 0
            if not (right_space or left_space):
                return False
        elif col == last_col:  # Vertical placement
            # Check up and down
            down_space = row + remaining_cells - 1 < GRID_SIZE
            up_space = row - (remaining_cells - 1) >= 0
            if not (down_space or up_space):
                return False

    elif orientation == 0:  # Horizontal
        if row != last_row or abs(col - last_col) != 1:
            return False
        # Check if there is enough space to the right for the remaining cells
        remaining_cells = ship_length - len(placed_cells)
        if col + remaining_cells - 1 >= GRID_SIZE or any(grid[row][col + i] != EMPTY for i in range(remaining_cells)):
            return False

    elif orientation == 1:  # Vertical
        if col != last_col or abs(row - last_row) != 1:
            return False
        # Check if there is enough space downward for the remaining cells
        remaining_cells = ship_length - len(placed_cells)
        if row + remaining_cells - 1 >= GRID_SIZE or any(grid[row + i][col] != EMPTY for i in range(remaining_cells)):
            return False

    return True
        
def setup_ships(grid):
    """
    Place all ships on the grid using the random placement function.
    """
    # Clear the grid before placing ships
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            grid[row][col] = EMPTY

    success = place_ships_randomly(grid)
    if not success:
        print("Failed to place all ships. Please try again.")
        
def main():
    pygame.init()

    # Display a menu for the player to choose ship placement method
    font = pygame.font.Font(None, 36)
    menu_text = [
        "Press R for Random Ship Placement",
        "Press M for Manual Ship Placement"
    ]

    setup_complete = False  # Flag to indicate if setup is complete

    # Menu loop
    while not setup_complete:
        WINDOW.fill((0, 0, 0))  # Clear the screen
        for i, text in enumerate(menu_text):
            rendered_text = font.render(text, True, (255, 255, 255))
            WINDOW.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, HEIGHT // 2 - 50 + i * 40))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Random placement
                    setup_ships(grid)
                    print("Ships placed randomly:")
                    for row in grid:  # Debugging: Print the grid to the console
                        print(row)
                    WINDOW.fill((0, 0, 0))  # Clear the screen before drawing the grid
                    draw_grid()  # Redraw the grid with the placed ships
                    pygame.display.update()  # Update the display
                    setup_complete = True  # Mark setup as complete
                elif event.key == pygame.K_m:  # Manual placement
                    if manual_setup(grid):  # Check if manual setup is complete
                        setup_complete = True  # Mark setup as complete

    # Main game loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        WINDOW.fill((0, 0, 0))  # Clear the screen
        draw_grid()  # Draw the grid with ships
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
    