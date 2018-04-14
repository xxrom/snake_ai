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

def head(x, y):
  gameDisplay.blit(headImg, (x, y))

x = (display_width * 0.45)
y = (display_height * 0.8)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

crashed = False
x_change = 0
while not crashed:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      crashed = True

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
  gameDisplay.fill(white)
  head(x, y)

  pygame.display.update()
  clock.tick(60)

pygame.quit()
quit()


