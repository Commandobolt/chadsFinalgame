import pygame
import sys
import random
from game_util import *
from pygame import mixer
import time

# Initialize Pygame
pygame.init()

#Create Pygame clock
clock = pygame.time.Clock()

# Clear terminal output.
for ii in range(0, 10):
    print()

print('\nRunning main.py.')
print('-------------------------------------------\n')

# Screen dimensions
scr_wid = 1000  # (px)
scr_hgt = 600  # (px)

# Create the screen
scr = pygame.display.set_mode((scr_wid, scr_hgt))
pygame.display.set_caption('Making a customized background')

#make static background
background = scr.copy()
make_background(background)

#Show splash screen
startscreen(background)

#background music
mixer.init()
mixer.music.load('pirate/pirate_song.ogg')
mixer.music.play()

#update display
pygame.display.flip()

#make the ai ships
num_boats = 6
boat_list = []
for ii in range(0, int(num_boats)):
    boat_list.append(Boat(scr, '1'))

#make tank
fury = Tank(scr)

# Spawn rate.
spawn_rate = .5  # hz.

# Create time epoch.
t0 = time.time()
t1 = 0.0
t_spawn = 0.0
t_wave = 0.0
level = 0
points = 0

running = True
while running:

    # draw the background
    scr.blit(background, (0, 0))

    # Update time.
    t1 = time.time() - t0
    txt = f't1 = {t1:.2f} s.'

    #updates time and level
    arial = pygame.font.SysFont('Arial', 20)
    text_level = arial.render(f'Level: {level}', True, (0, 0, 0))
    scr.blit(text_level, (scr.get_width() - 60, 40))

    text_time = arial.render(f'{t1}', True, (0, 0, 0))
    scr.blit(text_time, (scr.get_width() - 60, 10))

    text_points = arial.render(f'Points: {points}', True, (0, 0, 0))
    scr.blit(text_points, (scr.get_width() - 160, 10))

    # Spawn ships at a select rate.
    if t1 - t_spawn >= 1/spawn_rate:

        # Reset t_spawn.
        t_spawn = t1

        # Spawn.
        if len(boat_list) < 1000:
            boat_list.append(Boat(scr, f'{random.randint(1,6)}'))
            points += 1

    #spawn waves
    if t1 - t_wave >= 15:
        # Reset t_wave.
        t_wave = t1
        for ii in range(num_boats):
            boat_list.append(Boat(scr, f'{random.randint(1,6)}'))
        # boat speed increases over time
        level += 1
        num_boats += 1

    #create boxes
    #box1 = Box(scr,10, 10)

    # store events in a temp. variable so that you still have an instance of it even after the get function wipes the event list
    events = pygame.event.get()

    # Get events happening in window.
    for event in events:

        #when user presses a key
        if event.type == pygame.KEYDOWN:
            print(f'user has pressed down')
        if event.type == pygame.KEYUP:
            print(f'user has pressed up')

        if event.type == pygame.QUIT:
            running = False

    for boat in boat_list:
        boat.update_pos(scr, level)
        if boat.get_boatx() < 100:
            running = False
        if boat.check_hp():
            boat_list.remove(boat)
            points += 1

    fury.draw_tank(scr)
    fury.update_bullet_pos(scr, events, boat_list)

    # Display scr.
    pygame.display.flip()

    clock.tick(60)

startscreen(background, "Game Over", f"You scored {points} points")

pygame.display.flip()


