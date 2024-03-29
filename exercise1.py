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

# Initialize grid and parameters
width, height = 9, 7
grid = [['.' for _ in range(width)] for _ in range(height)]
walls = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]  # Wall positions
inlet = (4, 4)  # Inlet position

# Place walls on the grid
for (wx, wy) in walls:
    grid[wy][wx] = '#'

# Simulate the grain falling
simulation_finished = False
while not simulation_finished:
    grid, simulation_finished = simulate_grain(grid, inlet, simulation_finished)

# Place the inlet on the grid (if not occupied by a grain)
if (grid[inlet[1]][inlet[0]] != 'o'):
    grid[inlet[1]][inlet[0]] = '+'

# Count sand grains
sand_count = sum(row.count('o') for row in grid)

# Print the final grid and sand count
print_grid(grid)
print(f"Ziarenka: {sand_count}")
