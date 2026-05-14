import pygame
import random
import sys
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional

pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
GRID_SIZE = 8
TILE_SIZE = (WINDOW_WIDTH - 40) // GRID_SIZE
PADDING = 20
FPS = 60
ANIMATION_SPEED = 0.1

# Colors
COLORS = [
    (255, 0, 0),      # Red
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (255, 255, 0),    # Yellow
    (255, 165, 0),    # Orange
    (255, 0, 255),    # Magenta
]
BG_COLOR = (50, 50, 50)
GRID_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 255, 255)


class AnimationType(Enum):
    SWAP = 1
    DISAPPEAR = 2
    FALL = 3


@dataclass
class Animation:
    anim_type: AnimationType
    tile_pos: Tuple[int, int]
    start_pos: Tuple[float, float]
    end_pos: Tuple[float, float]
    duration: float
    elapsed: float = 0.0
    target_tile_pos: Optional[Tuple[int, int]] = None


class Tile:
    def __init__(self, row: int, col: int, color_idx: int):
        self.row = row
        self.col = col
        self.color_idx = color_idx
        self.color = COLORS[color_idx]
        self.x = PADDING + col * TILE_SIZE + TILE_SIZE // 2
        self.y = PADDING + row * TILE_SIZE + TILE_SIZE // 2
        self.matched = False

    def draw(self, screen, offset_x=0, offset_y=0):
        x = self.x + offset_x
        y = self.y + offset_y
        pygame.draw.rect(screen, self.color, (x - TILE_SIZE // 2 + 2, y - TILE_SIZE // 2 + 2, TILE_SIZE - 4, TILE_SIZE - 4), border_radius=5)
        pygame.draw.rect(screen, GRID_COLOR, (x - TILE_SIZE // 2 + 2, y - TILE_SIZE // 2 + 2, TILE_SIZE - 4, TILE_SIZE - 4), 3, border_radius=5)


class CandyCrushGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Candy Crush")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.score = 0
        self.selected_tile: Optional[Tuple[int, int]] = None
        self.animations: List[Animation] = []
        self.grid: List[List[Optional[Tile]]] = []
        self.initialize_grid()

    def initialize_grid(self):
        self.grid = []
        for row in range(GRID_SIZE):
            grid_row = []
            for col in range(GRID_SIZE):
                color_idx = random.randint(0, len(COLORS) - 1)
                grid_row.append(Tile(row, col, color_idx))
            self.grid.append(grid_row)
        self.remove_initial_matches()

    def remove_initial_matches(self):
        """Remove any matches from initial grid"""
        for _ in range(100):
            self.find_and_mark_matches()
            if not any(tile.matched for row in self.grid for tile in row if tile):
                break
            self.remove_marked_tiles()
            self.apply_gravity()
            self.spawn_new_tiles()

    def find_and_mark_matches(self):
        """Mark all matched tiles"""
        # Horizontal matches
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE - 2):
                if self.grid[row][col] and self.grid[row][col + 1] and self.grid[row][col + 2]:
                    if (self.grid[row][col].color_idx == self.grid[row][col + 1].color_idx ==
                        self.grid[row][col + 2].color_idx):
                        self.grid[row][col].matched = True
                        self.grid[row][col + 1].matched = True
                        self.grid[row][col + 2].matched = True

        # Vertical matches
        for col in range(GRID_SIZE):
            for row in range(GRID_SIZE - 2):
                if self.grid[row][col] and self.grid[row + 1][col] and self.grid[row + 2][col]:
                    if (self.grid[row][col].color_idx == self.grid[row + 1][col].color_idx ==
                        self.grid[row + 2][col].color_idx):
                        self.grid[row][col].matched = True
                        self.grid[row + 1][col].matched = True
                        self.grid[row + 2][col].matched = True

    def remove_marked_tiles(self):
        """Remove matched tiles and create animations"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] and self.grid[row][col].matched:
                    tile = self.grid[row][col]
                    anim = Animation(
                        anim_type=AnimationType.DISAPPEAR,
                        tile_pos=(row, col),
                        start_pos=(tile.x, tile.y),
                        end_pos=(tile.x, tile.y),
                        duration=0.3
                    )
                    self.animations.append(anim)
                    self.score += 10
                    self.grid[row][col] = None

    def apply_gravity(self):
        """Make tiles fall down"""
        for col in range(GRID_SIZE):
            write_pos = GRID_SIZE - 1
            for row in range(GRID_SIZE - 1, -1, -1):
                if self.grid[row][col]:
                    if row != write_pos:
                        # Create fall animation
                        tile = self.grid[row][col]
                        old_row = row
                        self.grid[row][col] = None
                        self.grid[write_pos][col] = tile
                        tile.row = write_pos

                        start_x = PADDING + col * TILE_SIZE + TILE_SIZE // 2
                        start_y = PADDING + old_row * TILE_SIZE + TILE_SIZE // 2
                        end_y = PADDING + write_pos * TILE_SIZE + TILE_SIZE // 2

                        anim = Animation(
                            anim_type=AnimationType.FALL,
                            tile_pos=(write_pos, col),
                            start_pos=(start_x, start_y),
                            end_pos=(start_x, end_y),
                            duration=0.2
                        )
                        self.animations.append(anim)
                    write_pos -= 1

    def spawn_new_tiles(self):
        """Spawn new tiles at the top"""
        for col in range(GRID_SIZE):
            for row in range(GRID_SIZE):
                if self.grid[row][col] is None:
                    color_idx = random.randint(0, len(COLORS) - 1)
                    new_tile = Tile(row, col, color_idx)
                    new_tile.y = PADDING - TILE_SIZE
                    self.grid[row][col] = new_tile

                    target_y = PADDING + row * TILE_SIZE + TILE_SIZE // 2
                    anim = Animation(
                        anim_type=AnimationType.FALL,
                        tile_pos=(row, col),
                        start_pos=(new_tile.x, new_tile.y),
                        end_pos=(new_tile.x, target_y),
                        duration=0.3
                    )
                    self.animations.append(anim)
                    break

    def update_animations(self, dt: float):
        """Update all active animations"""
        completed = []
        for anim in self.animations:
            anim.elapsed += dt
            progress = min(anim.elapsed / anim.duration, 1.0)

            if anim.anim_type == AnimationType.SWAP:
                row, col = anim.tile_pos
                if self.grid[row][col]:
                    tile = self.grid[row][col]
                    tile.x = anim.start_pos[0] + (anim.end_pos[0] - anim.start_pos[0]) * progress
                    tile.y = anim.start_pos[1] + (anim.end_pos[1] - anim.start_pos[1]) * progress

            elif anim.anim_type == AnimationType.FALL:
                row, col = anim.tile_pos
                if self.grid[row][col]:
                    tile = self.grid[row][col]
                    tile.y = anim.start_pos[1] + (anim.end_pos[1] - anim.start_pos[1]) * progress

            elif anim.anim_type == AnimationType.DISAPPEAR:
                row, col = anim.tile_pos
                # Animation completes when progress reaches 1.0

            if progress >= 1.0:
                completed.append(anim)

        for anim in completed:
            self.animations.remove(anim)

    def swap_tiles(self, pos1: Tuple[int, int], pos2: Tuple[int, int]):
        """Swap two tiles and check for matches"""
        r1, c1 = pos1
        r2, c2 = pos2

        self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]

        if self.grid[r1][c1]:
            self.grid[r1][c1].row = r1
            self.grid[r1][c1].col = c1
        if self.grid[r2][c2]:
            self.grid[r2][c2].row = r2
            self.grid[r2][c2].col = c2

        self.find_and_mark_matches()
        if any(tile.matched for row in self.grid for tile in row if tile):
            self.remove_marked_tiles()
        else:
            # Swap back if no matches
            self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]
            if self.grid[r1][c1]:
                self.grid[r1][c1].row = r1
                self.grid[r1][c1].col = c1
            if self.grid[r2][c2]:
                self.grid[r2][c2].row = r2
                self.grid[r2][c2].col = c2

    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse click"""
        x, y = pos
        if x < PADDING or x >= WINDOW_WIDTH - PADDING or y < PADDING or y >= WINDOW_HEIGHT - PADDING:
            return

        col = (x - PADDING) // TILE_SIZE
        row = (y - PADDING) // TILE_SIZE

        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            if self.selected_tile is None:
                self.selected_tile = (row, col)
            else:
                sr, sc = self.selected_tile
                if (row, col) == self.selected_tile:
                    self.selected_tile = None
                elif abs(row - sr) + abs(col - sc) == 1:  # Adjacent tiles
                    self.swap_tiles((sr, sc), (row, col))
                    self.selected_tile = None
                else:
                    self.selected_tile = (row, col)

    def draw(self):
        """Draw the game"""
        self.screen.fill(BG_COLOR)

        # Draw grid background
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = PADDING + col * TILE_SIZE
                y = PADDING + row * TILE_SIZE
                pygame.draw.rect(self.screen, (100, 100, 100), (x, y, TILE_SIZE, TILE_SIZE))

        # Draw tiles
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                tile = self.grid[row][col]
                if tile and not tile.matched:
                    offset_x = 0
                    offset_y = 0

                    # Find any active animations for this tile
                    for anim in self.animations:
                        if anim.tile_pos == (row, col) and anim.anim_type != AnimationType.DISAPPEAR:
                            continue

                    tile.draw(self.screen, offset_x, offset_y)

                    # Draw selection highlight
                    if self.selected_tile == (row, col):
                        x = PADDING + col * TILE_SIZE + TILE_SIZE // 2
                        y = PADDING + row * TILE_SIZE + TILE_SIZE // 2
                        pygame.draw.circle(self.screen, (255, 255, 255), (x, y), TILE_SIZE // 2 + 5, 3)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (20, 10))

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.update_animations(dt)

            # Check for matches after animations complete
            if not self.animations:
                if any(tile.matched for row in self.grid for tile in row if tile):
                    self.remove_marked_tiles()
                else:
                    self.find_and_mark_matches()
                    if any(tile.matched for row in self.grid for tile in row if tile):
                        self.remove_marked_tiles()
                    else:
                        self.apply_gravity()
                        self.spawn_new_tiles()

            self.draw()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = CandyCrushGame()
    game.run()
