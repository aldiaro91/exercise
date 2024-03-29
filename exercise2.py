def print_grid(grid):
    for row in reversed(grid):  # The grid is reversed for display (0,0 at bottom left)
        print(' '.join(row))

def simulate_grain(grid, inlet, simulation_finished):
    x, y = inlet
    while True:
        below = (x, y - 1)
        below_right = (x + 1, y - 1) if x + 1 < len(grid[0]) else None
        below_left = (x - 1, y - 1) if x - 1 >= 0 else None

        # If the grain cannot move down, down-right, or down-left
        if y == 0 or (grid[y-1][x] != '.' and
                      (below_right is None or grid[below_right[1]][below_right[0]] != '.') and
                      (below_left is None or grid[below_left[1]][below_left[0]] != '.')):
            # ... and if the grain will move out of bounds after falling further
            if (y == 0 or below_right is None or below_left is None):
                simulation_finished = True
                grid[y][x] = '.'  # Remove the grain from the current position (because it will fall out of the map)
            elif ((x, y) == inlet):
                grid[y][x] = 'o'
                simulation_finished = True
            break

        grid[y][x] = '.'  # Remove the grain from the current position before placing it somewhere else

        # Move the sand grain down if possible
        if below and grid[below[1]][below[0]] == '.':
            y -= 1
        # Move the sand grain down-right if possible
        elif below_right and grid[below_right[1]][below_right[0]] == '.':
            x += 1
            y -= 1
        # Move the sand grain down-left if possible
        elif below_left and grid[below_left[1]][below_left[0]] == '.':
            x -= 1
            y -= 1

        grid[y][x] = 'o'

    return (grid, simulation_finished)

def get_user_input():
    # Get the grid dimensions from the user and validate them
    while True:
        try:
            width, height = map(int, input("Enter grid width and height (e.g., '10 10'): ").split())
            if not (5 <= width <= 100) or not (5 <= height <= 100):
                raise ValueError("Width and height must be between 5 and 100.")
            break
        except ValueError as e:
            print(e)

    grid = [['.' for _ in range(width)] for _ in range(height)]
    walls = []

    while True:
        # Get wall positions from the user
        user_input = input("Enter 'r' to add a wall, 's' to add the inlet: ")
        if user_input == 'r':
            x1, y1, x2, y2 = map(int, input("Enter the bottom left and top right coordinates of the wall (e.g., '1 2 3 4'): ").split())
            # Check if the coordinates are within the grid and non-negative
            if 0 <= x1 < width and 0 <= y1 < height and 0 <= x2 < width and 0 <= y2 < height and x1 <= x2 and y1 <= y2:
                # Place the wall
                for x in range(x1, x2+1):
                    for y in range(y1, y2+1):
                        grid[y][x] = '#'  
                # Store wall coordinates for later validation
                walls.extend([(x, y) for x in range(x1, x2+1) for y in range(y1, y2+1)])
            else:
                print("Invalid wall coordinates. They must be non-negative integers within the grid.")
        elif user_input == 's':
            inlet_x, inlet_y = map(int, input("Enter the x and y coordinates of the inlet (e.g., '3 8'): ").split())
            # Check if the inlet coordinates are within the grid, non-negative, and not inside a wall
            if 0 <= inlet_x < width and 0 <= inlet_y < height and (inlet_x, inlet_y) not in walls:
                grid[inlet_y][inlet_x] = '+'  # Place the inlet
                inlet = (inlet_x, inlet_y)
                break  # Once the inlet is placed, we are ready to start the simulation
            else:
                print("Invalid inlet coordinates. They must be non-negative integers within the grid and not inside walls.")

    return grid, inlet, width, height

# Get user-defined map parameters
grid, inlet, width, height = get_user_input()

# Simulate the grain falling
simulation_finished = False
while not simulation_finished:
    grid, simulation_finished = simulate_grain(grid, inlet, simulation_finished)

# Make sure the inlet is still visible if not occupied by a grain (it may be overwritten by "." while running the simulation)
if (grid[inlet[1]][inlet[0]] != 'o'):
    grid[inlet[1]][inlet[0]] = '+'

# Count sand grains
sand_count = sum(row.count('o') for row in grid)

# Print the final grid and sand count
print_grid(grid)
print(f"Ziarenka: {sand_count}")

