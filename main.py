import pygame
import random
pygame.init()
clock = pygame.time.Clock()
FPS = 60
size = [1000, 1000]
black = (0, 0, 0)
dblue = (3, 30, 175)
blue = (52, 186, 235)
red = (252, 3, 3)
green = (46, 176, 39)
yellow = (252, 227, 3)
purple = (143, 50, 168)
white = (255, 255, 255)
points = 0
level = 1
deathCounter = 0
left = pygame.K_a
right = pygame.K_d
up = pygame.K_w
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
allSprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
invisibles = pygame.sprite.Group()
coins = pygame.sprite.Group()
spikes = pygame.sprite.Group()
font = pygame.font.SysFont("monospace", 100)
victoryText = font.render("You Win! Play again.", True, white)

class player(pygame.sprite.Sprite):
  def __init__(self, screen, x, y, width, height):
    super().__init__(allSprites)
    global level
    self.screen = screen
    self.x = x
    self.y = y
    self.homePos = (x, y)
    self.width = width
    self.height = height
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    self.pos = pygame.Vector2(x, y)
    self.vel = pygame.Vector2(0,0)
    self.acc = pygame.Vector2(0, 0)
    self.hit = False
    self.alive = True
    self.atCheck = False
  def move(self):
    self.acc.x = 0
    self.vel.x = 0
    keys = pygame.key.get_pressed()
    if keys[right]:
      self.acc.x += 1
    if keys[left]:
      self.acc.x += -1
    if keys[up] and self.hit:
      self.vel.y += -50
    self.acc.x += self.vel.x * .25
    self.vel += self.acc
    self.pos.x += self.vel.x + 0.5 * self.acc.x
    self.pos.y += self.vel.y * .1 * self.acc.y
    self.rect.midbottom = self.pos
    #print(self.acc.y)
    #print(self.acc.x)
  def collisions(self):
    global level
    self.acc.y = 1
    #print(self.rect.top)
    for platform in platforms:
      if self.acc.y > 0:
        if pygame.Rect.colliderect(self.rect, platform.hitbox):
          self.hit = True
          self.acc.y = 0
          self.vel.y = 0
          if platform.isCheck:
            if level == 2:
              self.homePos = (50, 400)
              self.atCheck = True
            if level == 3:
              self.homePos = (50, 775)
              self.atCheck = True
          if self.rect.top == platform.rect.bottom:
            self.acc.y = 0
            self.vel.y = 0
            self.pos.y = platform.rect.bottom
          #if not platform.rect.bottom < self.rect.top:
            #self.acc.y = 1
          else:
            self.pos.y = platform.rect.top
          #check if platform is a disappearing platform
          if platform.disappears and platform.timeToDie == -1:
            platform.timeToDie = pygame.time.get_ticks() / 1000
        else:
          self.hit = False
  def displayPoints(self):
    fontType = pygame.font.get_default_font()
    font = pygame.font.Font(fontType, 25)
    text = font.render("Points: " + str(points), True, yellow)
    textRect = text.get_rect()
    textRect.center = (75, 15)
    screen.blit(text, textRect)
  def displayDeaths(self):
    fontType = pygame.font.get_default_font()
    font = pygame.font.Font(fontType, 25)
    text = font.render("Deaths: " + str(deathCounter), True, yellow)
    textRect = text.get_rect()
    textRect.center = (75, 75)
    screen.blit(text, textRect)
  def update(self):
    global level
    global points
    global deathCounter
    #self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    if level == 2 and not self.atCheck:
      self.homePos = (50,925)
    if level == 3 and not self.atCheck:
      self.homePos = (50, 175)
    if self.pos.y >= 1000:
      self.pos.x, self.pos.y = self.homePos
      deathCounter += 1
    #print(self.y)
    self.displayDeaths()
    self.displayPoints()
    self.move()
    self.collisions()
    #print(self.pos)
    if pygame.Rect.colliderect(self.rect, p.hitbox):
      if level == 1 and points >= 2:
        level += 1
        points = 0
        self.pos.x, self.pos.y = 50, 925
      if level == 2 and points >= 4:
        level += 1
        points = 0
        self.atCheck = False
        self.pos.x, self.pos.y = 50, 175
      if level == 3 and points >= 10:
        level = "win"
        points = 0
    self.rect.midbottom = self.pos
    for spike in spikes:
      if pygame.Rect.colliderect(self.rect, spike.hitbox):
        self.pos.x, self.pos.y = self.homePos
        deathCounter += 1
    pygame.draw.rect(self.screen, dblue, self.rect, 0)
Player = player(screen, 50, 800, 25, 25)
#50, 800 is level 1
#50, 175 is level 3

