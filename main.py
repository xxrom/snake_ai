import pygame
import time

pygame.init()

WIDTH = 800
HEIGHT = 600

cellWidth = 20
cellHeight = 20

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pressedKeys = { 'left': 0, 'rigth': 0 }

headImg = pygame.image.load('car.png')

gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def head(x, y):
  gameDisplay.blit(headImg, (x, y))

def check(x):
  if (x > WIDTH or x < 0):
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
  # pygame.event.get()
  # pygame.display.update()

  # time.sleep(2)

  # game_loop()

def crash():
  messageDisplay('You Crashed!')


def game_loop():
  print('game loop')
  # time.sleep(1)
  x = (WIDTH * 0.1)
  y = (HEIGHT * 0.8)

  pressedKeys['left'] = 0
  pressedKeys['right'] = 0

  # pygame.display.set_caption('A bit Racey')

  gameExit = False
  x_change = 0

  while not gameExit:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

      keys = pygame.key.get_pressed()
      if event.type == pygame.KEYDOWN:
        if keys[pygame.K_LEFT]:
          pressedKeys['left'] = -5
        if keys[pygame.K_RIGHT]:
          pressedKeys['right'] = 5

      if event.type == pygame.KEYUP:
        print(event.key)
        if keys[pygame.K_LEFT] == 0:
          pressedKeys['left'] = 0
        if keys[pygame.K_RIGHT] == 0:
          pressedKeys['right'] = 0

      print(event)

    x += pressedKeys['left'] + pressedKeys['right']

    gameDisplay.fill(white)
    head(x, y)

    pygame.draw.rect(gameDisplay, black, (40, 40, 30, 30), 2)
    print(WIDTH / cellWidth)
    for i in range(0, WIDTH // cellWidth):
      for j in range(0, HEIGHT // cellHeight):
        print(i, ' ', j)
        pygame.draw.rect(gameDisplay, black,
          (i * cellWidth, j * cellHeight, cellWidth, cellHeight), 1)

    if check(x):
      crash()

    pygame.display.update()

    clock.tick(30)

game_loop()
pygame.quit()
quit()


