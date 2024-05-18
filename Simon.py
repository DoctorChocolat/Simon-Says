import pygame
import random

# Inicializar pygame
pygame.init()

# Configurar la pantalla
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simón Dice")

# Colores
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0)
DARK_RED = (100, 0, 0)
DARK_BLUE = (0, 0, 100)
DARK_YELLOW = (100, 100, 0)

# Colores para botones oscurecidos
DARK_COLORS = [DARK_GREEN, DARK_RED, DARK_YELLOW, DARK_BLUE]

# Definir las áreas de los botones
BUTTONS = [
    pygame.Rect(50, 50, 200, 200),    # Green
    pygame.Rect(350, 50, 200, 200),   # Red
    pygame.Rect(50, 350, 200, 200),   # Yellow
    pygame.Rect(350, 350, 200, 200)   # Blue
]

COLORS = [GREEN, RED, YELLOW, BLUE]
# SOUNDS = [pygame.mixer.Sound(f'sound{i}.wav') for i in range(1, 5)]  # Línea comentada

sequence = []
player_sequence = []
turn_to_play = False
score = 0

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 48)

def draw_buttons():
    for i, button in enumerate(BUTTONS):
        pygame.draw.rect(screen, DARK_COLORS[i], button)

def flash_button(index):
    color = COLORS[index]
    rect = BUTTONS[index]
    pygame.draw.rect(screen, color, rect)
    pygame.display.update()
    # SOUNDS[index].play()  # Línea comentada
    pygame.time.wait(500)
    pygame.draw.rect(screen, DARK_COLORS[index], rect)
    pygame.display.update()
    pygame.time.wait(300)

def play_sequence():
    for index in sequence:
        flash_button(index)
        pygame.time.wait(300)

def add_to_sequence():
    sequence.append(random.randint(0, 3))

def reset_game():
    global sequence, player_sequence, turn_to_play, score
    sequence = []
    player_sequence = []
    turn_to_play = False
    score = 0
    add_to_sequence()
    show_message("Mira esta secuencia...", 2000)
    play_sequence()
    show_message("Ahora repite tú...", 2000)
    turn_to_play = True

def show_message(message, duration=2000):
    screen.fill(BLACK)
    draw_buttons()
    text = big_font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(duration)

def show_instructions():
    instructions = [
        "Bienvenido a Simón Dice!",
        "Instrucciones:",
        "1. Mira la secuencia de colores.",
        "2. Repite la secuencia haciendo clic",
        "en los botones correspondientes.",
        "3. Cada ronda correcta aumenta tu puntuación.",
        "4. Si fallas, el juego se reinicia.",
        "",
        "Haz clic para comenzar..."
    ]
    screen.fill(BLACK)
    y_offset = 50
    for line in instructions:
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, y_offset))
        screen.blit(text, text_rect)
        y_offset += 40
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

show_instructions()
reset_game()

running = True
while running:
    screen.fill(BLACK)
    draw_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and turn_to_play:
            for i, button in enumerate(BUTTONS):
                if button.collidepoint(event.pos):
                    player_sequence.append(i)
                    flash_button(i)
                    if player_sequence[-1] != sequence[len(player_sequence) - 1]:
                        show_message("Fallo! Reiniciando...", 2000)
                        reset_game()
                    elif len(player_sequence) == len(sequence):
                        score += 1
                        turn_to_play = False
                        player_sequence = []
                        add_to_sequence()
                        show_message(f"Puntuación: {score}", 2000)
                        pygame.time.wait(1000)
                        show_message("Mira esta secuencia...", 2000)
                        play_sequence()
                        show_message("Ahora repite tú...", 2000)
                        turn_to_play = True

    if turn_to_play and len(player_sequence) < len(sequence):
        # Permitir tiempo adicional para que el jugador repita la secuencia
        pygame.time.wait(1000)

    score_text = font.render(f"Puntuación: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

pygame.quit()
