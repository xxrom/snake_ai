import pygame
import time
import random
import math

# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import keras
# from keras.models import Sequential # init neural network
# from keras.layers import Dense # for layers creations

# Initialising the ANN
# classifier = Sequential()

pygame.init()

FPS = 10
IN_GAME_FPS = 1000 // FPS;

SNAKE_EAT_AREA = 0 # расстояние в клеточках за которое будет кушать змея

CELL_WIDTH = 20
CELL_HEIGHT = 20

WIDTH = CELL_WIDTH * 20
HEIGHT = CELL_HEIGHT * 20

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pressedKeys = {
  'left': 0,
  'rigth': 0,
  'up': 0,
  'down': 0
}

snake = {
  'x': 0,
  'y': 0,
  'length': 0,
  'tail': []
}

food = {
  'x': 0,
  'y': 0
}

# headImg = pygame.image.load('car.png')

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def init_food():
  print(random.random())
  food['x'] = math.floor(random.random() * (WIDTH / CELL_WIDTH)) * CELL_WIDTH
  food['y'] = math.floor(random.random() * (HEIGHT / CELL_HEIGHT)) * CELL_HEIGHT
  print(food)

def init_snake(snakeObj):
  snakeObj['x'] = (CELL_WIDTH * 1)
  snakeObj['y'] = (CELL_HEIGHT * 1)
  snakeObj['length'] = 0
  snakeObj['tail'] = []
  snakeObj['direction'] = 'down'

