import pygame
import time
import random
import math

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 20
IN_GAME_FPS = 1000 // FPS;

cellWidth = 20
cellHeight = 20

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

headImg = pygame.image.load('car.png')

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def init_food():
  print(random.random())
  food['x'] = math.floor(random.random() * (WIDTH / cellWidth)) * cellWidth
  food['y'] = math.floor(random.random() * (HEIGHT / cellHeight)) * cellHeight
  print(food)

def draw_head(x, y):
  pygame.draw.rect(gameDisplay, (0, 200, 10), (x, y, cellWidth, cellHeight))
  # pygame.draw.circle(gameDisplay, (0, 200, 0), (x + (cellWidth // 2), y + (cellHeight // 2)), cellHeight // 2)
  # gameDisplay.blit(headImg, (x, y))

def draw_tail(tail):
  for i in tail:
    pygame.draw.rect(gameDisplay, (0, 255, 0), (i['x'], i['y'], cellWidth, cellHeight))

def draw_food(x, y):
  pygame.draw.circle(gameDisplay, red, (x + (cellWidth // 2), y + (cellHeight // 2)), 10)


def check(x, y):
  if (
    x > WIDTH - cellWidth
    or x < 0
    or y < 0
    or y > HEIGHT - cellHeight
  ):
    return True
  return False

def textObjects(text, font, color):
  textSurface = font.render(text, True, color)
  return textSurface, textSurface.get_rect()

def messageDisplay(text):
  largeText = pygame.font.Font('freesansbold.ttf', 115)
  TextSurf, TextRect = textObjects(text, largeText, black)
  TextRect.center = ((WIDTH / 2), (HEIGHT / 2))
  gameDisplay.blit(TextSurf, TextRect)

def crash():
  messageDisplay('You Crashed!')

def draw_field():
  for i in range(0, WIDTH // cellWidth):
    for j in range(0, HEIGHT // cellHeight):
      pygame.draw.rect(gameDisplay, (230,230,230),
        (i * cellWidth, j * cellHeight, cellWidth, cellHeight), 1)

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
        pressedKeys['left'] = -cellWidth
      if keys[pygame.K_RIGHT]:
        pressedKeys['right'] = cellWidth
      if keys[pygame.K_UP]:
        pressedKeys['up'] = -cellHeight
      if keys[pygame.K_DOWN]:
        pressedKeys['down'] = cellHeight

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

def game_loop():
  print('game loop')
  # time.sleep(1)
  snake['x'] = (cellWidth * 5)
  snake['y'] = (cellHeight * 5)
  snake['length'] = 0

  pressedKeys['left'] = 0
  pressedKeys['right'] = 0
  pressedKeys['up'] = 0
  pressedKeys['down'] = 0

  pygame.display.set_caption('SNAKE AI')

  gameExit = False
  startTime = millis()
  init_food()

  while not gameExit:
    events()

    if (millis() - startTime > IN_GAME_FPS):
      # print('enter MOVE 500 =============================')
      startTime = millis()

      prev_x = snake['x']
      prev_y = snake['y']
      snake['x'] += pressedKeys['left'] + pressedKeys['right']
      snake['y'] += pressedKeys['up'] + pressedKeys['down']

      # передвигаем весь хвост
      if (snake['x'] != prev_x or snake['y'] != prev_y):
        snake['tail'].insert(0, { 'x': prev_x, 'y': prev_y })
        snake['tail'].pop()

      if check(snake['x'], snake['y']):
        crash()
      else:
        eatArea = cellWidth * 3
        if (abs(snake['x'] - food['x']) <= eatArea
          and abs(snake['y'] - food['y']) <= eatArea):
          print(snake['tail'])
          if (snake['length'] == 0):
            snake['tail'].append({ 'x': prev_x, 'y': prev_y })
          else:
            getTailPosition = len(snake['tail']) - 1
            print('tail size', getTailPosition)
            print('add item', snake['tail'][getTailPosition])
            snake['tail'].append({
              'x': snake['tail'][getTailPosition]['x'],
              'y': snake['tail'][getTailPosition]['y']
            })
          snake['length'] += 1
          print(snake['tail'])
          init_food()



    gameDisplay.fill(white)
    draw_field()
    draw_tail(snake['tail'])
    draw_food(food['x'], food['y'])
    draw_head(snake['x'], snake['y'])

    pygame.display.update()
    clock.tick(FPS)

game_loop()
pygame.quit()
quit()


