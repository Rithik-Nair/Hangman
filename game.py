import pygame
import sys
import random

pygame.init()
clock = pygame.time.Clock()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hangman Game")
background_img = pygame.image.load("assets/bg.jpg")
background_img = pygame.transform.scale(background_img, (width, height))
background_img.set_alpha(220)  # Makes the background slightly transparent

font = pygame.font.SysFont("comicsans", 30)
game_font = pygame.font.SysFont("comicsans", 80)
letter_font = pygame.font.SysFont("comicsans", 60)

words = ['PYGAME', 'PYTHON', 'JAVA', 'HELLO', 'WORLD', 'HANGMAN', 'TIME', 'RANDOM']
background_color = (240, 248, 255)
button_color = (173, 216, 230)
text_color = (255, 255, 255)

def draw_hangman(status):
    pygame.draw.line(screen, (255,255,255), (150, 450), (450, 450), 5)
    pygame.draw.line(screen, (255,255,255), (250, 450), (250, 100), 5)
    pygame.draw.line(screen, (255,255,255), (250, 100), (400, 100), 5)
    pygame.draw.line(screen, (255,255,255), (400, 100), (400, 150), 5)
    if status >= 1: pygame.draw.circle(screen, (255,255,255), (400, 180), 30, 5)
    if status >= 2: pygame.draw.line(screen, (255,255,255), (400, 210), (400, 300), 5)
    if status >= 3: pygame.draw.line(screen, (255,255,255), (400, 240), (350, 280), 5)
    if status >= 4: pygame.draw.line(screen, (255,255,255), (400, 240), (450, 280), 5)
    if status >= 5: pygame.draw.line(screen, (255,255,255), (400, 300), (350, 350), 5)
    if status >= 6: pygame.draw.line(screen, (255,255,255), (400, 300), (450, 350), 5)

def draw_buttons(buttons):
    for box, letter in buttons:
        pygame.draw.rect(screen, button_color, box)
        pygame.draw.rect(screen, (0, 0, 0), box, 2)
        btn_text = font.render(letter, True, text_color)
        btn_rect = btn_text.get_rect(center=(box.x + 20, box.y + 20))
        screen.blit(btn_text, btn_rect)

def display_guess(word, guessed):
    display_text = ''
    for letter in word:
        if letter in guessed:
            display_text += letter + ' '
        else:
            display_text += '_ '
    text = letter_font.render(display_text.strip(), True, (20, 20, 20))
    screen.blit(text, (400 - text.get_width() // 2, 500))

def welcome_screen():
    while True:
        screen.blit(background_img, (0, 0))
        title = game_font.render("Welcome to Hangman", True, text_color)
        instruct = font.render("Press R for Random Word or C to Choose Word", True, text_color)
        screen.blit(title, (width//2 - title.get_width()//2, 200))
        screen.blit(instruct, (width//2 - instruct.get_width()//2, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return random.choice(words)
                elif event.key == pygame.K_c:
                    return custom_word_input()

def custom_word_input():
    user_input = ''
    typing = True
    while typing:
        screen.fill(background_color)
        prompt = font.render("Enter your secret word:", True, (0,0,0))
        typed = font.render("*" * len(user_input), True, (0,0,0))
        screen.blit(prompt, (width//2 - prompt.get_width()//2, 300))
        screen.blit(typed, (width//2 - typed.get_width()//2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and user_input:
                    return user_input.upper()
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.unicode.isalpha():
                    user_input += event.unicode

def end_screen(message):
    while True:
        screen.fill(background_color)
        msg = game_font.render(message, True, (255, 0, 0) if message == "You Lost!" else (0, 128, 0))
        again = font.render("Press Enter to play again or ESC to quit", True, (0, 128, 0))
        screen.blit(msg, (width//2 - msg.get_width()//2, 300))
        screen.blit(again, (width//2 - again.get_width()//2, 400))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(), sys.exit()

def main():
    word = welcome_screen()
    guessed = []
    hangman_status = 0

    # Setup letter buttons
    buttons = []
    A = 65
    size = 40
    gap = 20
    for i in range(26):
        x = (i % 13) * (size + gap) + 20
        y = 600 + (i // 13) * (size + gap)
        box = pygame.Rect(x, y, size, size)
        buttons.append([box, chr(A + i)])

    running = True
    while running:
        screen.blit(background_img, (0, 0))
        draw_hangman(hangman_status)
        draw_buttons(buttons)
        display_guess(word, guessed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for button, letter in buttons[:]:
                    if button.collidepoint(pos) and letter not in guessed:
                        guessed.append(letter)
                        if letter not in word:
                            hangman_status += 1
                        buttons.remove([button, letter])

        won = all(letter in guessed for letter in word)
        if won:
            end_screen("You Won!")
        if hangman_status == 6:
            end_screen("You Lost!")

        pygame.display.update()
        clock.tick(60)

main()
