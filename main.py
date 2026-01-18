import random
import pygame
import asyncio
# pygbag: web
#setup
pygame.init()

pygame.display.set_caption("simulation")

clock = pygame.time.Clock()
async def main():
  #screen stuff
  WIDTH, HEIGHT = 1920, 1080
  screen = pygame.display.set_mode((WIDTH, HEIGHT))

  #character width and height
  CWIDTH, CHEIGHT = 90, 256

  #colors
  WHITE = (255, 255, 255)
  BLACK = (0, 0, 0)
  GRAY = (150, 150, 150)
  HOVER = (100, 100, 255)

  #what screen it is in rn
  SCREEN = "main menu"

  #fonts
  title_font = pygame.font.Font(None, 80)
  button_font = pygame.font.Font(None, 50)

  # Load sprites
  walk1 = pygame.image.load("walkframe1.png").convert_alpha()
  walk2 = pygame.image.load("walkframe2.png").convert_alpha()
  walk3 = pygame.image.load("walkframe3.png").convert_alpha()
  walk4 = pygame.image.load("walkframe4.png").convert_alpha()

  # Scale sprites for better visibility
  walk1 = pygame.transform.scale(walk1, (CWIDTH, CHEIGHT))
  walk2 = pygame.transform.scale(walk2, (CWIDTH, CHEIGHT))
  walk3 = pygame.transform.scale(walk3, (CWIDTH, CHEIGHT))
  walk4 = pygame.transform.scale(walk4, (CWIDTH, CHEIGHT))

  #movement stuff
  x = 1
  y = 1

  #walk cycle
  sprites = [walk1, walk2, walk3, walk4]
  current_sprite = 0
  animation_counter = 0

  #locate the character
  char_rect = sprites[0].get_rect()
  char_rect.topleft = (x, 600)

  #create mask for collision
  char_mask = pygame.mask.from_surface(sprites[0])

  class Rain:
    #when raindrop created, trigger reset and also draw mask for collision
    def __init__(self):
      self.reset()
      self.mask = pygame.mask.Mask((1, 1), True)

    #recreates some more raindrops from ones that reset
    def reset(self):
      self.x = random.randint(0, WIDTH)
      self.y = random.randint(-100, 0)
      self.fallspd = random.randint(5, 10)
      self.rect = pygame.Rect(self.x, self.y, 2, 10)
    
    #drawing the raindrops and reset
    def update(self):
      self.y += self.fallspd
      self.rect.topleft = (self.x, self.y)
      if self.y > HEIGHT:
        self.reset()
    
    def draw(self, surface):
      pygame.draw.line(surface, (100, 100, 255), (self.x, self.y), (self.x, self.y+10), 2)

  #make the buttons work
  class Button:
    def __init__(self, text, center_pos, width=200, height=60):
      self.text = text
      self.rect = pygame.Rect(0, 0, width, height)
      self.rect.center = center_pos
      self.color = GRAY
      self.hover_color = HOVER

    def draw(self, surface):
      mouse_pos = pygame.mouse.get_pos()
      if self.rect.collidepoint(mouse_pos):
          color = self.hover_color
      else:
          color = self.color
      pygame.draw.rect(surface, color, self.rect)
      # Draw text
      txt_surf = button_font.render(self.text, True, BLACK)
      txt_rect = txt_surf.get_rect(center=self.rect.center)
      surface.blit(txt_surf, txt_rect)

    def is_clicked(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # left click
          if self.rect.collidepoint(event.pos):
            return True
      return False
    
  #button creation
  walk_button = Button("walk", (WIDTH//2, HEIGHT//2))
  run_button = Button("run", (WIDTH//2, HEIGHT//2 + 100))
  menu_button = Button("main menu", (WIDTH // 2, HEIGHT // 2 + 200))

  #create 300 raindrops
  raindrops = [Rain() for i in range (300)]
  hitcount = 0

  #main loop
  running = True

  while running:
    clock.tick(60)
    screen.fill((56, 93, 158))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
    
      if SCREEN == "main menu":
        if walk_button.is_clicked(event):
            y = 1
            SCREEN = "game"
      
      if SCREEN == "main menu":
        if run_button.is_clicked(event):
          y = 3
          SCREEN = "game"

    if SCREEN == "main menu":
      screen.fill(WHITE)
      title = title_font.render("rain simulation", True, BLACK)
      screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))
      walk_button.draw(screen)
      run_button.draw(screen)

    elif SCREEN == "game":
      screen.fill((56, 93, 158))

      for i in raindrops:
        i.update()
        i.draw(screen)
        #find positions of drop and character relative to eachother
        offset_x = i.rect.x - char_rect.x
        offset_y = i.rect.y - char_rect.y

        #check for the overlap of masks for hit 
        if char_mask.overlap(i.mask, (offset_x, offset_y)):
          hitcount += 1
          i.reset()
    
      #cycle through sprites every 10 frames, also updating the mask so the collision detection will still work
      animation_counter += 1
      if animation_counter >= 10:
        current_sprite = (current_sprite+1) % len(sprites)
        char_mask = pygame.mask.from_surface(sprites[current_sprite])
        animation_counter = 0
      
      #running speedup
      x += y
      y *= 1.001
      if y >= 10:
        y = 10
      
      char_rect.topleft = (x, 600)
      screen.blit(sprites[current_sprite], (x, 600))
      pygame.draw.rect(screen, BLACK, pygame.Rect(0, 847, WIDTH, 300))

      if x >= WIDTH:
        SCREEN = "end"
    
    elif SCREEN == "end":
      screen.fill(WHITE)
      end_title = title_font.render(str(hitcount) + " raindrops hit him", True, BLACK)
      end_title_rect = end_title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
      screen.blit(end_title, end_title_rect)
      menu_button.draw(screen)
      if menu_button.is_clicked(event):
          # reset game state
          SCREEN = "main menu"
          x = 1
          y = 1
          hitcount = 0
          current_sprite = 0
          animation_counter = 0

          for drop in raindrops:
              drop.reset()
    await asyncio.sleep(0)
    pygame.display.flip()
asyncio.run(main())