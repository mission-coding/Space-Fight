import pygame
import sys
import random
import time

pygame.init()

# Screen
screen_w = 400
screen_h = 525
screen = pygame.display.set_mode((screen_w, screen_h))
# Game Title
pygame.display.set_caption("Space Fight by Vivek")

# Colors
dark_blue = (0,0,50)
yellow = (255,255,0)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

# Images
bg_img = pygame.image.load("gallery/bg.jpg").convert_alpha()
bg_img2 = pygame.image.load("gallery/bg2.jpg").convert_alpha()
explode_img = pygame.image.load("gallery/explode.png").convert_alpha()
heart_img = pygame.image.load("gallery/heart.png").convert_alpha()
empty_heart_img = pygame.image.load("gallery/empty_heart.png").convert_alpha()
player_img = pygame.image.load("gallery/player.png").convert_alpha()
weapon_img = pygame.image.load("gallery/weapon.png").convert_alpha()
enemy_imgs = [pygame.image.load("gallery/enemy.png").convert_alpha(), 
              pygame.image.load("gallery/enemy2.png").convert_alpha(),
              pygame.image.load("gallery/enemy3.png").convert_alpha(),
              pygame.image.load("gallery/enemy4.png").convert_alpha()
              ]

class Player():
    def __init__(self) -> None:
        self.w = 65
        self.h = 53
        self.x = screen_w/2 - self.w/2
        self.y = screen_h - self.h
        self.speed = 8
        self.health = 5

    def draw(self):
        screen.blit(player_img, [self.x, self.y])
        # pygame.draw.rect(screen, yellow, [self.x, self.y, self.w, self.h])
        self.hitbox = (self.x, self.y, self.w, self.h)
        # pygame.draw.rect(screen, green, self.hitbox, 2)

    def move(self):
        keys = pygame.key.get_pressed()

        # Moving Player
        if keys[pygame.K_LEFT]:
            self.x -= self.speed

        elif keys[pygame.K_RIGHT]:
            self.x += self.speed

        elif keys[pygame.K_UP]:
            self.y -= self.speed
            
        elif keys[pygame.K_DOWN]:
            self.y += self.speed

        # Stoping Player when it goes out of the screen
        if self.x >= screen_w - self.w:
            self.x = screen_w - self.w 

        if self.x <= 0:
            self.x = 0 

        if self.y >= screen_h - self.h:
            self.y = screen_h - self.h 

        if self.y <= 0:
            self.y = 0 

class Enemy():
    def __init__(self, x, y) -> None:
        self.w = 66
        self.h = 64
        self.x = x
        self.y = y
        self.speed = 4
        self.health = 3
        self.hitbox = (self.x, self.y, self.w, self.h)
        self.image = random.choice(enemy_imgs)
        
    def draw(self):
        screen.blit(self.image, [self.x, self.y])
        # pygame.draw.rect(screen, red, [self.x, self.y, self.w, self.h])
        self.hitbox = (self.x, self.y, self.w, self.h)
        # pygame.draw.rect(screen, green, self.hitbox, 2)

    def move(self):
        self.y += self.speed

class Weapon():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.w = 8
        self.h = 23
        self.speed = 6
        self.hitbox = (self.x, self.y, self.w, self.h)

    def draw(self):
        screen.blit(weapon_img, [self.x, self.y])
        # pygame.draw.rect(screen, white, [self.x, self.y, self.w, self.h], border_top_left_radius=2, border_top_right_radius=2)
        self.hitbox = (self.x, self.y, self.w, self.h)
        # pygame.draw.rect(screen, green, self.hitbox, 2)

    def move(self):
        self.y -= self.speed