class spike(pygame.sprite.Sprite):
  def __init__(self, screen, x, y, level, width, height):
    super().__init__(allSprites)
    super().__init__(spikes) 
    self.screen = screen
    self.x = x
    self.y = y
    self.width = width 
    self.height = height
    self.level = level
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
  def update(self):
    global level
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    if self.level == level:
      spikes.add(self)
      pygame.draw.rect(self.screen, red, self.rect, 0)
    else:
      spikes.remove(self)
s = spike(screen, 475, 790, 1, 10, 10)
s2 = spike(screen,575, 540, 1, 10, 10)
s3 = spike(screen,675, 290, 1, 10, 10)
s3 = spike(screen,775, 290, 1, 10, 10)
s5 = spike(screen, 875, 290, 1, 10, 10)
s6 = spike(screen, 525, 560, 2, 10, 10)
s7 = spike(screen, 600, 560, 2, 10, 10)
s8 = spike(screen, 675, 560, 2, 10, 10)
s9 = spike(screen, 750, 560, 2, 10, 10)
s10 = spike(screen, 300, 310, 2,100, 10 )
s11 = spike(screen, 475, 310, 2,100, 10 )
s10 = spike(screen, 650, 310, 2,100, 10 )
s10 = spike(screen, 825, 310, 2,10, 10 )
s11 = spike(screen, 0, 400, 3, 800 , 10 )
class next_level(pygame.sprite.Sprite):
  def __init__(self, screen, x, y):
    super().__init__(allSprites)
    #super().__init__(next_level)
    self.screen = screen
    self.x = x
    self.y = y
    self.width = 15
    self.height = 60
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
  def displayLevel(self):
    global level
    fontType = pygame.font.get_default_font()
    font = pygame.font.Font(fontType, 25)
    text = font.render("Level: " + str(level), True, red)
    textRect = text.get_rect()
    textRect.center = (75, 45)
    screen.blit(text, textRect)
  def update(self):
    global level
    self.displayLevel()
    if level == 2:
      self.x = 900
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    pygame.draw.rect(self.screen, black, self.rect, 0)

p = next_level(screen, 935,275)
    
class coin(pygame.sprite.Sprite):
  def __init__(self, screen, x, y, level):
    super().__init__(allSprites)
    super().__init__(coins)
    self.screen = screen
    self.x = x
    self.y = y
    self.level = level
    self.width = 25
    self.height = 25
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    self.received = False
  def update(self):
    global points
    global level
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    if pygame.Rect.colliderect(self.hitbox, Player.rect) and not self.received and self.level == level:
      self.kill()
      self.received = True
      points += 1
    elif not self.received:
      if self.level == level:
        coins.add(self)
        pygame.draw.rect(self.screen, yellow, self.rect, 0) 
      else:
        coins.remove(self)
    
    
  
c = coin(screen,500, 775, 1)
c2 = coin(screen,50,575, 1)
c3 = coin(screen,450,595, 2)
c4 = coin(screen,350,300, 2)
c5 = coin(screen,525,300, 2)
c6 = coin(screen,700,300, 2)
c7 = coin(screen,0, 375, 3)
c8 = coin(screen,200, 375, 3)
c9 = coin(screen,400, 375, 3)
c10 = coin(screen,600, 375, 3)
c11 = coin(screen,750, 375, 3)
c12 = coin(screen, 150, 410, 3)
c13 = coin(screen,350, 410, 3)
c14 = coin(screen,550, 410, 3)
c15 = coin(screen,700, 410, 3)
c16 = coin(screen,750, 410, 3)
class platform(pygame.sprite.Sprite):
  def __init__(self, screen, x, y, width, height, disappears, isCheck, level):
    super().__init__(allSprites)
    super().__init__(platforms)
    self.screen = screen
    self.x = x
    self.y = y
    self.level = level
    self.width = width
    self.height = height
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    self.hitbox = pygame.Rect(self.x, self.y, self.width+5, self.height + 5)
    self.disappears = disappears
    self.isCheck = isCheck
    self.timeToDie = -1
    self.timeToDisappear = 0
  def update(self):
    global level
    currTime = pygame.time.get_ticks() / 1000
    alive = True
    if level == 1:
      self.timeToDisappear = 0.75
    if level == 2:
      self.timeToDisappear = 0.25
    if self.timeToDie > 0:
      if 4 > currTime - self.timeToDie > self.timeToDisappear:
        alive = False
        invisibles.add(self)
        platforms.remove(self)
      elif currTime - self.timeToDie > 4:
        alive = True
        invisibles.remove(self)
        platforms.add(self)
        self.timeToDie = -1
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    if alive:
      if self.level == level:
        platforms.add(self)
        if self.isCheck:
          pygame.draw.rect(self.screen, purple, self.rect, 0)
        else:
          pygame.draw.rect(self.screen, green, self.rect, 0)
      else:
        platforms.remove(self)

    self.rect = self.screen.get_rect(top=(self.y))
    #self.rect = self.screen.get_rect(bottom=(self.y))
    
