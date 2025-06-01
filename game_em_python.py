import pgzrun
import random
import math
from pygame import Rect

WIDTH = 800
HEIGHT = 600

# Game States
MENU = "menu"
PLAYING = "playing"
EXIT = "exit"

game_state = MENU
music_on = True

# Assets
hero_idle = ["hero_idle1", "hero_idle2"]
hero_run = ["hero_run1", "hero_run2"]
enemy_walk = ["enemy_walk1", "enemy_walk2"]

# Load background music and sound
music.set_volume(0.5)
music.play("bg_music")

# Classes
class Button:
    def __init__(self, text, x, y, w, h, callback):
        self.text = text
        self.rect = Rect((x, y), (w, h))
        self.callback = callback

    def draw(self):
        screen.draw.filled_rect(self.rect, "gray")
        screen.draw.textbox(self.text, self.rect, color="black")

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

class Hero:
    def __init__(self):
        self.actor = Actor(hero_idle[0], (100, HEIGHT - 100))
        self.vx = 0
        self.vy = 0
        self.on_ground = True
        self.frame = 0
        self.idle = True
        self.direction = 1

    def update(self):
        self.frame += 0.1
        if self.idle:
            self.actor.image = hero_idle[int(self.frame) % len(hero_idle)]
        else:
            self.actor.image = hero_run[int(self.frame) % len(hero_run)]

        self.vy += 0.5
        self.actor.y += self.vy
        self.actor.x += self.vx

        if self.actor.y >= HEIGHT - 50:
            self.actor.y = HEIGHT - 50
            self.vy = 0
            self.on_ground = True

    def draw(self):
        self.actor.draw()

class Enemy:
    def __init__(self, x, y, patrol_range):
        self.actor = Actor(enemy_walk[0], (x, y))
        self.frame = 0
        self.range = patrol_range
        self.origin_x = x
        self.vx = 2

    def update(self):
        self.frame += 0.1
        self.actor.image = enemy_walk[int(self.frame) % len(enemy_walk)]

        self.actor.x += self.vx
        if self.actor.x > self.origin_x + self.range or self.actor.x < self.origin_x - self.range:
            self.vx = -self.vx

    def draw(self):
        self.actor.draw()

# Game Objects
hero = Hero()
enemies = [Enemy(400, HEIGHT - 50, 100), Enemy(600, HEIGHT - 50, 150)]

# Menu buttons
buttons = []
def start_game():
    global game_state
    game_state = PLAYING

def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        music.play("bg_music")
    else:
        music.stop()

def exit_game():
    exit()

buttons.append(Button("Start Game", 300, 200, 200, 50, start_game))
buttons.append(Button("Toggle Music", 300, 270, 200, 50, toggle_music))
buttons.append(Button("Exit", 300, 340, 200, 50, exit_game))

# Game Loop Functions
def update():
    if game_state == PLAYING:
        hero.update()
        for enemy in enemies:
            enemy.update()

def draw():
    screen.clear()
    if game_state == MENU:
        screen.draw.text("Platformer Game", center=(WIDTH//2, 100), fontsize=60, color="white")
        for btn in buttons:
            btn.draw()
    elif game_state == PLAYING:
        screen.fill((0, 100, 255))  # Blue sky
        hero.draw()
        for enemy in enemies:
            enemy.draw()

def on_mouse_down(pos):
    if game_state == MENU:
        for btn in buttons:
            btn.click(pos)

def on_key_down(key):
    if game_state == PLAYING:
        if key == keys.RIGHT:
            hero.vx = 5
            hero.idle = False
            hero.direction = 1
        elif key == keys.LEFT:
            hero.vx = -5
            hero.idle = False
            hero.direction = -1
        elif key == keys.SPACE and hero.on_ground:
            hero.vy = -10
            hero.on_ground = False

def on_key_up(key):
    if game_state == PLAYING:
        if key in (keys.RIGHT, keys.LEFT):
            hero.vx = 0
            hero.idle = True

pgzrun.go()