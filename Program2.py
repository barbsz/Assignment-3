import pygame 
import sys

pygame.init()
screen = pygame.display.set_mode((1000, 400))
pygame.display.set_caption("Farmer's Market")
TILE_SIZE = 128
clock = pygame.time.Clock()

background = pygame.image.load('cloud.png')
def background_sky(background):
    size= pygame.transform.scale(background, (1000,400))
    screen.blit(size, (0,0))


def draw_speech_bubble(screen, text, text_colour, bg_colour, pos, size):

    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, text_colour)
    text_rect = text_surface.get_rect(midbottom=pos)

     # background
    bg_rect = text_rect.copy()
    bg_rect.inflate_ip(10, 10)

    # Frame
    frame_rect = bg_rect.copy()
    frame_rect.inflate_ip(4, 4)

    pygame.draw.rect(screen, text_colour, frame_rect)
    pygame.draw.rect(screen, bg_colour, bg_rect)
    screen.blit(text_surface, text_rect)


# Read image utility function
def read_image(path, w=None, h=None):

    img = pygame.image.load(path)

    if (w == None) and (h == None):
        pass
    elif h == None:
        scale = w / img.get_width()
        h = scale * img.get_height()
        img = pygame.transform.scale(img, (int(w), int(h)))
    elif w == None:
        scale = h / img.get_height()
        w = scale * img.get_width()
        img = pygame.transform.scale(img, (int(w), int(h)))
    else:
        img = pygame.transform.scale(img, (int(w), int(h)))
    
    return img

# Define player class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        image = read_image('boy.png', w=TILE_SIZE, h=TILE_SIZE)
        self.image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect(topleft=(50, screen.get_height() - TILE_SIZE))

    def update(self):

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.rect.x -= 5
        if pressed[pygame.K_RIGHT]:
            self.rect.x += 5

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        draw_speech_bubble(screen, "I have 200 pesos, How many apples and oranges I can buy? ", (255, 255, 255), (0, 0, 0), self.rect.midtop, 25)

# Define NPC characters
class NPCOne(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image_left = read_image('girl2.png', w=TILE_SIZE, h=TILE_SIZE)
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = pygame.Surface(self.image_left.get_size(), pygame.SRCALPHA)
        self.image.blit(self.image_left, (0, 0))
        self.rect = self.image.get_rect(topleft=(400, screen.get_height() - TILE_SIZE))
        self.speaking = False

    def update(self, player):

        if abs(player.rect.x - self.rect.x) < 100:
            self.speaking = True
        else:
            self.speaking = False

        if player.rect.x < self.rect.x:
            self.image = self.image_left
        else:
            self.image = self.image_right

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.speaking:
            draw_speech_bubble(screen, "You can buy 4 oranges and 5 apples", (255, 255, 0), (175, 175, 0), self.rect.midtop, 25)


# Create player and NPCs
player = Player()
npc_one = NPCOne()

# Game loop
run=True
while run:


    clock.tick(60)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    # Update objects
    player.update()
    npc_one.update(player)

    # Draw objects
    screen.fill((255, 255, 255))
    background_sky(background)
    player.draw(screen)
    npc_one.draw(screen)

    # update display
    pygame.display.update()
    pygame.display.flip()
    