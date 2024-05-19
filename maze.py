from random import choice
from pygame import *


init()
font.init()
font1 = font.SysFont("Impact", 100)
game_over_text = font1.render("все, капець", True, (224, 205, 153))
mixer.init()
mixer.music.load('jungles.ogg')
# mixer.music.play()
mixer.music.set_volume(0.2)

MAP_WIDTH, MAP_HEIGHT = 25, 20 # ширина і висота карти
TILESIZE = 30 #розмір квадратика карти
WIDTH, HEIGHT = MAP_WIDTH*TILESIZE, MAP_HEIGHT*TILESIZE

window = display.set_mode((WIDTH,HEIGHT))
FPS = 90
clock = time.Clock()

bg = image.load('forest_PNG3.png')
bg = transform.scale(bg,(WIDTH,HEIGHT))

cyborg_img = image.load("35-350637_arctic-wolf-sprite-super-mario-world-star-png-removebg-preview.png")
player_img = image.load("스크린샷+2019-03-18+오후+3.47.57-removebg-preview.png")
wall_img = image.load("1559585070grass-png-11-removebg-preview.png")
gold_img = image.load("Carrot-PNG.png")
all_sprites = sprite.Group()

class Sprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)

class Player(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.hp = 100
        self.speed = 4

    def update(self):
        key_pressed = key.get_pressed()
        old_post = self.rect.x, self.rect.y
        if key_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed


        collide_list = sprite.spritecollide(self, walls, False)
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_post

        collide_list = sprite.spritecollide(self, enemys, False, sprite.collide_mask)
        if len(collide_list) > 0:
            self.hp -= 100


class Enemy(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.hp = 100
        self.speed = 2
        self.dir_list = ['right', 'left', 'up', 'down']
        self.dir = choice(self.dir_list)

        
    def update(self):
        old_pos = self.rect.x, self.rect.y
        if self.dir == 'right':
            self.rect.x += self.speed
        elif self.dir == 'left':
            self.rect.x -= self.speed
        elif self.dir == 'up':
            self.rect.y += self.speed
        elif self.dir == 'down':
            self.rect.y -= self.speed

        collide_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_pos
            self.dir = choice(self.dir_list)



player = Player(player_img, TILESIZE-5, TILESIZE-5, 300, 300)
walls = sprite.Group()
enemys = sprite.Group()

with open("map.txt", "r") as f:
    map = f.readlines()
    x = 0
    y = 0
    for line in map:
        for symbol in line:
            if symbol == "w": 
                walls.add(Sprite(wall_img, TILESIZE, TILESIZE, x, y))
            if symbol == "p": # гравець
                player.rect.x = x
                player.rect.y = y
            if symbol == "g": # стіни
                gold = Sprite(gold_img, 70, 70, x, y )
            if symbol == "e": 
                enemys.add(Enemy(cyborg_img, TILESIZE+5, TILESIZE+5, x, y))
                
            x += TILESIZE
        y += TILESIZE
        x = 0



run = True
finish = False
game_win_text = font1.render("все", True, (200, 100, 153))
       
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
    window.fill((141, 143, 224))
    window.blit(bg,(0,0))
    all_sprites.draw(window)
    if player.hp <= 0:
        finish = True
    if sprite.collide_mask(player, gold):
        finish = True
        game_win_text = font1.render("супер", True, (200, 100, 153))
       
    
    if not finish :
        all_sprites.update()
    else:
        window.blit(game_win_text, (WIDTH /2 - game_win_text.get_width() /2, 200))
        
    display.update()
    clock.tick(FPS)