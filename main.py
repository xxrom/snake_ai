import pygame

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

headImg = pygame.image.load('car.png')

gameDisplay = pygame.display.set_mode((display_width, display_height))

def head(x, y):
  gameDisplay.blit(headImg, (x, y))

def check(x):
  if (x > display_width or x < 0):
    return True
  return False


def game_loop():
  x = (display_width * 0.45)
  y = (display_height * 0.8)

  pygame.display.set_caption('A bit Racey')
  clock = pygame.time.Clock()

  gameExit = False
  x_change = 0

  while not gameExit:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        gameExit = True

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          x_change = -5;
        if event.key == pygame.K_RIGHT:
          x_change = +5;

      if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
          x_change = 0;

      print(event)

    x += x_change

    gameExit = check(x) or gameExit

    gameDisplay.fill(white)
    head(x, y)

    pygame.display.update()
    clock.tick(60)

game_loop()
pygame.quit()
quit()


