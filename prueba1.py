import pygame
from pygame import mixer
from fighter2 import Fighter

mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define fighter variables
WIZARD_SIZE = 162
WIZARD_SCALE = 4
WIZARD_OFFSET = [72, 56]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]
MARTIAL_HERO_2_SIZE = 250
MARTIAL_HERO_2_SCALE = 3
MARTIAL_HERO_2_OFFSET = [112, 107]
MARTIAL_HERO_2_DATA = [MARTIAL_HERO_2_SIZE, MARTIAL_HERO_2_SCALE, MARTIAL_HERO_2_OFFSET]

#load music and sounds
pygame.mixer.music.load("C:/Users/David/main.py/juego_pi/audio/music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("C:/Users/David/main.py/juego_pi/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("C:/Users/David/main.py/juego_pi/audio/magic.wav")
magic_fx.set_volume(0.75)

#load background image
bg_image = pygame.image.load("C:/Users/David/main.py/juego_pi/imagenes/entorno1/fondo.png").convert_alpha()

#load spritesheets
wizard_sheet = pygame.image.load("C:/Users/David/main.py/juego_pi/imagenes/Wizard Pack/Sprites/Wizard.png").convert_alpha()
martial_hero_2_sheet = pygame.image.load("C:/Users/David/main.py/juego_pi/imagenes/Martial Hero 2/Sprites/Martial Hero 2.png").convert_alpha()

#load victory image
victory_img = pygame.image.load("C:/Users/David/main.py/juego_pi/imagenes/iconos/victory.png").convert_alpha()

#define number of steps in each animation
WIZARD_ANIMATION_STEPS = [8, 8, 7, 2, 4, 6, 2, 8]
MARTIAL_HERO_2_ANIMATION_STEPS = [4, 4, 7, 2, 4, 2, 8, 3]

#define font
count_font = pygame.font.Font("C:/Users/David/main.py/juego_pi/Font/Starting Machine.ttf", 80)
score_font = pygame.font.Font("C:/Users/David/main.py/juego_pi/Font/Starting Machine.ttf", 30)

#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#function for drawing fighter health bars
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, RED, (x, y, 400, 30))
  pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

#create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, MARTIAL_HERO_2_DATA, martial_hero_2_sheet, MARTIAL_HERO_2_ANIMATION_STEPS, magic_fx)

#game loop
run = True
while run:

  clock.tick(FPS)

  #draw background
  draw_bg()

  #show player stats
  draw_health_bar(fighter_1.health, 20, 20)
  draw_health_bar(fighter_2.health, 580, 20)
  draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
  draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

  #update countdown
  if intro_count <= 0:
    #move fighters
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
  else:
    #display count timer
    draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    #update count timer
    if (pygame.time.get_ticks() - last_count_update) >= 1000:
      intro_count -= 1
      last_count_update = pygame.time.get_ticks()

  #update fighters
  fighter_1.update()
  fighter_2.update()

  #draw fighters
  fighter_1.draw(screen)
  fighter_2.draw(screen)

  #check for player defeat
  if round_over == False:
    if fighter_1.alive == False:
      score[1] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
    elif fighter_2.alive == False:
      score[0] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
  else:
    #display victory image
    screen.blit(victory_img, (360, 150))
    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
      round_over = False
      intro_count = 3
      fighter_1 = Fighter(1, 200, 310, False, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, sword_fx)
      fighter_2 = Fighter(2, 700, 310, True, MARTIAL_HERO_2_DATA, martial_hero_2_sheet, MARTIAL_HERO_2_ANIMATION_STEPS, magic_fx)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.update()

#exit pygame
pygame.quit()
