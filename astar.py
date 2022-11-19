from numpy import cos
import pygame
import random
import heapq
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
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 60

WIDTH = 640
HEIGHT = 480
class PriorityQueue:
    """Define a PriorityQueue data structure that will be used"""
    def  __init__(self):
        self.Heap = []
        self.Count = 0
        self.len = 0

    def push(self, item, priority):
        entry = (priority, self.Count, item)
        heapq.heappush(self.Heap, entry)
        self.Count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.Heap)
        return item

    def isEmpty(self):
        return len(self.Heap) == 0
class SnakeGame:

    def __init__(self, w=WIDTH , h=HEIGHT):
        self.GameOver = False
        self.w = w
        self.h = h
        self.boardW = w // BLOCK_SIZE
        self.boardH = h // BLOCK_SIZE
        self.board = [[0 for _ in range(0, self.boardW)] for _ in range (0, self.boardH)]
        self.boardTup = set(tuple([xB,yB]) for xB in range(0, self.boardW) for yB in range(0, self.boardH))
        # init display 
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
        # init game state
        self.GameOver = False
        self.direction = 0 # check direction 
        self.head = [(self.boardW)/2, (self.boardH)/2]
        # self.snake = [self.head]
        self.snake = [[self.head[0], self.head[1]],
                      [self.head[0]-1, self.head[1]],
                      [self.head[0]-2, self.head[1]]]

        self.score = 0
        self.food = [-2,-2]
        self._place_food()
     
    def _place_food(self):
        snakeTup = set(tuple(snakePix) for snakePix in self.snake)
        possibleLoc = list(self.boardTup - snakeTup)
        chosenLoc = list(possibleLoc[random.randint(0, len(possibleLoc) - 1)])
        self.food = chosenLoc
    
    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt[0]*BLOCK_SIZE, pt[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt[0]*BLOCK_SIZE+4, pt[1]*BLOCK_SIZE+4, BLOCK_SIZE - 8, BLOCK_SIZE - 8))
        
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food[0]*BLOCK_SIZE, self.food[1]*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def is_collision_boundary(self, snakeLoc):
        return (0<=snakeLoc[0]<self.boardW) and (0<=snakeLoc[1]<self.boardH)

    def manhattanDistance(self,snakeLoc):
        return (abs(snakeLoc[0] - self.food[0]) + abs(snakeLoc[1] - self.food[1]))

    def checkAndMove(self, nextDirection):
        if(len(self.snake) > 3):
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
        self.snake.insert(0,[self.head[0],self.head[1]])

    def checkGameOver(self):
        if self.head[0] >= self.boardW or self.head[0] < 0 or self.head[1] >= self.boardH or self.head[1] < 0: 
            self.GameOver = True
        if self.head in self.snake[1:]:
            self.GameOver = True

    def snakeBFS(self):
        alreadyTraveled = []
        directionQueue = PriorityQueue()
        directionQueue.push([], 0)
        snakeQueue = PriorityQueue()
        snakeQueue.push(self.snake, 0)
        while not snakeQueue.isEmpty():
            curSnake = snakeQueue.pop()
            curDirection = directionQueue.pop()
            if (self.food[0] == curSnake[0][0] and self.food[1] == curSnake[0][1]):
                return curDirection
            if not ((0 <= curSnake[0][0] < self.boardW) and (0 <= curSnake[0][1] < self.boardH) and (curSnake[0] not in curSnake[1:]) and (curSnake[0] not in alreadyTraveled)):
                continue
            else:
                alreadyTraveled.append(curSnake[0])
                new_Snake = [snakePix[:] for snakePix in curSnake]
                new_Snake.insert(0, [new_Snake[0][0] + 1, new_Snake[0][1]])
                new_Snake.pop(-1)
                cost = self.manhattanDistance(new_Snake[0])
                snakeQueue.push(new_Snake,cost)
                newDirection = curDirection[:]
                newDirection.append(0)
                directionQueue.push(newDirection, cost)

                new_Snake = [snakePix[:] for snakePix in curSnake]
                new_Snake.insert(0, [new_Snake[0][0], new_Snake[0][1] - 1])
                new_Snake.pop(-1)
                cost = self.manhattanDistance(new_Snake[0])
                snakeQueue.push(new_Snake,cost)
                newDirection = curDirection[:]
                newDirection.append(1)
                directionQueue.push(newDirection, cost)

                new_Snake = [snakePix[:] for snakePix in curSnake]
                new_Snake.insert(0, [new_Snake[0][0] - 1, new_Snake[0][1]])
                new_Snake.pop(-1)
                cost = self.manhattanDistance(new_Snake[0])
                snakeQueue.push(new_Snake,cost)
                newDirection = curDirection[:]
                newDirection.append(2)
                directionQueue.push(newDirection, cost)

                new_Snake = [snakePix[:] for snakePix in curSnake]
                new_Snake.insert(0, [new_Snake[0][0], new_Snake[0][1] + 1])
                new_Snake.pop(-1)
                cost = self.manhattanDistance(new_Snake[0])
                snakeQueue.push(new_Snake,cost)
                newDirection = curDirection[:]
                newDirection.append(3)
                directionQueue.push(newDirection, cost)
                
        return []

    def nextMove(self, direction):
        directionList = self.snakeBFS()
        # 1: up
        # 2: left
        # 3: down
        # 0: right
        if directionList == None or len(directionList) == 0:
            if self.is_collision_boundary([self.head[0]+1,self.head[1]]) and [self.head[0]+1,self.head[1]] not in self.snake and direction != 2:
                return [0]
            elif self.is_collision_boundary([self.head[0],self.head[1]-1]) and [self.head[0],self.head[1]-1] not in self.snake and direction != 3:
                return [1]
            elif self.is_collision_boundary([self.head[0]-1,self.head[1]]) and [self.head[0]-1,self.head[1]] not in self.snake and direction != 0:
                return [2]
            elif self.is_collision_boundary([self.head[0],self.head[1]+1]) and [self.head[0],self.head[1]+1] not in self.snake and direction != 1:
                return [3]
            else:
                return [0]
        return directionList

def play():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    game = SnakeGame()
    MAX = 100
    n = 0
    while n < MAX:
        directionList = []
        while not game.GameOver:
            game._update_ui()
            
            game.checkGameOver()
            game.clock.tick(SPEED)
            if len(directionList)==0:
                directionList = game.nextMove(game.direction)
            game.checkAndMove(directionList.pop(0))    
            if game.head == game.food:
                game.score += 1
                game._place_food()
            else:
                game.snake.pop(-1)
            

        
        n += 1
        if game.score > record:
            record = game.score
        print('Game', n, 'Score', game.score, 'Record:', record)
        plot_scores.append(game.score)
        total_score += game.score
        mean_score = total_score / n
        game.reset()
        plot_mean_scores.append(mean_score)
        plot(plot_scores, plot_mean_scores)
if __name__ == '__main__':
    play()

