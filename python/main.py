import os
from tkinter import NW, Canvas, Label, PhotoImage, font, simpledialog
import tkinter as tk
import pygame
import random


# Game settings
pygame.init()

info_object = pygame.display.Info()

WIDTH, HEIGHT = info_object.current_w, info_object.current_h-50
CELL_SIZE = 50
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 15
LINE_COLOR = (255, 255, 255)
# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255,255,255)
TRANS = (255,255,255,128)

ENABLED = True
longestRun = 0
shortestRun = 0
average = 0

# Initialize Pygame and the mixer module
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wandering in the Woods Game")
clock = pygame.time.Clock()

# Global variables
background = pygame.image.load('p1.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

runcount = 1
runtime = []

# Load the audio file
meetup_sound = pygame.mixer.Sound('meetup_sound.wav')

font = pygame.font.SysFont(None, 36)


class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback

    def draw(self):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        text_surface = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()

# player_image = pygame.image.load('success.png')  # Ensure you have a file named player_image.png in your directory
# player_image = pygame.transform.scale(player_image, (WIDTH, HEIGHT))  # Resize the image to fit the screen


class Window:
    
    def __init__(self, image):
        self.image = image
        self.root = tk.Tk()
        self.widgets()
        self.root.mainloop()
    def widgets(self):
        self.img = PhotoImage(file=self.image)
        label = tk.Label(self.root, image=self.img)
        label.pack()
image = "success.png"

def second_screen():
    root = tk.Tk()
    root.title("Display Image using tkinter")

    # Load the image
    image = tk.PhotoImage(file="download.png")

    # Display the image in a label
    label = Label(root, image=image)
    label.pack()

    root.mainloop()

     
    

def start_menu():
    buttons = [
        Button(WIDTH // 2 - 75, 150, 150, 50, 'K-2', game_for_K2(10,10,2)),
        Button(WIDTH // 2 - 75, 250, 150, 50, '3-5', game_for_35),
        Button(WIDTH // 2 - 75, 350, 150, 50, '6-8', game_for_68)
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.check_click(event.pos)

        screen.blit(background, (0, 0))
        for button in buttons:
            button.draw()
        pygame.display.flip()

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, y), (WIDTH, y))

class Player:
    def __init__(self, x, y, player_image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(player_image)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))

    def move(self, grid_width, grid_height):
        direction = random.choice(["up", "down", "left", "right"])
        if direction == "up" and self.y > 0:
            self.y -= 1
        elif direction == "down" and self.y < grid_height - 1:
            self.y += 1
        elif direction == "left" and self.x > 0:
            self.x -= 1
        elif direction == "right" and self.x < grid_width - 1:
            self.x += 1

    def draw(self):
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        draw_grid()


class Group:
    def __init__(self):
        self.players = []

    def add(self, player):
        self.players.append(player)

    def move(self, grid_width, grid_height):
        direction = random.choice(["up", "down", "left", "right"])
        for player in self.players:
            next_x, next_y = player.x, player.y
            if direction == "up" and player.y > 0:
                next_y -= 1
            elif direction == "down" and player.y < grid_height - 1:
                next_y += 1
            elif direction == "left" and player.x > 0:
                next_x -= 1
            elif direction == "right" and player.x < grid_width - 1:
                next_x += 1

            if not any(p.x == next_x and p.y == next_y for p in self.players):
                player.x, player.y = next_x, next_y

def game_for_K2(grid_width, grid_height, num_players):
    player_images = ['player1.png', 'player2.png']
    if num_players <= 0:
        raise ValueError(f"Must have at least one player")

    players = [Player(random.randint(0, grid_width - 1), random.randint(0, grid_height - 1), player_images[i % len(player_images)]) for i in range(num_players)]

    groups = [Group() for _ in range(num_players)]
    for i, player in enumerate(players):
        groups[i].add(player)

    move_count = 0
    runs = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.blit(background, (0, 0))

        for group in groups:
            group.move(grid_width, grid_height)

        move_count += 1

        merged = False
        for i, group1 in enumerate(groups):
            for player1 in group1.players:
                for j, group2 in enumerate(groups):
                    if i != j:
                        for player2 in group2.players:
                            if player1.x == player2.x and player1.y == player2.y:
                                group1.add(player2)
                                group2.players.remove(player2)
                                merged = True

        if merged:
            groups = [group for group in groups if group.players]

        for player in players:
            player.draw()

        if len(groups[0].players) == num_players:
            runs.append(move_count)
            rr = max(runs)
            runtime.append(rr)
            longest_run = max(runtime)
            shortest_run = min(runtime)
            average_run = _sum(runtime) / len(runtime)

            # Play the audio when all players meet
            meetup_sound.play()
            second_screen()

            return longest_run, shortest_run, average_run

        pygame.display.flip()
        clock.tick(FPS)



def game_for_35(grid_width, grid_height, num_players):
    player_images = ['player1.png', 'player2.png', 'player3.png', 'player4.png']
    if ENABLED:
        root = tk.Tk()
        root.withdraw()
        # grid_width = simpledialog.askinteger("Input", "Enter grid width:", parent=root, minvalue=5, maxvalue=500)
        # grid_height = simpledialog.askinteger("Input", "Enter grid height:", parent=root, minvalue=5, maxvalue=500)
        num_players = simpledialog.askinteger("Input", "Enter number of players:", parent=root, minvalue=2, maxvalue=4)
        root.destroy()
        # screen = pygame.display.set_mode((grid_width, grid_height))
        # pygame.display.set_caption("Wandering in the Woods Game")
        
        # background = pygame.image.load('background.jpg')
        # background = pygame.transform.scale(background, (grid_width, grid_height))
    if num_players <= 0:
        raise ValueError(f"Must have at least one player")
    players = [Player(random.randint(0, grid_width - 1), random.randint(0, grid_height - 1), player_images[i % len(player_images)]) for i in range(num_players)]
    groups = [Group() for _ in range(num_players)]
    for i, player in enumerate(players):
        groups[i].add(player)
    move_count = 0
    runs = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        screen.blit(background, (0, 0))
        for group in groups:
            group.move(grid_width, grid_height)
        move_count += 1
        merged = False
        for i, group1 in enumerate(groups):
            for player1 in group1.players:
                for j, group2 in enumerate(groups):
                    if i != j:
                        for player2 in group2.players:
                            if player1.x == player2.x and player1.y == player2.y:
                                group1.add(player2)
                                group2.players.remove(player2)
                                merged = True
        if merged:
            groups = [group for group in groups if group.players]
        for player in players:
            player.draw()
        if len(groups[0].players) == num_players:
            runs.append(move_count)
            rr = max(runs)
            runtime.append(rr)
            longest_run = max(runtime)
            shortest_run = min(runtime)
            average_run = _sum(runtime) / len(runtime)
            # Play the audio when all players meet
            meetup_sound.play()
            second_screen()

            return longest_run, shortest_run, average_run
        pygame.display.flip()
        clock.tick(FPS)
    


def game_for_68(grid_width, grid_height, num_players):
    player_images = ['player1.png', 'player2.png', 'player3.png', 'player4.png','player5.png']
    if ENABLED:
        root = tk.Tk()
        root.withdraw()
        # grid_width = simpledialog.askinteger("Input", "Enter grid width:", parent=root, minvalue=5, maxvalue=50)
        # grid_height = simpledialog.askinteger("Input", "Enter grid height:", parent=root, minvalue=5, maxvalue=50)
        num_players = simpledialog.askinteger("Input", "Enter number of players:", parent=root, minvalue=3, maxvalue=5)
        root.destroy()
    if num_players <= 0:
        raise ValueError(f"Must have at least one player")

    players = [Player(random.randint(0, grid_width - 1), random.randint(0, grid_height - 1), player_images[i % len(player_images)]) for i in range(num_players)]

    groups = [Group() for _ in range(num_players)]
    for i, player in enumerate(players):
        groups[i].add(player)

    move_count = 0
    runs = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.blit(background, (0, 0))

        for group in groups:
            group.move(grid_width, grid_height)

        move_count += 1

        merged = False
        for i, group1 in enumerate(groups):
            for player1 in group1.players:
                for j, group2 in enumerate(groups):
                    if i != j:
                        for player2 in group2.players:
                            if player1.x == player2.x and player1.y == player2.y:
                                group1.add(player2)
                                group2.players.remove(player2)
                                merged = True

        if merged:
            groups = [group for group in groups if group.players]

        for player in players:
            player.draw()

        if len(groups[0].players) == num_players:
            runs.append(move_count)
            rr = max(runs)
            runtime.append(rr)
            longest_run = max(runtime)
            shortest_run = min(runtime)
            average_run = _sum(runtime) / len(runtime)

            # Play the audio when all players meet
            meetup_sound.play()
            second_screen()


            return longest_run, shortest_run, average_run

        pygame.display.flip()
        clock.tick(FPS)

def _sum(arr):
    sum = 0
    for i in arr:
        sum = sum + i
 
    return(sum)

def display_statistics(longest_run, shortest_run, average_run, val):
    stats_window = True
    while stats_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.blit(background, (0, 0))
        font = pygame.font.SysFont(None, 45)
        hh = round(average_run, 2)
        longest_text = font.render(f"Longest Run: {longest_run}", True, WHITE)
        shortest_text = font.render(f"Shortest Run: {shortest_run}", True, WHITE)
        average_text = font.render(f"Average Run: {hh} ", True, WHITE)
        retry = font.render("Retry", True, BLACK)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Retry button
        retry_button_rect = pygame.Rect(50, 450, 200, 50)
        pygame.draw.rect(screen, BLUE if retry_button_rect.collidepoint(mouse) else WHITE, retry_button_rect)

        retry_text_rect = retry.get_rect(center=retry_button_rect.center)  # Centering the text
        screen.blit(retry, retry_text_rect.topleft)  # Blit the text at the centered position

        if retry_button_rect.collidepoint(mouse) and click[0] == 1:
            if val == 1:
                longest_run, shortest_run, average_run = game_for_K2(10, 10, 2)
                runtime.append(longest_run)
            elif val == 2:
                longest_run, shortest_run, average_run = game_for_35(10, 10, 2)
                runtime.append(longest_run)
            elif val == 3:
                longest_run, shortest_run, average_run = game_for_68(10, 10, 2)
                runtime.append(longest_run)

        screen.blit(longest_text, (50, 150))
        screen.blit(shortest_text, (50, 250))
        screen.blit(average_text, (50, 350))
        pygame.display.flip()
        clock.tick(FPS)



def game_menu():
    global background
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(background, (0, 0))
        font = pygame.font.SysFont(None, 55)
        text_k2 = font.render("K-2", True, BLACK)
        text_35 = font.render("3-5", True, BLACK)
        text_68 = font.render("6-8", True, BLACK)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # K-2 button
        if 150 < mouse[0] < 350 and 100 < mouse[1] < 150:
            pygame.draw.rect(screen, TRANS, (150, 100, 200, 50))
            if click[0] == 1:
                ENABLED = True
                longest_run, shortest_run, average_run = game_for_K2(10, 10, 2)
                display_statistics(longest_run, shortest_run, average_run,1)
        else:
            pygame.draw.rect(screen, WHITE, (150, 100, 200, 50))
        screen.blit(text_k2, (225, 105))

        # 3-5 button
        if 150 < mouse[0] < 350 and 200 < mouse[1] < 250:
            pygame.draw.rect(screen, TRANS, (150, 200, 200, 50))
            if click[0] == 1:
                ENABLED = True
                longest_run, shortest_run, average_run = game_for_35(10, 10, 3)
                display_statistics(longest_run, shortest_run, average_run,2)
        else:
            pygame.draw.rect(screen, WHITE, (150, 200, 200, 50))
        screen.blit(text_35, (215, 205))

        # 6-8 button
        if 150 < mouse[0] < 350 and 300 < mouse[1] < 350:
            pygame.draw.rect(screen, TRANS, (150, 300, 200, 50))
            if click[0] == 1:
               ENABLED = True
               longest_run, shortest_run, average_run = game_for_68(10, 10, 4)
               display_statistics(longest_run, shortest_run, average_run,3)
        else:
            pygame.draw.rect(screen, WHITE, (150, 300, 200, 50))
        screen.blit(text_68, (215, 305))

        pygame.display.update()
        clock.tick(FPS)


game_menu()