plat = platform(screen, 50, 900, 75, 50, False, False, 1)
plat2 = platform(screen, 250, 850, 75, 50, True, False, 1)
plat3 = platform(screen, 450, 800, 75, 50, False, False, 1)
plat4 = platform(screen, 650, 750, 75, 50, True, False, 1)
plat5 = platform(screen, 850, 700, 75, 50, False, False, 1)
plat6 = platform(screen, 750, 600, 75, 50, True, False, 1)
plat7 = platform(screen, 550, 550, 75, 50, False, False, 1)
plat8 = platform(screen, 350, 500, 75, 50, False, False, 1)
plat9 = platform(screen, 150, 450, 75, 50, False, False, 1)
plat10 = platform(screen, 250, 350, 75, 50, True, False, 1)
plat11 = platform(screen, 450, 300, 75, 50, False, False, 1)
plat12 = platform(screen, 50, 600, 75, 50, True, False, 1)
plat13 = platform(screen, 650, 300, 300, 50, False, False, 1)
plat14 = platform(screen, 50, 950, 50, 50, False, False, 2)
plat15 = platform(screen, 150, 850, 50, 50, True, False, 2)
plat16 = platform(screen, 250, 750, 50, 50, True, False, 2)
plat17 = platform(screen, 350, 875, 50, 50, True, False, 2)
plat18 = platform(screen, 475, 950, 50, 50, True, False, 2)
plat19 = platform(screen, 550, 875, 50, 50, True, False, 2)
plat20 = platform(screen, 650, 800, 50, 50, True, False, 2)
plat21 = platform(screen, 750, 750, 10, 10, True, False, 2)
plat22 = platform(screen, 850, 750, 10, 10, True, False, 2)
plat23 = platform(screen, 950, 700, 10, 10, True, False, 2)
plat24 = platform(screen, 500, 570, 350,10, False, False, 2)
plat25 = platform(screen, 300, 520, 50, 50, False, False, 2)
plat26 = platform(screen, 100, 470, 50, 50, True, False, 2)
plat27 = platform(screen, 250, 320, 650,10, False, False, 2)
plat28 = platform(screen, 50, 360, 50, 50, False, True, 2)
plat29 = platform(screen, 50, 200, 50, 50, False, False, 3)
plat30 = platform(screen, 200, 225, 50, 50, True, False, 3)
plat31 = platform(screen, 350, 250, 50, 50, True, False, 3)
plat32 = platform(screen, 500, 275, 50, 50, True, False, 3)
plat33 = platform(screen, 650, 300, 50, 50, True, False, 3)
plat34 = platform(screen, 800, 325, 50, 50, True, False, 3)
plat35 = platform(screen, 900, 350, 50, 50, True, False, 3)
plat36 = platform(screen, 900, 450, 50, 50, True, False, 3)
plat37 = platform(screen, 800, 500, 50, 50, True, False, 3)
plat38 = platform(screen, 700, 575, 50, 50, True, False, 3)
plat39 = platform(screen, 550, 575, 50, 50, True, False, 3)
plat40 = platform(screen, 400, 575, 50, 50, True, False, 3)
plat41 = platform(screen, 250, 575, 50, 50, True, False, 3)
plat42 = platform(screen, 150, 575, 50, 50, True, False, 3)
plat43 = platform(screen, 50, 800, 50, 50, False, True, 3)
plat44 = platform(screen, 225, 900, 10, 10, True, False, 3)
plat45 = platform(screen, 375, 950, 10, 10, True, False, 3)
plat46 = platform(screen, 525, 950, 10, 10, True, False, 3)
plat47 = platform(screen, 675, 950, 10, 10, True, False, 3)
plat48 = platform(screen, 825, 950, 10, 10, True, False, 3)
plat49 = platform(screen, 975, 950, 10, 10, True, False, 3)
plat50 = platform(screen, 1125, 950, 10, 10, True, False, 3)
plat51 = platform(screen, 1125, 850, 10, 10, True, False, 3)
plat52 = platform(screen, 1125, 750, 10, 10, True, False, 3)
plat53 = platform(screen, 1125, 650, 10, 10, True, False, 3)
plat54 = platform(screen, 1125, 550, 10, 10, True, False, 3)
plat55 = platform(screen, 1125, 450, 10, 10, True, False, 3)
plat56 = platform(screen, 1125, 350, 10, 10, True, False, 3)
plat57 = platform(screen, 1000, 250, 10, 10, True, False, 3)
while True:
  clock.tick(FPS)
  events = pygame.event.get()
  keys = pygame.key.get_pressed()
  screen.fill(blue)
  allSprites.update()
  pygame.display.flip()
  if level == "win":
    screen.fill(black)
    screen.blit(victoryText, (50, 500))
    pygame.display.flip()
    pygame.time.wait(10000)
    break