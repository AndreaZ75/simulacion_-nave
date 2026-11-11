import pygame 
import sys 
import math 

"""pygame.init()
print("pygame instalado correctamente")
print(pygame.version.ver)

pygame.quit() """

pygame.init()
print("Pygame inicio exitosamente")
print("Version de Pygame: " + pygame.version.ver)

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulación de Nave Espacial 2D")
reloj = pygame.time.Clock()

def transformar_vertice(vertice, posx, posy, escala, angulo):
    x, y = vertice
    # Aplicar escala
    x_esc = x * escala
    y_esc = y * escala
    # Aplicar rotación
    rad = math.radians(angulo)
    x_rot = x_esc * math.cos(rad) - y_esc * math.sin(rad)
    y_rot = x_esc * math.sin(rad) + y_esc * math.cos(rad)
    # Aplicar traslación
    x_final = x_rot + posx
    y_final = y_rot + posy
    return (x_final, y_final)

# Modelo local de la nave con la proa (punta) ubicada estrictamente en (0, -25)
modelo_triangulo = [(0, -25), (-15, 15), (15, 15)] 

# Variables de posición inicial y transformación
posx, posy = 400, 300
escala = 1.0
angulo = 0

# Configuración de velocidad y físicas de la nave
VELOCIDAD_NAVE = 250
VELOCIDAD_ROTACION = 200
VELOCIDAD_ESCALA = 1.5

# Configuración de los proyectiles
VELOCIDAD_BALA = 500
color_bala = (255, 50, 50)
balas = []
cooldown_disparo = 250  # Cooldown en milisegundos (250 ms)
ultimo_disparo = 0

# Configuración de límites y colores
ESCALA_MINIMA, ESCALA_MAXIMA = 0.5, 3.0
COLOR_FONDO = (18, 18, 28)
COLOR_TRIANGULO = (171, 43, 217)  # Color principal acorde al estilo visual
fuente = pygame.font.Font(None, 24)

# Bucle principal del juego (60 FPS con Double Buffering)
ejecutando = True
while ejecutando:
    dt = reloj.tick(60) / 1000
    tiempo_actual = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
            elif evento.key == pygame.K_SPACE:
                # Generación dinámica de proyectiles con cooldown de 250 ms
                if tiempo_actual - ultimo_disparo >= cooldown_disparo:
                    # Calcular la posición exacta de la punta de la nave
                    punta = transformar_vertice((0, -25), posx, posy, escala, angulo)
                    rad = math.radians(angulo)
                    # Velocidades vectoriales independientes para el proyectil
                    vx = VELOCIDAD_BALA * math.sin(rad)
                    vy = -VELOCIDAD_BALA * math.cos(rad)
                    # Estructura del proyectil: [x, y, vx, vy, tiempo_de_vida]
                    balas.append([punta[0], punta[1], vx, vy, 4.0])
                    ultimo_disparo = tiempo_actual

    # Controles del teclado para rotación y avance vectorial
    teclas = pygame.key.get_pressed()
    
    # Rotación geométrica suave con A / D o Flechas Izquierda / Derecha
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        angulo -= VELOCIDAD_ROTACION * dt
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        angulo += VELOCIDAD_ROTACION * dt
        
    # Avance vectorial continuo con W o Flecha Arriba usando trigonometría 
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        rad = math.radians(angulo)
        posx += VELOCIDAD_NAVE * dt * math.sin(rad)
        posy -= VELOCIDAD_NAVE * dt * math.cos(rad)

    # Control de escala con las teclas de más / menos
    if teclas[pygame.K_EQUALS] or teclas[pygame.K_KP_PLUS]:
        escala += VELOCIDAD_ESCALA * dt
    if teclas[pygame.K_MINUS] or teclas[pygame.K_KP_MINUS]:
        escala -= VELOCIDAD_ESCALA * dt

    escala = max(ESCALA_MINIMA, min(ESCALA_MAXIMA, escala))

    # Reto Opcional 
    if posx < 0:
        posx = ANCHO
    elif posx > ANCHO:
        posx = 0
    if posy < 0:
        posy = ALTO
    elif posy > ALTO:
        posy = 0

    # Gestión de memoria y actualización del ciclo de vida de los proyectiles
    for bala in balas[:]:
        bala[0] += bala[2] * dt
        bala[1] += bala[3] * dt
        bala[4] -= dt  # Reducir contador de vida
        
        # Eliminar automáticamente si sale de los bordes o agota su tiempo de vida
        if (bala[0] < 0 or bala[0] > ANCHO or bala[1] < 0 or bala[1] > ALTO or bala[4] <= 0):
            balas.remove(bala)

    # Transformación de los vértices del modelo local al espacio de pantalla
    vertices = [
        transformar_vertice(vertice, posx, posy, escala, angulo)
        for vertice in modelo_triangulo
    ]
    vertices = [(round(x), round(y)) for x, y in vertices]

    # Renderizado y doble búfer
    pantalla.fill(COLOR_FONDO)
    
    # Dibujar proyectiles dinámicos
    for bala in balas:
        pygame.draw.circle(pantalla, color_bala, (round(bala[0]), round(bala[1])), 3)

    # Dibujar la nave espacial vectorial
    pygame.draw.polygon(pantalla, COLOR_TRIANGULO, vertices)
    pygame.draw.polygon(pantalla, (220, 255, 240), vertices, 2)

    # Renderizar instrucciones de uso en pantalla
    instrucciones = fuente.render(
        "Girar: A/D | Avanzar: W | Disparar: ESPACIO | Escala: +/- | Salir: ESC",
        True,
        (230, 230, 240),
    )
    pantalla.blit(instrucciones, (12, ALTO - 30))
    pygame.display.flip()

pygame.quit()
sys.exit()

"""#1. inicializar pygame
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode(ANCHO, ALTO)
pygame.display.set_caption("Graficacion 2D - Actividad en aula")
reloj = pygame.time.Clock()

#2 funcion de transformacion geometrica 2D
def transformar(vertice, pos_x, por_y, escala, angulo):
    x, y = vertice 
    #escalamiento
    x_esc, y_esc = x * escala, y * escala 
    #rotacion (matematica continua)
    rad = math.radians(angulo)
    x_rot = x_esc * math.cos(rad) - y_esc * math.sin(rad) 
    y_rot = x_esc * math.sin(rad) + y_esc * math.cos(rad) 
    #traslacion (al sistema de coordenadas de la pantalla)
    return(x_rot + pos_x, y_rot + por_y)

#modelo local del triangulo
modelo_triangulo = [(0, -30), (-20,20), (20,20)]

#variables de posicion y rotacion
pos_x, pos_y = 400,300
angulo=0
escala = 1.5

#3. bucle principal de renderizado
ejecutando = True 
while ejecutando:
    pantalla.fill((25,25,35)) #fondo oscuro 

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False 

    #controles por teclado
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: angulo -=4 #flecha izquierda: rotar
    if teclas[pygame.K_RIGHT]: angulo +=4 #flecha derecha: rotar
    if teclas[pygame.K_w]: por_y -=4 #tecla w: arriba
    if teclas[pygame.K_s]: por_y +=4 #tecla s: abajo
    if teclas[pygame.K_a]: por_x -=4 #tecla a: mover izq
    if teclas[pygame.K_d]: por_x +=4 #tecla d: der

    #transformar vertices
    vertices_pantalla = [
        transformar_vertice(v, pos_x, pos_y, escala, angulo)
        for v in modelo_triangulo 
    ]

    #renderizar poligono en el lienzo
    pygame.draw.polygon(pantalla, (50,255,150), vertices_pantalla, 2)

    pygame. display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()"""