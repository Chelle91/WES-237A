"""
Bop It! Game Dashboard - Main Server Interface
This script creates a visual dashboard to display game status and player scores.
It acts as the central server that receives updates from connected PYNQ client boards.
"""

import pygame
import socket
import threading
import json
import Extras
import random
import time
import sys

def button_check():
    global state, button
    print("Checks the button state")
    if button < 5:  # Condition for loss
        screen.fill((0, 0, 0))
        text = FONT.render("YOU LOSE", True, (255, 255, 255))
        text_rect = text.get_rect(center=(600 // 2, 400 // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)
        state = "LOSE"
    else:
        screen.fill((0, 0, 0))
        text = FONT.render("YOU DID IT", True, (255, 255, 255))
        text_rect = text.get_rect(center=(600 // 2, 400 // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(500)

def tilt_check():
    global state, tilt
    print("Checks the tilt state")
    if tilt < 5:  # Condition for loss
        screen.fill((0, 0, 0))
        text = FONT.render("YOU LOSE", True, (255, 255, 255))
        text_rect = text.get_rect(center=(600 // 2, 400 // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)
        state = "LOSE"
    else:
        screen.fill((0, 0, 0))
        text = FONT.render("YOU DID IT", True, (255, 255, 255))
        text_rect = text.get_rect(center=(600 // 2, 400 // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(500)

def light_check():
    global state, light
    print("Checks the light state")
    if light > 5:  # Condition for loss (i.e. too much light)
        screen.fill((0, 0, 0))
        text = FONT.render("YOU LOSE", True, (255, 255, 255))
        text_rect = text.get_rect(center=(600 // 2, 400 // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)
        state = "LOSE"
    else:
        screen.fill((0, 0, 0))
        text = FONT.render("YOU DID IT", True, (255, 255, 255))
        text_rect = text.get_rect(center=(600 // 2, 400 // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(500)

def joystick_check():
    global state, joystick
    print("Checks the joystick state")
    if joystick > 5:  # Condition for loss
        screen.fill((0, 0, 0))
        text = FONT.render("YOU LOSE", True, (255, 255, 255))
        text_rect = text.get_rect(center=(600 // 2, 400 // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)
        state = "LOSE"
    else:
        screen.fill((0, 0, 0))
        text = FONT.render("YOU DID IT", True, (255, 255, 255))
        text_rect = text.get_rect(center=(600 // 2, 400 // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(500)

def Start_Game():
    global state
    Ready_text = FONT.render("Ready", True, BLACK)
    Waittime = 1000  # in ms
    checktime = 5    # in seconds

    while True:
        time.sleep(1)

        print(state)
        print(Waittime)
        print(checktime)

        if state == "LOSE":
            pygame.quit()
            sys.exit()

        for i in range(5, 0, -1):
            screen.fill((0, 0, 0))
            text = FONT.render(str(i), True, (255, 255, 255))
            text_rect = text.get_rect(center=(600 // 2, 400 // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(Waittime)

        boptable = random.randint(1,4)

        if boptable == 1:  # Button challenge
            screen.fill((0, 0, 0))
            text = FONT.render("PUSH IT (BUTTON)", True, (255, 255, 255))
            text_rect = text.get_rect(center=(600 // 2, 400 // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            timer = threading.Timer(checktime, button_check)
            timer.start()
            time.sleep(checktime)
            checktime = checktime - 0.5
            Waittime = int(Waittime - (Waittime * 0.2))

        elif boptable == 2:  # Tilt challenge
            screen.fill((0, 0, 0))
            text = FONT.render("TILT IT", True, (255, 255, 255))
            text_rect = text.get_rect(center=(600 // 2, 400 // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            timer = threading.Timer(checktime, tilt_check)
            timer.start()
            time.sleep(checktime)
            checktime = checktime - 0.5
            Waittime = int(Waittime - (Waittime * 0.2))

        elif boptable == 3:  # Light challenge
            screen.fill((0, 0, 0))
            text = FONT.render("LIGHT IT", True, (255, 255, 255))
            text_rect = text.get_rect(center=(600 // 2, 400 // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            # Call the light sensor check here
            timer = threading.Timer(checktime, light_check)
            timer.start()
            time.sleep(checktime)
            checktime = checktime - 0.5
            Waittime = int(Waittime - (Waittime * 0.2))

        elif boptable == 4:  # Joystick challenge
            screen.fill((0, 0, 0))
            text = FONT.render("STICK IT", True, (255, 255, 255))
            text_rect = text.get_rect(center=(600 // 2, 400 // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            timer = threading.Timer(checktime, joystick_check)
            timer.start()
            time.sleep(checktime)
            checktime = checktime - 0.5
            Waittime = int(Waittime - (Waittime * 0.2))

        print('Button Pressed')

# Initialize pygame for the graphical interface
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bop It! Game Dashboard")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

# Initialize game state variables
players = {}
time_left = 60
game_status = "Waiting for players..."
button = 1
tilt = 1
light = 1
joystick = 1
objects = []
state = "WIN"

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("0.0.0.0", 5005))

def listen_for_updates():
    global players, time_left, game_status, button, tilt, light, joystick
    while True:
        data, addr = server.recvfrom(1024)
        try:
            print(data)
            update = json.loads(data.decode())
            players = update.get("players", {})
            button = update.get("button")
            tilt = update.get("tilt")
            light = update.get("light")
            joystick = update.get("joystick")
            time_left = update.get("time_left", 60)
            game_status = update.get("status", "Game in progress")
        except json.JSONDecodeError:
            print("Error decoding JSON data.")

threading.Thread(target=listen_for_updates, daemon=True).start()

def draw_start():
    screen.fill(WHITE)
    Extras.Button(30, 180, 400, 100, screen, objects, 'Start Game', Start_Game)
    for obj in objects:
        obj.process()
    status_text = FONT.render(f"Status: {game_status}", True, BLACK)
    time_text = FONT.render(f"Time Left: {time_left}s", True, BLACK)
    screen.blit(status_text, (20, 20))
    screen.blit(time_text, (20, 60))
    y_offset = 100
    for player, stats in players.items():
        text = FONT.render(f"{player}: {stats['successes']} points", True, BLACK)
        screen.blit(text, (20, y_offset))
        y_offset += 40
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_start()
    pygame.time.delay(100)
pygame.quit()
