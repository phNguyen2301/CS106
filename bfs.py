import pygame
from pygame.locals import *
import sys
import random
from helper import plot

pygame.init()
font = pygame.font.Font('arial.ttf', 20)

# class Direction(Enum):
#     RIGHT = 1
#     LEFT = 2
#     UP = 3
#     DOWN = 4

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 100)
BLACK = (0, 0, 0)

BLOCK_SIZE = 40
SPEED = 200

WIDTH = 800
HEIGHT = 800


class SnakeGame:

    def __init__(self, w=WIDTH, h=HEIGHT):
        self.GameOver = False
        self.w = w
        self.h = h
        self.boardW = w // BLOCK_SIZE
        self.boardH = h // BLOCK_SIZE
        self.board = [[0 for _ in range(0, self.boardW)]
                      for _ in range(0, self.boardH)]
        self.boardTup = set(tuple([xB, yB]) for xB in range(
            0, self.boardW) for yB in range(0, self.boardH))
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # init game state
        self.GameOver = False
        self.direction = 0
        self.head = [(self.boardW)/2, (self.boardH)/2]
        # self.snake = [self.head]
        self.snake = [[self.head[0], self.head[1]],
                      [self.head[0]-1, self.head[1]],
                      [self.head[0]-2, self.head[1]],
                      [self.head[0]-3, self.head[1]]]

        self.score = 0
        self._place_food()

    def _place_food(self):
        snakeTup = set(tuple(snakePix) for snakePix in self.snake)
        possibleLoc = list(self.boardTup - snakeTup)
        chosenLoc = list(possibleLoc[random.randint(0, len(possibleLoc) - 1)])
        self.food = chosenLoc

    def _update_ui(self):
        self.display.fill(BLACK)
        pygame.draw.rect(self.display, GREEN, pygame.Rect(
            self.head[0]*BLOCK_SIZE, self.head[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, RED, pygame.Rect(
            self.snake[1][0]*BLOCK_SIZE, self.snake[1][1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        for pt in self.snake[2:-1]:
            pygame.draw.rect(self.display, BLUE, pygame.Rect(
                pt[0]*BLOCK_SIZE, pt[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(self.display, RED, pygame.Rect(
            self.food[0]*BLOCK_SIZE, self.food[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def is_collision_boundary(self, snakeLoc):
        return (0 <= snakeLoc[0] < self.boardW) and (0 <= snakeLoc[1] < self.boardH)

    def checkAndMove(self, nextDirection):
        if (len(self.snake) > 1):
            if nextDirection == 0 and self.direction != 2:
                self.direction = 0
                self.head[0] += 1

            elif nextDirection == 1 and self.direction != 3:
                self.direction = 1
                self.head[1] += -1

            elif nextDirection == 2 and self.direction != 0:
                self.direction = 2
                self.head[0] += -1

            elif nextDirection == 3 and self.direction != 1:
                self.direction = 3
                self.head[1] += 1

        else:
            if nextDirection == 0:
                self.direction = 0
                self.head[0] += 1

            elif nextDirection == 1:
                self.direction = 1
                self.head[1] += -1

            elif nextDirection == 2:
                self.direction = 2
                self.head[0] += -1

            elif nextDirection == 3:
                self.direction = 3
                self.head[1] += 1
        self.snake.insert(0, [self.head[0], self.head[1]])

    def checkGameOver(self):
        if self.head[0] >= self.boardW or self.head[0] < 0 or self.head[1] >= self.boardH or self.head[1] < 0:
            self.GameOver = True
        if self.head in self.snake[1:]:
            self.GameOver = True

    def snakeBFS(self):
        alreadyTraveled = []
        directionQueue = [[]]
        snakeQueue = [self.snake]
        while snakeQueue:
            curSnake = snakeQueue.pop(0)
            curDirection = directionQueue.pop(0)
            if (self.food[0] == curSnake[0][0] and self.food[1] == curSnake[0][1]):
                safePathToTail = self.getPathToTail(curSnake)
                if safePathToTail is not None and len(safePathToTail) != 0:
                    return curDirection

            if not ((0 <= curSnake[0][0] < self.boardW) and (0 <= curSnake[0][1] < self.boardH) and (curSnake[0] not in curSnake[1:]) and (curSnake[0] not in alreadyTraveled)):
                continue
            else:
                alreadyTraveled.append(curSnake[0])
                new_Snake = [snakePix[:] for snakePix in curSnake]
                new_Snake.insert(0, [new_Snake[0][0] + 1, new_Snake[0][1]])
                new_Snake.pop(-1)
                snakeQueue.append(new_Snake)

                new_Snake = [snakePix[:] for snakePix in curSnake]
                new_Snake.insert(0, [new_Snake[0][0], new_Snake[0][1] - 1])
                new_Snake.pop(-1)
                snakeQueue.append(new_Snake)

                new_Snake = [snakePix[:] for snakePix in curSnake]
                new_Snake.insert(0, [new_Snake[0][0] - 1, new_Snake[0][1]])
                new_Snake.pop(-1)
                snakeQueue.append(new_Snake)

                new_Snake = [snakePix[:] for snakePix in curSnake]
                new_Snake.insert(0, [new_Snake[0][0], new_Snake[0][1] + 1])
                new_Snake.pop(-1)
                snakeQueue.append(new_Snake)

                for d in range(0, 4):
                    newDirection = curDirection[:]
                    newDirection.append(d)
                    directionQueue.append(newDirection)
        return []

    def getPathToTail(self, testSnake):
        tail = [testSnake[-1][0], testSnake[-1][1]]

        alreadyTraveled = []
        directionQueue = [[]]
        snakeQueue = [testSnake]
        while snakeQueue:
            curSnake = snakeQueue.pop(0)
            curDirection = directionQueue.pop(0)
            if (tail[0] == curSnake[0][0] and tail[1] == curSnake[0][1]):
                return curDirection
            if not ((0 <= curSnake[0][0] < self.boardW) and (0 <= curSnake[0][1] < self.boardH) and (curSnake[0] not in curSnake[1:]) and (curSnake[0] not in alreadyTraveled)):
                continue
            else:
                alreadyTraveled.append(curSnake[0])
                new_Snake = [snakePix[:] for snakePix in curSnake]
                new_Snake.insert(0, [new_Snake[0][0] + 1, new_Snake[0][1]])
                new_Snake.pop(-1)
                snakeQueue.append(new_Snake)

                new_Snake = [snakePix[:] for snakePix in curSnake]
                new_Snake.insert(0, [new_Snake[0][0], new_Snake[0][1] - 1])
                new_Snake.pop(-1)
                snakeQueue.append(new_Snake)

                new_Snake = [snakePix[:] for snakePix in curSnake]
                new_Snake.insert(0, [new_Snake[0][0] - 1, new_Snake[0][1]])
                new_Snake.pop(-1)
                snakeQueue.append(new_Snake)

                new_Snake = [snakePix[:] for snakePix in curSnake]
                new_Snake.insert(0, [new_Snake[0][0], new_Snake[0][1] + 1])
                new_Snake.pop(-1)
                snakeQueue.append(new_Snake)

                for d in range(0, 4):
                    newDirection = curDirection[:]
                    newDirection.append(d)
                    directionQueue.append(newDirection)
        return []

    def getNextMove(self):
        directionList = self.snakeBFS()
        if directionList is not None and len(directionList) != 0:
            return directionList
        pathToTail = self.getPathToTail(self.snake)
        if pathToTail is not None and len(pathToTail) != 0:
            return pathToTail
        print("stuck")


def play():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    game = SnakeGame()
    MAX = 1
    n = 1
    while n <= MAX:
        directionList = []
        while not game.GameOver:
            game._update_ui()
            game.clock.tick(SPEED)
            game.checkGameOver()
            if len(directionList) == 0:
                directionList = game.getNextMove()
            if directionList is not None and len(directionList) != 0:
                game.checkAndMove(directionList.pop(0))
            else:
                break
            if game.head == game.food:
                game.score += 1
                game._place_food()
            else:
                game.snake.pop(-1)

        if game.score > record:
            record = game.score
        print('Game', n, 'Score', game.score, 'Record:', record)
        # plot_scores.append(game.score)
        # total_score += game.score
        # mean_score = total_score / n
        # plot_mean_scores.append(mean_score)
        # plot(plot_scores, plot_mean_scores, n)
        game.reset()
        n += 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    play()
