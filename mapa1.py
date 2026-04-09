import pygame
import sys


class Tile:
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)

    def draw(self, screen, x, y):
        screen.blit(self.image, (x, y))


class Map:
    def __init__(self, tile_size):
        self.tile_size = tile_size
        self.rows = 30
        self.cols = 30
        
        self.grid = [
            [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,1,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,1,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,1,1,0,0,0],
            [0,0,1,1,1,1,0,0,0,0,0,1,0,0,0],
            [0,0,1,0,0,1,0,0,0,0,0,1,0,0,0],
            [0,0,1,0,0,1,1,1,1,1,1,1,0,0,0],
            [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
        ]

        self.road_tile = Tile(self.tile_size, (0, 0, 0))        # černá cesta
        self.grass_tile = Tile(self.tile_size, (0, 180, 0))     # zelené pozadí

    def draw(self, screen):
        for y in range(self.rows):
            for x in range(self.cols):
                px = x * self.tile_size
                py = y * self.tile_size

                if self.grid[y][x] == 1:
                    self.road_tile.draw(screen, px, py)
                else:
                    self.grass_tile.draw(screen, px, py)

                pygame.draw.rect(screen, (100, 100, 100), (px, py, self.tile_size, self.tile_size), 1)


class Game:
    def __init__(self):
        pygame.init()

        self.tile_size = 32
        self.map = Map(self.tile_size)

        self.width = self.map.cols * self.tile_size
        self.height = self.map.rows * self.tile_size

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("OOP cesta v Pygame")

        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.map.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()