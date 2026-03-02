import pygame
import random
import sys

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

def menu():
    opciones = ["Jugar", "Salir"]
    seleccion = 0
    fuente = pygame.font.SysFont("Arial", 50)

    while True:
        pantalla.fill(NEGRO)
        #Dibujar las opciones
        for i, opcion in enumerate(opciones):
            color = BLANCO if i == seleccion else (100, 100, 100)
            texto = fuente.render(opcion, True, color)
            texto_rect = texto.get_rect(center=(ANCHO/2, ALTO/2 + i*60))
            pantalla.blit(texto, texto_rect)

        pygame.display.update()

        #Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif event.key == pygame.K_RETURN:
                    if seleccion == 0:
                        return "jugar"
                    else:
                        return "salir"
                    
        reloj.tick(10)  #Controlar los FPS del menú

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
                pygame.quit()
                sys.exit()                
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
        if cabeza in serpiente[1:]:
            game_over = True
            
        #Dibujar
        pantalla.fill((NEGRO))
        pygame.draw.rect(pantalla, ROJO, [comida_x, comida_y, CELDA, CELDA])
        dibujar_serpiente(serpiente)
        mostrar_puntuacion(largo_serpiente - 1)

        pygame.display.update()
        reloj.tick(velocidad)
    
    #===============================================
    #Selección después del juego: opciones al perder
    #===============================================
    while True:
        #Se dibuja de nuevo el estado final
        pantalla.fill(NEGRO)
        pygame.draw.rect(pantalla, ROJO, [comida_x, comida_y, CELDA, CELDA])
        dibujar_serpiente(serpiente)
        mostrar_puntuacion(largo_serpiente - 1)

        #Mensaje de Game Over
        fuente = pygame.font.SysFont("Arial", 30)
        texto = fuente.render("Game Over - R: Reiniciar M: Menú", True, BLANCO)
        texto_rect = texto.get_rect(center=(ANCHO/2, ALTO/2))
        pantalla.blit(texto, texto_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "reiniciar"
                elif event.key == pygame.K_m:
                    return "menu"
                
        reloj.tick(10) # Pausa para no saturar la compu

if __name__ == "__main__":
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Juego de la Serpiente - Esteban RT")
    reloj = pygame.time.Clock()

    while True:
        opcion = menu()
        if opcion == "jugar":
            resultado = game_loop()
            #Si el jugador elige reiniciar, volvemos a llamar a game_loop directamente
            while resultado == "reiniciar":
                resultado = game_loop()
            #Si elige menu, solo se sale de este if y vuelve al menú principal
        elif opcion == "salir":
            break

    pygame.quit()
    sys.exit()
