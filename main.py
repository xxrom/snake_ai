import pygame
import time

pygame.init()

WIDTH = 800
HEIGHT = 600

IN_GAME_FPS = 1000 // 5;

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
  'y': 0
}

headImg = pygame.image.load('car.png')

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def head(x, y):
  pygame.draw.rect(gameDisplay, green, (x, y, cellWidth, cellHeight))
  # gameDisplay.blit(headImg, (x, y))

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
      pygame.draw.rect(gameDisplay, black,
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

  pressedKeys['left'] = 0
  pressedKeys['right'] = 0
  pressedKeys['up'] = 0
  pressedKeys['down'] = 0

  # pygame.display.set_caption('A bit Racey')

  gameExit = False
  x_change = 0

  startTime = millis()

  while not gameExit:
    events()

    if (millis() - startTime > IN_GAME_FPS):
      print('enter MOVE 500 =============================')
      startTime = millis()
      snake['x'] += pressedKeys['left'] + pressedKeys['right']
      snake['y'] += pressedKeys['up'] + pressedKeys['down']


    gameDisplay.fill(white)
    head(snake['x'], snake['y'])
    draw_field()

    if check(snake['x'], snake['y']):
      crash()

    pygame.display.update()
    clock.tick(60)

game_loop()
pygame.quit()
quit()