def game_loop():
    # Global Variables
    player = Player()
    enemy = Enemy(random.randint(0, screen_w - 30), -20)
    weapon = Weapon(player.x + 35, player.y + 35)
    clock = pygame.time.Clock()
    fps = 30
    enemies = []
    enemy_count = 0
    weapons = []
    weapon_count = 0
    score = 0
    over = False
    x1 = 0
    y1 = 0
    y2 = -screen_h
    bg_speed = 3
    explode = False

    def draw_text(text, color , size , x, y):
        font = pygame.font.Font(None, size)
        display_text = font.render(text, True, color)
        screen.blit(display_text, [x,y])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and over==True:
                    game_loop()
        
        # importing hi-score:
        with open("gallery/hiscore.txt", "r") as f:
            hiscore = int(f.read())


        if not over:
        # Displaying Enemy's Spaceships after some time gap
            enemy_count += 1
            if enemy_count > 30:
                random.shuffle(enemy_imgs)
                enemies.append(Enemy(random.randint(0, screen_w - enemy.w), -65))
                enemy_count = 0

            # Displaying Player's Bullets after some time gap
            weapon_count += 1
            if weapon_count > 10:
                weapons.append(Weapon(player.x + 30, player.y + 10))
                weapon_count = 0

            # Drawing All the objects
            
            screen.blit(bg_img, [x1, y1])
            screen.blit(bg_img2, [x1, y2])

            y1 += bg_speed
            y2 += bg_speed

            if y1 >= screen_h:
                y1 = -screen_h
            if y2 >= screen_h:
                y2 = -screen_h


        for i in enemies:
            i.draw()
            i.move()

        for i in weapons:
            i.draw()
            i.move()
            
        player.draw()
        player.move()

        # Hearts or player's health
        if player.health == 1 or 1 < player.health <= 5:
            screen.blit(heart_img, [10, 10])
        else:
            screen.blit(empty_heart_img, [10, 10])
        if player.health == 2 or 2 < player.health <= 5:
            screen.blit(heart_img, [35, 10])
        else:
            screen.blit(empty_heart_img, [35, 10])
        if player.health == 3 or 3 < player.health <= 5:
            screen.blit(heart_img, [60, 10])
        else:
            screen.blit(empty_heart_img, [60, 10])
        if player.health == 4 or 4 < player.health <= 5:
            screen.blit(heart_img, [85, 10])
        else:
            screen.blit(empty_heart_img, [85, 10])
        if player.health == 5:
            screen.blit(heart_img, [110, 10])
        else:
            screen.blit(empty_heart_img, [110, 10])

        # increasing hiscore when hiscore breaks
        if score >= hiscore:
            hiscore = score
            
        # Displaying Score 
        draw_text(f"Hi-score: {hiscore}  Score: {score}", green, 27, screen_w-220, 10)
        
        if not over:
            for enemy_ship in enemies[:]:
                # Moving Enemy's Spaceships toward Player's Shapeship
                if abs(player.hitbox[0] - enemy_ship.hitbox[0]) > 5:
                    if player.hitbox[0] < enemy_ship.hitbox[0]:
                        enemy_ship.x -= 1
                    elif player.hitbox[0] > enemy_ship.hitbox[0]:
                        enemy_ship.x += 1
                
                # Reducing Player's health
                if (player.hitbox[1] + player.hitbox[3] > enemy_ship.hitbox[1] and
                    player.hitbox[1] < enemy_ship.hitbox[1] + enemy_ship.hitbox[3] and
                    player.hitbox[0] + player.hitbox[2] > enemy_ship.hitbox[0] and
                    player.hitbox[0] < enemy_ship.hitbox[0] + enemy_ship.hitbox[2]):
                    player.health -= 1
                    screen.blit(explode_img, [enemy_ship.x , enemy_ship.y])
                    explode = True
                    if explode:
                        screen.blit(explode_img, [enemy_ship.x, enemy_ship.y])
                    enemies.remove(enemy_ship)
                    # print(player.health)

             # Destroying enemy's shape ship with bullets
            for weapon in weapons[:]:
                for enemy_ship in enemies[:]:
                    if weapon.hitbox[1] < enemy_ship.hitbox[1] + enemy_ship.hitbox[3] and weapon.hitbox[1] + weapon.hitbox[3] > enemy_ship.hitbox[1]:
                        if weapon.hitbox[0] < enemy_ship.hitbox[0] + enemy_ship.hitbox[2] and weapon.hitbox[0] + weapon.hitbox[2] > enemy_ship.hitbox[0]:
                            weapons.remove(weapon)
                            enemy_ship.health -=1

                        if enemy_ship.health == 0:
                            explode = True
                            if explode:
                                curtime = time.time()
                                screen.blit(explode_img, [enemy_ship.x, enemy_ship.y])
                            enemies.remove(enemy_ship)
                            score += 1

            # Game over when player health finished
            if player.health <= 0:
                over = True

        if over:
            bg_speed = 0
            player.speed = 0 
            for enemy_ship in enemies[:]:
                enemy_ship.speed = 0
            for weapon in weapons[:]:
                weapon.speed = 0 

            if score >= hiscore:
                with open("gallery/hiscore.txt", "w") as f:
                    f.write(str(score))

            draw_text("Game Over!", red, 40, screen_w/2-80, screen_h/2-20)

        # Giving FPS to the game
        clock.tick(fps)

        # Updating everything
        pygame.display.update()

game_loop()
