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

def draw_grid(grid):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(WINDOW, (255, 255, 255), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(WINDOW, (255, 255, 255), (0, y), (WIDTH, y))
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

def place_ships_randomly(grid, ship_coordinates):
    """
    Randomly place all ships on the grid and store their coordinates in a dictionary of sets.
    """
    ship_types = [
        (CARRIER, 5),       # 1 Carrier
        (BATTLESHIP, 4),    # 2 Battleships
        (CRUISER, 3),       # 3 Cruisers
        (DESTROYER, 1)      # 4 Destroyers
    ]
    ship_counts = [1, 2, 3, 4]  # Number of each ship type to place

    for (ship_type, ship_length), count in zip(ship_types, ship_counts):
        for ship_number in range(1, count + 1):
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
                        # Place the ship and store its coordinates
                        ship_coords = set()
                        for i in range(ship_length):
                            grid[row][col + i] = ship_type
                            ship_coords.add((row, col + i))
                        ship_coordinates[f"{ship_type} {ship_number}"] = ship_coords
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
                        # Place the ship and store its coordinates
                        ship_coords = set()
                        for i in range(ship_length):
                            grid[row + i][col] = ship_type
                            ship_coords.add((row + i, col))
                        ship_coordinates[f"{ship_type} {ship_number}"] = ship_coords
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
    """
    Allow the player to manually place ships on the grid.
    """
    # Define ship types, lengths, and limits
    ship_types = {
        pygame.K_1: (DESTROYER, 1, 4),  # Key 1 for Destroyer (4 allowed)
        pygame.K_2: (CRUISER, 3, 3),   # Key 2 for Cruiser (3 allowed)
        pygame.K_3: (BATTLESHIP, 4, 2),  # Key 3 for Battleship (2 allowed)
        pygame.K_4: (CARRIER, 5, 1)    # Key 4 for Carrier (1 allowed)
    }
    ship_counts = {key: 0 for key in ship_types}  # Track how many of each ship have been placed
    ship_coordinates = {}  # Dictionary to store ship coordinates
    selected_ship = None  # Currently selected ship type and length
    cells_to_place = 0  # Number of cells left to place for the current ship
    placed_cells = []  # Track the cells already placed for the current ship
    orientation = None  # Orientation is determined dynamically (None initially)
    font = pygame.font.Font(None, 36)  # Font for displaying text
    message = ""  # Message to display on the screen
    hovered_cell = None  # Track the cell the mouse is hovering over

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEMOTION:
                # Track the cell the mouse is hovering over
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    hovered_cell = (row, col)
                else:
                    hovered_cell = None
            elif event.type == pygame.KEYDOWN:  # Ensure event has a key attribute
                if event.key in ship_types and cells_to_place == 0:  # Select a ship type only if no ship is currently being placed
                    ship_type, ship_length, ship_limit = ship_types[event.key]
                    if ship_counts[event.key] < ship_limit:  # Check if the limit is reached
                        selected_ship = (ship_type, ship_length, event.key)  # Store the key for ship_counts
                        cells_to_place = ship_length  # Set the number of cells to place
                        placed_cells = []  # Reset the placed cells for the new ship
                        orientation = None  # Reset orientation for the new ship
                        message = f"{ship_type} selected! Place the ship."
                        print(f"Selected {ship_type} with length {ship_length}")
                    else:
                        message = f"Limit reached for {ship_type}!"
                        print(f"Limit reached for {ship_type}!")
                elif event.key == pygame.K_0:  # Press 0 to remove the ship being placed
                    if placed_cells:
                        # Remove the cells of the ship being placed
                        for row, col in placed_cells:
                            grid[row][col] = EMPTY
                        placed_cells = []  # Clear the placed cells
                        cells_to_place = 0  # Reset the number of cells to place
                        selected_ship = None  # Reset the selected ship
                        message = "Ship placement canceled. Select a new ship to place."
                        print("Ship placement canceled.")  # Debug print
                    elif hovered_cell:  # Remove an already placed ship if hovering over it
                        row, col = hovered_cell
                        ship_to_remove = None
                        for ship_name, ship_coords in ship_coordinates.items():
                            if (row, col) in ship_coords:
                                ship_to_remove = ship_name
                                break

                        if ship_to_remove:
                            # Remove the ship from the grid
                            for r, c in ship_coordinates[ship_to_remove]:
                                grid[r][c] = EMPTY
                            # Remove the ship from the coordinates dictionary
                            del ship_coordinates[ship_to_remove]
                            message = f"{ship_to_remove} removed. Select a new ship to place."
                            print(f"{ship_to_remove} removed from the grid.")  # Debug print
                        else:
                            print("No ship to delete at hovered cell.")  # Debug print
            elif event.type == pygame.MOUSEBUTTONDOWN and selected_ship:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE
                ship_type, ship_length, ship_key = selected_ship

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
                        ship_name = f"{ship_type} {ship_counts[ship_key] + 1}"
                        ship_coordinates[ship_name] = set(placed_cells)  # Store the ship's coordinates
                        ship_counts[ship_key] += 1
                        selected_ship = None  # Reset selection after placing the ship
                else:
                    message = "Invalid placement. Ensure the cell follows the rules."
                    print("Invalid placement. Ensure the cell follows the rules.")

        # Check if all ships have been placed
        if all(ship_counts[key] == ship_types[key][2] for key in ship_types):
            print("All ships placed!")
            message = "All ships placed! Press Enter to proceed."
            WINDOW.fill((0, 0, 0))
            draw_grid(grid)  # Draw the final grid with ships visible
            rendered_text = font.render(message, True, (255, 255, 255))
            WINDOW.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, HEIGHT - 50))
            pygame.display.update()

            # Wait for the player to press Enter to proceed
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Enter key
                        return ship_coordinates  # Return the ship coordinates

        # Draw the grid and update the display
        WINDOW.fill((0, 0, 0))
        draw_grid(grid)  # Pass the correct grid

        # Highlight the hovered cell
        if hovered_cell:
            row, col = hovered_cell
            pygame.draw.rect(
                WINDOW,
                (255, 255, 0),  # Yellow highlight
                (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                3
            )

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

    # Initialize the ship coordinates dictionary
    ship_coordinates = {
        CARRIER: [],
        BATTLESHIP: [],
        CRUISER: [],
        DESTROYER: []
    }

    success = place_ships_randomly(grid, ship_coordinates)
    if not success:
        print("Failed to place all ships. Please try again.")
        return False, None

    return True, ship_coordinates

def draw_grid_with_label(grid, offset_x, label, hide_ships=True, destroyed_ships=None):
    """
    Draw a grid at a specific horizontal offset with a label above it.
    If hide_ships is True, ships will not be displayed (only hits and misses will be shown).
    """
    if destroyed_ships is None:
        destroyed_ships = []

    font = pygame.font.Font(None, 36)
    label_text = font.render(label, True, (255, 255, 255))
    WINDOW.blit(label_text, (offset_x + GRID_SIZE * CELL_SIZE // 2 - label_text.get_width() // 2, 10))  # Center the label above the grid

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = offset_x + col * CELL_SIZE  # Each cell is CELL_SIZE x CELL_SIZE
            y = 50 + row * CELL_SIZE
            pygame.draw.rect(WINDOW, (255, 255, 255), (x, y, CELL_SIZE, CELL_SIZE), 1)  # Draw grid lines

            # Draw hits and misses
            if grid[row][col] == "Hit":
                pygame.draw.circle(WINDOW, (0, 255, 0), (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 4)  # Green circle for hits
            elif grid[row][col] == "Miss":
                pygame.draw.circle(WINDOW, (255, 0, 0), (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 4)  # Red circle for misses

    # Draw lines connecting the dots for destroyed ships
    for ship_cells in destroyed_ships:
        if not isinstance(ship_cells, (list, set)) or len(ship_cells) < 2:
            print(f"Invalid ship data in destroyed_ships: {ship_cells}")  # Debug print
            continue  # Skip invalid data

        ship_cells = sorted(ship_cells)  # Sort the cells for consistent line drawing
        for i in range(len(ship_cells) - 1):
            try:
                start_row, start_col = ship_cells[i]
                end_row, end_col = ship_cells[i + 1]
                start_x = offset_x + start_col * CELL_SIZE + CELL_SIZE // 2
                start_y = 50 + start_row * CELL_SIZE + CELL_SIZE // 2
                end_x = offset_x + end_col * CELL_SIZE + CELL_SIZE // 2
                end_y = 50 + end_row * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.line(WINDOW, (0, 255, 0), (start_x, start_y), (end_x, end_y), 3)  # Green line
            except ValueError as e:
                print(f"Error unpacking ship cell: {e}")  # Debug print
                continue

def check_and_handle_ship_destruction(grid, hit_row, hit_col, destroyed_ships, ship_coordinates, original_ship_coordinates, destroyed_ships_coordinates):
    """
    Check if a ship is destroyed and handle marking surrounding cells.
    A ship is destroyed only when all its cells are hit.
    """
    hit_cell = (hit_row, hit_col)

    # Find the ship that contains the hit cell
    for ship_name, ship_coords in ship_coordinates.items():
        if hit_cell in ship_coords:
            # Remove the hit cell from the ship's coordinates
            ship_coords.remove(hit_cell)

            # Check if the ship is destroyed
            if not ship_coords:  # All cells of the ship are hit
                destroyed_ships.add(ship_name)  # Add the ship name to the destroyed ships
                destroyed_ships_coordinates[ship_name] = original_ship_coordinates[ship_name]  # Add the ship's coordinates
                print(f"Ship destroyed: {ship_name}")

                # Use the original coordinates to mark surrounding cells
                original_coords = original_ship_coordinates[ship_name]
                for row, col in original_coords:
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            adj_row, adj_col = row + dr, col + dc
                            if 0 <= adj_row < GRID_SIZE and 0 <= adj_col < GRID_SIZE:
                                if grid[adj_row][adj_col] not in ["Hit", "Miss"]:
                                    grid[adj_row][adj_col] = "Miss"  # Mark as miss
                                    print(f"Marked surrounding cell ({adj_row}, {adj_col}) as Miss")  # Debug print

                # Remove the destroyed ship from the ship_coordinates dictionary
                del ship_coordinates[ship_name]
            break

def battle_phase(player1_grid, player2_grid, player1_ship_coordinates, player2_ship_coordinates):
    """
    Handles the battle phase where players take turns shooting at each other's grids.
    """
    global WIDTH, CELL_SIZE, WINDOW  # Use global variables for window dimensions
    WIDTH = 1400  # Set the window width to 1400 to accommodate both grids and space
    CELL_SIZE = 50  # Each cell is 50x50 pixels
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battleship - Battle Phase")

    # Turn tracking
    player_turn = 1  # Player 1 starts

    # Hit counters for each player
    player1_hits = 0
    player2_hits = 0
    max_hits = 26  # Victory condition: 26 hits

    # Track destroyed ships for both players
    destroyed_ships_player1 = set()
    destroyed_ships_player2 = set()

    # Track destroyed ship coordinates for both players
    destroyed_ships_coordinates_player1 = {}
    destroyed_ships_coordinates_player2 = {}

    # Create unaltered copies of the ship coordinates
    original_player1_ship_coordinates = {k: v.copy() for k, v in player1_ship_coordinates.items()}
    original_player2_ship_coordinates = {k: v.copy() for k, v in player2_ship_coordinates.items()}

    # Main battle loop
    run = True
    winner = None  # Track the winner
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Determine which grid the player clicked on
                if player_turn == 1 and 750 <= mouse_x < 1250:  # Player 1 clicks on Player 2's grid
                    col = (mouse_x - 750) // CELL_SIZE
                    row = (mouse_y - 50) // CELL_SIZE
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                        if player2_grid[row][col] not in ["Hit", "Miss"]:
                            if player2_grid[row][col] != EMPTY:
                                player2_grid[row][col] = "Hit"  # Mark as hit
                                player1_hits += 1  # Increment Player 1's hit counter
                                check_and_handle_ship_destruction(
                                    player2_grid, row, col, destroyed_ships_player2, player2_ship_coordinates,
                                    original_player2_ship_coordinates, destroyed_ships_coordinates_player2
                                )
                                # Player 1 gets another turn
                            else:
                                player2_grid[row][col] = "Miss"  # Mark as miss
                                player_turn = 2  # Switch turn to Player 2
                elif player_turn == 2 and 150 <= mouse_x < 650:  # Player 2 clicks on Player 1's grid
                    col = (mouse_x - 150) // CELL_SIZE
                    row = (mouse_y - 50) // CELL_SIZE
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                        if player1_grid[row][col] not in ["Hit", "Miss"]:
                            if player1_grid[row][col] != EMPTY:
                                player1_grid[row][col] = "Hit"  # Mark as hit
                                player2_hits += 1  # Increment Player 2's hit counter
                                check_and_handle_ship_destruction(
                                    player1_grid, row, col, destroyed_ships_player1, player1_ship_coordinates,
                                    original_player1_ship_coordinates, destroyed_ships_coordinates_player1
                                )
                                # Player 2 gets another turn
                            else:
                                player1_grid[row][col] = "Miss"  # Mark as miss
                                player_turn = 1  # Switch turn to Player 1

        # Debugging: Print the hit counters
        print(f"Player 1 hits: {player1_hits} / {max_hits}")
        print(f"Player 2 hits: {player2_hits} / {max_hits}")

        # Check for a winner
        if player1_hits == max_hits:
            winner = "Player 1"
            break
        elif player2_hits == max_hits:
            winner = "Player 2"
            break

        # Draw the battle phase grids
        WINDOW.fill((0, 0, 0))  # Clear the screen
        draw_grid_with_label(player1_grid, 150, "Player 1", hide_ships=True, destroyed_ships=destroyed_ships_player1)
        draw_grid_with_label(player2_grid, 750, "Player 2", hide_ships=True, destroyed_ships=destroyed_ships_player2)

        # Display turn information
        font = pygame.font.Font(None, 36)
        turn_text = f"Player {player_turn}'s Turn"
        rendered_text = font.render(turn_text, True, (255, 255, 255))
        WINDOW.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, 10))

        pygame.display.update()

    # Display the winner and reveal ship layouts
    if winner:
        WINDOW.fill((0, 0, 0))  # Clear the screen
        font = pygame.font.Font(None, 72)
        winner_text = f"{winner} Wins!"
        rendered_text = font.render(winner_text, True, (255, 255, 255))
        # Move the winning text to the bottom of the screen
        WINDOW.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, HEIGHT - 100))

        # Draw both grids with original ship layouts revealed
        draw_grid_with_label(player1_grid, 150, "Player 1 (Original Layout)", hide_ships=False)
        draw_grid_with_label(player2_grid, 750, "Player 2 (Original Layout)", hide_ships=False)

        # Highlight original ship positions
        highlight_original_ships(original_player1_ship_coordinates, 150)
        highlight_original_ships(original_player2_ship_coordinates, 750)

        pygame.display.update()

        # Wait for the player to close the game
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    
def highlight_original_ships(original_coordinates, offset_x):
    
    
    """
    Highlight the original ship positions on the grid.
    """
    for ship_cells in original_coordinates.values():
        for row, col in ship_cells:
            x = offset_x + col * CELL_SIZE
            y = 50 + row * CELL_SIZE
            pygame.draw.rect(WINDOW, (0, 255, 255), (x, y, CELL_SIZE, CELL_SIZE), 3)  # Cyan border
def main():
    global WIDTH, CELL_SIZE, WINDOW  # Declare global variables at the start of the function
    pygame.init()

    # Initialize player grids
    player1_grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    player2_grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Menu font
    font = pygame.font.Font(None, 36)

    # Player 1's turn to place ships
    setup_complete = False
    while not setup_complete:
        WINDOW.fill((0, 0, 0))  # Clear the screen
        rendered_text = font.render("Player 1: Place your ships", True, (255, 255, 255))
        WINDOW.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, HEIGHT // 2 - 100))
        menu_text = [
            "Press R for Random Ship Placement",
            "Press M for Manual Ship Placement"
        ]
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
                    success, player1_ship_coordinates = setup_ships(player1_grid)
                    setup_complete = success
                elif event.key == pygame.K_m:  # Manual placement
                    player1_ship_coordinates = manual_setup(player1_grid)
                    setup_complete = True

    # Wait for Player 2 to start their turn
    WINDOW.fill((0, 0, 0))
    rendered_text = font.render("Player 2: Press Enter to start placing ships", True, (255, 255, 255))
    WINDOW.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Enter key
                waiting = False

    # Player 2's turn to place ships
    setup_complete = False
    while not setup_complete:
        WINDOW.fill((0, 0, 0))  # Clear the screen
        rendered_text = font.render("Player 2: Place your ships", True, (255, 255, 255))
        WINDOW.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, HEIGHT // 2 - 100))
        menu_text = [
            "Press R for Random Ship Placement",
            "Press M for Manual Ship Placement"
        ]
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
                    success, player2_ship_coordinates = setup_ships(player2_grid)
                    setup_complete = success
                elif event.key == pygame.K_m:  # Manual placement
                    player2_ship_coordinates = manual_setup(player2_grid)
                    setup_complete = True

    # Wait for the battle phase to start
    WINDOW.fill((0, 0, 0))
    rendered_text = font.render("Battle Phase: Press Enter to start", True, (255, 255, 255))
    WINDOW.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # Enter key
                waiting = False

    # Start the battle phase
    battle_phase(player1_grid, player2_grid, player1_ship_coordinates, player2_ship_coordinates)
    
if __name__ == "__main__":
    main()
    
