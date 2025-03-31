import os
import pygame
from random import choice, randrange

pygame.init()

WIDTH, HEIGHT = 1920, 1080
RES = (WIDTH, HEIGHT)
FONT_SIZE = 35
alpha_value = randrange(30, 40, 5)

fullscreen = False

# Ruta absoluta para la fuente
font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MS Mincho.ttf")

# Verificar que la fuente existe antes de usarla
if not os.path.exists(font_path):
    raise FileNotFoundError(f"No se encontró la fuente en: {font_path}")

# Cargar la fuente correctamente
font = pygame.font.Font(font_path, FONT_SIZE)
font_2 = pygame.font.Font(font_path, FONT_SIZE - FONT_SIZE // 6)
font_3 = pygame.font.Font(font_path, FONT_SIZE - FONT_SIZE // 3)

chars = ['ｦ', 'ｱ', 'ｳ', 'ｴ', 'ｵ', 'ｶ', 'ｷ', 'ｹ', 'ｺ', 'ｻ', 'ｼ', 'ｽ', 'ｾ', 'ｿ', 'ﾀ', 'ﾂ', 'ﾃ', 'ﾅ', 'ﾆ', 'ﾇ', 'ﾈ',
         'ﾊ', 'ﾋ', 'ﾎ', 'ﾏ', 'ﾐ', 'ﾑ', 'ﾒ', 'ﾓ', 'ﾔ', 'ﾕ', 'ﾗ', 'ﾘ', 'ﾜ', '9', '8', '7', '5', '2', '1', ':', '.',
         '"', '=', '*', '+', '-', '¦', '|', '_', '╌', '日', 'C', 'O', 'D', 'E', 'X', 'c', 'o', 'd', 'e', 'x']

# Generar caracteres con distintos tonos de verde
green_chars = [
    [font.render(char, True, (randrange(0, 100), 255, randrange(0, 100))) for char in chars],
    [font_2.render(char, True, (40, randrange(100, 175), 40)) for char in chars],
    [font_3.render(char, True, (40, randrange(50, 100), 40)) for char in chars]
]

# Renderizar "CODEDEX" en verde
codedex_chars = [font.render(char, True, (0, 255, 0)) for char in "CODEDEX"]

screen = pygame.display.set_mode(RES) # Para que arranque en pantalla completa, cambiar por:  (RES, pygame.FULLSCREEN)
display_surface = pygame.Surface(RES)
display_surface.set_alpha(alpha_value)

clock = pygame.time.Clock()

def toggle_fullscreen():
    global screen, fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(RES)

class Symbol:
    def __init__(self, x, y, layer):
        self.x, self.y, self.layer = x, y, layer
        self.speed = 40
        self.value = choice(green_chars[self.layer])

    def draw(self):
        self.value = choice(green_chars[self.layer])
        self.y = self.y + self.speed if self.y < HEIGHT else -FONT_SIZE * randrange(1, 10)
        screen.blit(self.value, (self.x, self.y))


class CodedexRain:
    def __init__(self, x):
        self.x = x  # Cada instancia tiene su propia columna
        self.y = randrange(-HEIGHT, 0)  # Comienza en una posición aleatoria arriba
        self.speed = 40
        self.index = 0  # Para recorrer "CODEDEX"

    def draw(self):
        # Dibujar cada letra en su posición correspondiente
        for i, char in enumerate(codedex_chars):
            screen.blit(char, (self.x, self.y + i * FONT_SIZE))

        # Mover la palabra hacia abajo
        self.y += self.speed / 35

        # Cuando la palabra completa haya salido de la pantalla, reiniciar posición
        if self.y >= HEIGHT:
            self.y = -FONT_SIZE * len(codedex_chars)  # Volver a aparecer arriba


# Generamos símbolos en distintas capas con diferentes tonos de verde
symbols = [
    Symbol(x, randrange(-HEIGHT, 0), i % 3)
    for i, x in enumerate(range(0, WIDTH, FONT_SIZE))
]

# Generamos múltiples columnas con "CODEDEX"
codedex_rains = [CodedexRain(x) for x in range(0, WIDTH, FONT_SIZE * 7)]

run = True
while run:
    screen.blit(display_surface, (0, 0))
    display_surface.fill(pygame.Color('black'))

    [symbol.draw() for symbol in symbols]
    [codedex.draw() for codedex in codedex_rains]  # Dibujar múltiples CODEDEX

    pygame.time.delay(140)
    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_F11:
                toggle_fullscreen()