def draw_head(snake):
  pygame.draw.rect(gameDisplay, (0, 200, 10), (snake['x'], snake['y'], CELL_WIDTH, CELL_HEIGHT))

  if (snake['direction'] == 'down'):
    pygame.draw.circle(gameDisplay, (200, 0, 0), (snake['x'] + CELL_WIDTH // 2, snake['y'] + CELL_HEIGHT), CELL_HEIGHT // 5)
  if (snake['direction'] == 'right'):
    pygame.draw.circle(gameDisplay, (200, 0, 0), (snake['x'] + CELL_WIDTH, snake['y'] + CELL_HEIGHT // 2), CELL_HEIGHT // 5)
  if (snake['direction'] == 'up'):
    pygame.draw.circle(gameDisplay, (200, 0, 0), (snake['x'] + CELL_WIDTH // 2, snake['y']), CELL_HEIGHT // 5)
  if (snake['direction'] == 'left'):
    pygame.draw.circle(gameDisplay, (200, 0, 0), (snake['x'], snake['y'] + CELL_HEIGHT // 2), CELL_HEIGHT // 5)

  # pygame.draw.circle(gameDisplay, (0, 200, 0), (x + (CELL_WIDTH // 2), y + (CELL_HEIGHT // 2)), CELL_HEIGHT // 2)
  # gameDisplay.blit(headImg, (x, y))

def draw_tail(tail, length):
  for i in range(0, length):
    pygame.draw.rect(gameDisplay, (0, 255, 0), (tail[i]['x'], tail[i]['y'], CELL_WIDTH, CELL_HEIGHT))

def draw_food(x, y):
  pygame.draw.circle(gameDisplay, red, (x + (CELL_WIDTH // 2), y + (CELL_HEIGHT // 2)), 10)

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
  if checkCrash == False:
    eatArea = CELL_WIDTH * SNAKE_EAT_AREA
    if (abs(snake['x'] - food['x']) <= eatArea
      and abs(snake['y'] - food['y']) <= eatArea):
      print(snake['tail'])
      if (snake['length'] == 0):
        snake['tail'].append({ 'x': prev_x, 'y': prev_y })
      else:
        getTailPosition = snake['length'] - 1
        print('tail size', getTailPosition)
        print('add item', snake['tail'][getTailPosition])
        snake['tail'].append({
          'x': snake['tail'][getTailPosition]['x'],
          'y': snake['tail'][getTailPosition]['y']
        })
      snake['length'] += 1
      print(snake['tail'])
      init_food()

def draw_field():
  for i in range(0, WIDTH // CELL_WIDTH):
    for j in range(0, HEIGHT // CELL_HEIGHT):
      pygame.draw.rect(gameDisplay, (230,230,230),
        (i * CELL_WIDTH, j * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 1)

def millis():
    return int(round(time.time() * 1000))

def events():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()

    keys = pygame.key.get_pressed()
    if event.type == pygame.KEYDOWN:
      if keys[pygame.K_LEFT]:
        pressedKeys['left'] = -CELL_WIDTH
      if keys[pygame.K_RIGHT]:
        pressedKeys['right'] = CELL_WIDTH
      if keys[pygame.K_UP]:
        pressedKeys['up'] = -CELL_HEIGHT
      if keys[pygame.K_DOWN]:
        pressedKeys['down'] = CELL_HEIGHT

    if event.type == pygame.KEYUP:
      if keys[pygame.K_LEFT] == 0:
        pressedKeys['left'] = 0
      if keys[pygame.K_RIGHT] == 0:
        pressedKeys['right'] = 0
      if keys[pygame.K_UP] == 0:
        pressedKeys['up'] = 0
      if keys[pygame.K_DOWN] == 0:
        pressedKeys['down'] = 0

    print(event)

def crash_time_checking(checkCrash, startTime):
  if (millis() < startTime and checkCrash == True):
    crash()
    pygame.display.update()
    clock.tick(FPS)
    return True
  elif (millis() > startTime and checkCrash == True):
    game_loop()
    return False

def snake_moves():
  if (snake['direction'] == 'down'):
    if (pressedKeys['left'] != 0):
      snake['direction'] = 'right'
    if (pressedKeys['right'] != 0):
      snake['direction'] = 'left'

  elif (snake['direction'] == 'right'):
    if (pressedKeys['left'] != 0):
      snake['direction'] = 'up'
    if (pressedKeys['right'] != 0):
      snake['direction'] = 'down'

  elif (snake['direction'] == 'up'):
    if (pressedKeys['left'] != 0):
      snake['direction'] = 'left'
    if (pressedKeys['right'] != 0):
      snake['direction'] = 'right'

  elif (snake['direction'] == 'left'):
    if (pressedKeys['left'] != 0):
      snake['direction'] = 'down'
    if (pressedKeys['right'] != 0):
      snake['direction'] = 'up'

  if (snake['direction'] == 'down'):
    snake['y'] += CELL_HEIGHT
  if (snake['direction'] == 'up'):
    snake['y'] -= CELL_HEIGHT
  if (snake['direction'] == 'left'):
    snake['x'] -= CELL_WIDTH
  if (snake['direction'] == 'right'):
    snake['x'] += CELL_WIDTH

  # snake['x'] += pressedKeys['left'] + pressedKeys['right']
  # snake['y'] += pressedKeys['up'] + pressedKeys['down']

def draw_info(snake, food, distanceToFood, distanceToWall):
  distanceToFood = math.sqrt((snake['x'] - food['x'])**2 + (snake['y'] - food['y'])**2) // CELL_HEIGHT # расстояние в пикселях
  if (snake['direction'] == 'down'):
    distanceToWall = HEIGHT - snake['y'] - CELL_HEIGHT
  if (snake['direction'] == 'right'):
    distanceToWall = WIDTH - snake['x'] - CELL_WIDTH
  if (snake['direction'] == 'up'):
    distanceToWall = snake['y']
  if (snake['direction'] == 'left'):
    distanceToWall = snake['x']
  distanceToWall //= CELL_WIDTH
  messageDisplay('food ' + str(int(distanceToFood)), 20, 60, 20)
  messageDisplay('wall ' + str(int(distanceToWall)), 20, 60, 40)

# def init_ann():
#   # Initialising the ANN
#   classifier = Sequential()

#   # Adding the input layer and the first hidden layer
#   classifier.add(Dense(
#     6, # количество нейронов в скрытом слое/ не артист= (inputs + outpust)/2
#     input_dim = 11, # количество входов в нейронку (только в первом слое)
#     kernel_initializer = 'random_uniform', # инициализация весов начальная близи 0
#     activation = 'relu' # функция активации будет _/ , хорошо в скрытом слое
#   ))

#   # Adding the second hidden layer
#   classifier.add(Dense(
#     6, # количество нейронов в скрытом слое
#     kernel_initializer = 'random_uniform', # инициализация весов начальная близи 0
#     activation = 'relu' # функция активации будет _/ , хорошо в скрытом слое
#   ))

#   # Adding the output layer
#   classifier.add(Dense(
#     1, # количество котегорий на выходе (1 = 2, 3 = 3, n = n)
#     kernel_initializer = 'random_uniform', # инициализация весов начальная близи 0
#     activation = 'sigmoid' # функция активации будет сигмоида= получим % out
#     # если на выходе больше 2 категорий, то нужно выбрать softmax функцию
#   ))

#   # Compilint the ANN градиентный спуск применяем
#   classifier.compile(
#     optimizer = 'adam', # метод оптимизации
#     loss = 'binary_crossentropy', # cadecorical_crossentropy >2
#     metrics = ['accuracy'] # метод измерения качества модели
#   )

# def ann():


def game_loop():
  print('game loop')
  init_snake(snake)

  pressedKeys['left'] = 0
  pressedKeys['right'] = 0
  pressedKeys['up'] = 0
  pressedKeys['down'] = 0

  distanceToFood = 0
  distanceToWall = 0

  pygame.display.set_caption('SNAKE AI')

  gameExit = False
  checkCrash = False
  startTime = millis()
  init_food()

  while not gameExit:
    events()
    if (crash_time_checking(checkCrash, startTime) == True):
      continue

    prev_x = snake['x']
    prev_y = snake['y']

    snake_moves()

    # передвигаем весь хвост
    if (snake['x'] != prev_x or snake['y'] != prev_y):
      snake['tail'].insert(0, { 'x': prev_x, 'y': prev_y })
      snake['tail'].pop()

    checkCrash = check(snake['x'], snake['y'])
    check_crash(checkCrash, prev_x, prev_y)

    gameDisplay.fill(white)
    draw_field()
    draw_tail(snake['tail'], snake['length'])
    draw_food(food['x'], food['y'])
    draw_head(snake)

    draw_info(snake, food, distanceToFood, distanceToWall)

    if checkCrash == True:
      startTime = millis() + 1000 # 1 сек отображаем надпись врезались и перезпускам все

    print('distance to the food', distanceToFood)
    print('distance to the wall', distanceToWall)
    pygame.display.update()
    clock.tick(FPS)

game_loop()
pygame.quit()
quit()


