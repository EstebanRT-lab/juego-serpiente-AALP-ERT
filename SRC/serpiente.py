import pygame
import random

#Inicializar Pygame
pygame.init()

#Dimensiones de la ventana
ANCHO = 600
ALTO = 400

#Tamaño de cada celda (la serpiente y la comda serán cuadrados de este tamaño)
CELDA = 20

#Colores (RGB)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)         #color de la serpiente
ROJO = (255, 0, 0)          #color de la comida
AZUL = (0, 0, 255)          #color del texto

#Ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de la Serpiente")

#Reloj para controlar los FPS (frames por segundo)
reloj = pygame.time.Clock()

#Velocidad inicial (FPS)
velocidad = 10

def dibujar_serpiente(lista_serpiente):
    for segmento in lista_serpiente:
        pygame.draw.rect(pantalla, VERDE, [segmento[0], segmento[1], CELDA, CELDA])

def mostrar_puntuacion(puntuacion):
    fuente = pygame.font.SysFont("Arial", 25)
    texto = fuente.render(f"puntuación: {puntuacion}", True, BLANCO)
    pantalla.blit(texto, [0, 0])

def game_loop():
    game_over = False
    game_cerrado = False

    #Posición inicial
    x = ANCHO // 2
    y = ALTO // 2
    dx = CELDA
    dy = 0

    serpiente = []
    largo_serpiente = 1

    #Comida
    comida_x = round(random.randrange (0, ANCHO - CELDA) / CELDA) * CELDA
    comida_y = round(random.randrange(0, ALTO - CELDA) / CELDA) * CELDA

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_cerrado = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -CELDA
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = CELDA
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -CELDA
                    dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = CELDA
                    dx = 0

        #Mover cabeza
        x += dx
        y += dy

        #Bordes tablero
        if x < 0 or x >= ANCHO or y < 0 or y >= ALTO:
            game_over = True
            
        cabeza = [x, y]
        serpiente.insert(0, cabeza)

        if len(serpiente) > largo_serpiente:
            serpiente.pop()
            
        #Comida
        if x == comida_x and y == comida_y:
            largo_serpiente += 1
            comida_generada = False
            while not comida_generada:
                comida_x = round(random.randrange(0, ANCHO - CELDA) / CELDA) * CELDA
                comida_y = round(random.randrange(0, ALTO - CELDA) / CELDA) * CELDA
                if [comida_x, comida_y] not in serpiente:
                    comida_generada = True

        #Colisión con cuerpo
        if cabeza in serpiente[1:0]:
            game_over = True
            
        #Dibujar
        pantalla.fill((NEGRO))
        pygame.draw.rect(pantalla, ROJO, [comida_x, comida_y, CELDA, CELDA])
        dibujar_serpiente(serpiente)
        mostrar_puntuacion(largo_serpiente - 1)

        pygame.display.update()
        reloj.tick(velocidad)
    #Fin del juego
    if not game_cerrado:
        pygame.time.wait(2000)
    pygame.quit()
    quit()

if __name__ == "__main__":
    game_loop()