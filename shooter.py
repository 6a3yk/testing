from pygame import *
from random import randint
import time as t
init()
mixer.init()
font.init()


class GameSprite(sprite.Sprite):  #обищй класс спрайт
    def __init__(self, player_image, player_x, player_y, player_speed,w,h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):  #класс пуля
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 5:
            self.kill()
class Player(GameSprite):  #класс Игрок
    def update(self):
        global win_width, win_height
        key_pressed = key.get_pressed()
        if (key_pressed[K_LEFT] or key_pressed[K_a]) and self.rect.x > 150:
            self.rect.x -= self.speed
        if (key_pressed[K_RIGHT] or key_pressed[K_d]) and self.rect.x < win_width-150:
            self.rect.x += self.speed
    def fire(self):
        bullet1 = Bullet('bullet.png', self.rect.centerx,self.rect.top,10,10,30)
        bullets.add(bullet1)
        global last_fire, fire
        last_fire = t.time()
        fire.play()
        
        
class Enemy(GameSprite):  #класс Враг
    global win_width, win_height
    def update(self):
        global win_width
        self.rect.y += self.speed
        if self.rect.y >= 500:
            global lost
            lost += 1
            self.rect.x = randint(50,win_width-150)
            self.rect.y = 0


window = display.set_mode((0, 0), FULLSCREEN)
win_width,win_height = display.get_surface().get_size() 

FPS = 30
game = True
finish = False
score = 0
lost = 0

clock = time.Clock()
font0 = font.Font(None,100)
font1 = font.Font(None,30)

win_image = font0.render('YOU WON YEEE', True, (0,255,255) ) 
lose_image = font0.render('YOU SUS LOSER', True, (255,0,0) )
display.set_caption('Shooter')

backround = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
mixer.music.load('space.ogg')
kick = mixer.Sound('fire.ogg')
mixer.music.play()

player = Player

player = Player('rocket.png', win_width//2,win_height-200,10,65,65)
bullets = sprite.Group()
monsters = sprite.Group()
last_fire = 0
for i in range(5):
    monsters.add(Enemy('ufo.png',randint(150,win_width-150),randint(-250,-30),randint(3,5),45,45))

while game:
    #обнова экрана
    display.update()
    #задержка
    clock.tick(FPS)
    #обработка событий
    for event0 in event.get():
        if event.type == QUIT:
            game == False
        elif event0.type == KEYDOWN and event.key == K_SPACE:
            if t.time() - last_fire > 0.3 and not(finish):
                player.fire()
    if not (finish):    
        #игрологика        
        player.update()
        monsters.update()
        bullets.update()

        monsters_list = sprite.groupcollide(monsters,bullets,True,True)
        for monst in monsters_list:
            score +=1
            monsters.add(Enemy('ufo.png',randint(50,win_width-50),randint(-250,-30),randint(1,3),45,45))
            
                                                #события и игровая логика
        image_score = font1.render('Счёт: '+str(score), True, (255,255,255))
        image_lost = font1.render('Пропущено: '+str(lost), True, (255,255,255))


        #чистка экрана(фон) 
        window.blit(backround,(0,0))

        #отрисовка
        window.blit(image_score,(250,150))
        window.blit(image_lost,(250,200))

        player.reset()
        monsters.draw(window)
        bullets.draw(window)

        if score >= 50:
            window.blit(win_image, (win_width//2,win_height//2))
            finish = True

        monsters_list = sprite.spritecollide(player, monsters,True)
        if len(monsters_list) > 0:
            window.blit(lose_image, (win_width//2,win_height//2))
            finish = True

