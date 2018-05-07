import pygame
import time
import random
import math

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import keras
from keras.models import Sequential # init neural network
from keras.layers import Dense # for layers creations

class Snake:
  def __init__(self, x, y):
    self.x = x * CELL_WIDTH
    self.y = y * CELL_HEIGHT
    self.length = 0
    self.tail = []
    self.direction = 'down'

  def respawn(self):
    self.x = 2 * CELL_WIDTH
    self.y = 2 * CELL_HEIGHT
    self.length = 0
    self.direction = 'down'

  def __getitem__(self, item):
    return getattr(self, item)

  def moves(self, pressedKeys):
    # print('MOVESSSS left ',  pressedKeys['left'], ' right ', pressedKeys['right'])
    if (self.direction == 'down'):
      if (pressedKeys['left'] != 0):
        self.direction = 'right'
      if (pressedKeys['right'] != 0):
        self.direction = 'left'

    elif (self.direction == 'right'):
      if (pressedKeys['left'] != 0):
        self.direction = 'up'
      if (pressedKeys['right'] != 0):
        self.direction = 'down'

    elif (self.direction == 'up'):
      if (pressedKeys['left'] != 0):
        self.direction = 'left'
      if (pressedKeys['right'] != 0):
        self.direction = 'right'

    elif (self.direction == 'left'):
      if (pressedKeys['left'] != 0):
        self.direction = 'down'
      if (pressedKeys['right'] != 0):
        self.direction = 'up'

    if (self.direction == 'down'):
      self.y += CELL_HEIGHT
    if (self.direction == 'up'):
      self.y -= CELL_HEIGHT
    if (self.direction == 'left'):
      self.x -= CELL_WIDTH
    if (self.direction == 'right'):
      self.x += CELL_WIDTH

    # snake.x += pressedKeys['left'] + pressedKeys['right']
    # snake.y += pressedKeys['up'] + pressedKeys['down']

  def draw_head(self):
    pygame.draw.rect(gameDisplay, (0, 200, 10), (self.x, self.y, CELL_WIDTH, CELL_HEIGHT))

    if (self.direction == 'down'):
      pygame.draw.circle(gameDisplay, (200, 0, 0), (self.x + CELL_WIDTH // 2, self.y + CELL_HEIGHT), CELL_HEIGHT // 5)
    if (self.direction == 'right'):
      pygame.draw.circle(gameDisplay, (200, 0, 0), (self.x + CELL_WIDTH, self.y + CELL_HEIGHT // 2), CELL_HEIGHT // 5)
    if (self.direction == 'up'):
      pygame.draw.circle(gameDisplay, (200, 0, 0), (self.x + CELL_WIDTH // 2, self.y), CELL_HEIGHT // 5)
    if (self.direction == 'left'):
      pygame.draw.circle(gameDisplay, (200, 0, 0), (self.x, self.y + CELL_HEIGHT // 2), CELL_HEIGHT // 5)

    # pygame.draw.circle(gameDisplay, (0, 200, 0), (x + (CELL_WIDTH // 2), y + (CELL_HEIGHT // 2)), CELL_HEIGHT // 2)
    # gameDisplay.blit(headImg, (x, y))

  def draw_tail(self):
    for i in range(0, self.length):
      pygame.draw.rect(
        gameDisplay,
        (0, 255, 0),
        (self.tail[i]['x'],
        self.tail[i]['y'],
        CELL_WIDTH,
        CELL_HEIGHT)
      )

class Game:
  def __init__(self, width, height, cellWidth, cellHeight, FPS):
    self.width = width
    self.height = height
    self.cellWidth = cellWidth
    self.cellHeight = cellHeight
    self.food = { 'x': 0, 'y': 0 }
    self.pressedKeys = {
      'left': 0,
      'right': 0,
      'up': 0,
      'down': 0
    }
    self.FPS = FPS

    pygame.display.set_caption('SNAKE AI')

  def events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

      keys = pygame.key.get_pressed()
      if event.type == pygame.KEYDOWN:
        if keys[pygame.K_LEFT]:
          self.pressedKeys['left'] = -CELL_WIDTH
        if keys[pygame.K_RIGHT]:
          self.pressedKeys['right'] = CELL_WIDTH
        if keys[pygame.K_i]:
          # self.pressedKeys['up'] = -CELL_HEIGHT
          self.FPS += 2
        if keys[pygame.K_k]:
          # self.pressedKeys['down'] = CELL_HEIGHT
          self.FPS -= 2

      if event.type == pygame.KEYUP:
        if keys[pygame.K_LEFT] == 0:
          self.pressedKeys['left'] = 0
        if keys[pygame.K_RIGHT] == 0:
          self.pressedKeys['right'] = 0
        # if keys[pygame.K_UP] == 0:
          # pressedKeys['up'] = 0
        # if keys[pygame.K_DOWN] == 0:
          # pressedKeys['down'] = 0

      # print(event)

  def __getitem__(self, item):
    return getattr(self, item)

  def add_snake(self, snake):
    self.snake = snake
  def add_food(self, food):
    self.food = food

  def init_food(self):
    self.food['x'] = math.floor(random.random() * (self.width / self.cellWidth)) * self.cellWidth
    self.food['y'] = math.floor(random.random() * (self.height / self.cellHeight)) * self.cellHeight
    self.distanceToFood = 0
    self.distanceToWall = 0

  def draw_food(self):
    pygame.draw.circle(gameDisplay, red, (self.food['x'] + (self.cellWidth // 2), self.food['y'] + (self.cellHeight // 2)), self.cellHeight // 2)

  def draw_info(self):
    self.distanceToFoodAhead = calculate_distance(self.snake, self.food) # // CELL_HEIGHT # расстояние в пикселях
    distanceDown = HEIGHT - snake.y - CELL_HEIGHT
    distanceRight = WIDTH - snake.x - CELL_WIDTH
    distanceLeft = snake.x
    distanceUp = snake.y

    if snake.y < food.y:
      foodDown = 1
    elif snake.y > food.y:
      foodDown = 0
    else:
      foodDown = 2

    if snake.x < food.x:
      foodRight = 1
    elif snake.x > food.x:
      foodRight = 0
    else:
      foodRight = 2

    self.haveFoodAhead = 0
    self.haveFoodLeft = 0
    self.haveFoodRight = 0

    if (self.snake.direction == 'down'):
      self.wallAhead = distanceDown
      self.wallLeft = distanceRight
      self.wallRight = distanceLeft
      self.foodDirection = 'left'
      if snake.x == food.x and foodDown == 1:
        self.haveFoodAhead = 1
      if snake.y == food.y:
        if foodRight == 1:
          self.haveFoodLeft = 1
        else:
          self.haveFoodRight = 1

    if (self.snake.direction == 'right'):
      self.wallAhead = distanceRight
      self.wallLeft = distanceUp
      self.wallRight = distanceDown

      if snake.y == food.y and foodRight == 0:
        self.haveFoodAhead = 1
      if snake.x == food.x:
        if foodDown == 1:
          self.haveFoodRight = 1
        else:
          self.haveFoodLeft = 1

    if (self.snake.direction == 'up'):
      self.wallAhead = distanceUp
      self.wallLeft = distanceLeft
      self.wallRight = distanceRight

      if snake.x == food.x and foodDown == 0:
        self.haveFoodAhead = 1
      if snake.y == food.y:
        if foodRight == 0:
          self.haveFoodLeft = 1
        else:
          self.haveFoodRight = 1

    if (self.snake.direction == 'left'):
      self.wallAhead = distanceLeft
      self.wallLeft = distanceDown
      self.wallRight = distanceUp

      if snake.y == food.y and foodRight == 1:
        self.haveFoodAhead = 1
      if snake.x == food.x:
        if foodDown == 0:
          self.haveFoodRight = 1
        else:
          self.haveFoodLeft = 1
    # distanceToFoodAhead //= CELL_WIDTH

    messageDisplay('fps ' + str(int(self.FPS)), 20, 60, 20)
    messageDisplay('food ' + str(int(self.distanceToFood)), 20, 60, 40)
    messageDisplay('ahead ' + str(int(self.distanceToFoodAhead)) + ' ' + self.haveFoodAhead, 20, 80, 60)
    messageDisplay('left ' + str(int(self.distanceToFoodLeft)) + ' ' + self.haveFoodLeft, 20, 80, 80)
    messageDisplay('right ' + str(int(self.distanceToFoodRight)) + ' ' + self.haveFoodRight, 20, 80, 100)


    return self.distanceToFood, self.distanceToWall

FPS = 8
IN_GAME_FPS = 1000 // FPS;

SNAKE_EAT_AREA = 0 # расстояние в клеточках за которое будет кушать змея

CELL_WIDTH = 20
CELL_HEIGHT = 20

WIDTH = CELL_WIDTH * 30
HEIGHT = CELL_HEIGHT * 30

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Initializing the ANN
classifier = Sequential()

pygame.init()
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))

snake = Snake(1, 1)
game = Game(WIDTH, HEIGHT, CELL_WIDTH, CELL_HEIGHT, FPS)
game.add_snake(snake)

clock = pygame.time.Clock()

def check(x, y):
  if (
    x > WIDTH - CELL_WIDTH
    or x < 0
    or y < 0
    or y > HEIGHT - CELL_HEIGHT
  ):
    return True
  return False # вышли за границу поля

def textObjects(text, font, color):
  textSurface = font.render(text, True, color)
  return textSurface, textSurface.get_rect()

def messageDisplay(text, textSize = 80, x = (WIDTH / 2), y = (HEIGHT / 2)):
  largeText = pygame.font.Font('freesansbold.ttf', textSize)
  TextSurf, TextRect = textObjects(text, largeText, black)
  TextRect.center = (x, y)
  gameDisplay.blit(TextSurf, TextRect)

def crash():
  print('You Crashed!')
  messageDisplay('You Crashed!', 50)

def check_crash(checkCrash, prev_x, prev_y):
  global game
  if checkCrash == False:
    eatArea = game.cellWidth * SNAKE_EAT_AREA
    if (abs(snake.x - game.food['x']) <= eatArea
      and abs(snake.y - game.food['y']) <= eatArea):
      # print(snake.tail)
      if (snake.length == 0):
        snake.tail.append({ 'x': prev_x, 'y': prev_y })
      else:
        getTailPosition = snake.length - 1
        # print('tail size', getTailPosition)
        # print('add item', snake.tail[getTailPosition])
        snake.tail.append({
          'x': snake.tail[getTailPosition]['x'],
          'y': snake.tail[getTailPosition]['y']
        })
      snake.length += 1
      # print(snake.tail)
      game.init_food()

def draw_field():
  for i in range(0, WIDTH // CELL_WIDTH):
    for j in range(0, HEIGHT // CELL_HEIGHT):
      pygame.draw.rect(gameDisplay, (230,230,230),
        (i * CELL_WIDTH, j * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 1)

def millisec():
  return int(round(time.time() * 1000))

def crash_time_checking(checkCrash, startTime):
  if (millisec() < startTime and checkCrash == True):
    crash()
    pygame.display.update()
    clock.tick(FPS)
    return True
  elif (millisec() > startTime and checkCrash == True):
    game_loop()
    return False

def calculate_distance(a, b):
  return math.sqrt((a['x'] - b['x'])**2 + (a['y'] - b['y'])**2)

def init_ann():
  global classifier
  # Initialising the ANN
  classifier = Sequential()

  # Adding the input layer and the first hidden layer
  classifier.add(Dense(
    5, # количество нейронов в скрытом слое/ не артист= (inputs + outpust)/2
    input_dim = 5, # количество входов в нейронку (только в первом слое)
    kernel_initializer = 'random_uniform', # инициализация весов начальная близи 0
    activation = 'relu' # функция активации будет _/ , хорошо в скрытом слое
  ))

  # Adding the second hidden layer
  classifier.add(Dense(
    3, # количество нейронов в скрытом слое
    kernel_initializer = 'random_uniform', # инициализация весов начальная близи 0
    activation = 'relu' # функция активации будет _/ , хорошо в скрытом слое
  ))

  # Adding the output layer
  classifier.add(Dense(
    3, # количество котегорий на выходе (1 = 2, 3 = 3, n = n)
    kernel_initializer = 'random_uniform', # инициализация весов начальная близи 0
    activation = 'softmax' # функция активации будет сигмоида= получим % out
    # если на выходе больше 2 категорий, то нужно выбрать softmax функцию
  ))

  # Compilint the ANN градиентный спуск применяем
  adam = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-8)
  classifier.compile(
    optimizer = adam, # метод оптимизации
    loss = 'categorical_crossentropy', # cadecorical_crossentropy >2
    metrics = ['accuracy'] # метод измерения качества модели
  )

  X_pred = [ # down, right, up, left, old - new => distance to food
    # [1, 0, 0, 0, 19], [ 1, 0, 0, 0, -19],
    [1, 0, 0, 0, 8], [ 1, 0, 0, 0, -8],
    # [1, 0, 0, 0, 1], [ 1, 0, 0, 0, -1],

    # [0, 1, 0, 0, 19], [ 0, 1, 0, 0,  -19],
    [0, 1, 0, 0, 8], [ 0, 1, 0, 0,  -8],
    # [0, 1, 0, 0, 1], [ 0, 1, 0, 0,  -1],

    # [0, 0, 1, 0, 19], [ 0, 0, 1, 0, -19],
    [0, 0, 1, 0, 8], [ 0, 0, 1, 0, -8],
    # [0, 0, 1, 0, 1], [ 0, 0, 1, 0, -1],

    # [0, 0, 0, 1, 19], [ 0, 0, 0, 1,  -19],
    [0, 0, 0, 1, 8], [ 0, 0, 0, 1,  -8],
    # [0, 0, 0, 1, 1], [ 0, 0, 0, 1, -1],
  ]

  y_test = [ # left right ahead
    # [0, 0, 1], [1, 0, 0],
    [0, 0, 1], [1, 0, 0],
    # [0, 0, 1], [1, 0, 0],

    # [0, 0, 1], [1, 0, 0],
    [0, 0, 1], [1, 0, 0],
    # [0, 0, 1], [1, 0, 0],

    # [0, 0, 1], [1, 0, 0],
    [0, 0, 1], [1, 0, 0],
    # [0, 0, 1], [0, 1, 0],

    # [0, 0, 1], [0, 1, 0],
    [0, 0, 1], [1, 0, 0],
    # [0, 0, 1], [1, 0, 0],
  ]

  classifier.fit(np.array(X_pred), np.array(y_test),
    batch_size = 1, # после скольких будет коррекция весов
    nb_epoch = 50 # 1000 количество эпох
  )

def ann(X_train, y_train, X_pred):
  # Fitting the ANN to the Training set
  classifier.fit(X_train, y_train,
    batch_size = 1, # после скольких будет коррекция весов
    nb_epoch = 1 # количество эпох
  )
  y_pred = classifier.predict(X_pred)
  y_pred = (y_pred > 0.5) # if (x > 0.5) true else false
  print(y_pred)

def game_loop():
  gameExit = False
  checkCrash = False
  startTime = millisec()
  game.init_food()
  snake.respawn()

  while not gameExit:
    global distanceToFood, distanceToWall

    game.events()
    if (crash_time_checking(checkCrash, startTime) == True):
      continue

    prev_x = snake.x
    prev_y = snake.y

    snake.moves(game.pressedKeys)

    # передвигаем весь хвост
    if (snake.x != prev_x or snake.y != prev_y):
      snake.tail.insert(0, { 'x': prev_x, 'y': prev_y })
      snake.tail.pop()

    checkCrash = check(snake.x, snake.y)
    check_crash(checkCrash, prev_x, prev_y)

    gameDisplay.fill(white)
    draw_field()
    snake.draw_tail()
    game.draw_food()
    snake.draw_head()

    oldDistanceToFood = game.distanceToFood
    distanceToFood, distanceToWall = game.draw_info()
    print(oldDistanceToFood - distanceToFood)
    X_pred = [
      int(snake.direction == 'down'),
      int(snake.direction == 'right'),
      int(snake.direction == 'up'),
      int(snake.direction == 'left'),
      int(oldDistanceToFood - distanceToFood)
    ]
    # print('X_pred', X_pred)
    # y_pred = classifier.predict(np.array([X_pred]))
    # print(y_pred)
    # game.pressedKeys['left'] = int(y_pred[0][0] > 0.5)
    # game.pressedKeys['right'] = int(y_pred[0][1] > 0.5)

    if checkCrash == True:
      startTime = millisec() + 1000 # 1 сек отображаем надпись врезались и перезапускаем все

    pygame.display.update()
    clock.tick(game.FPS)

# ANN
# init_ann()
game_loop()
pygame.quit()
quit()


