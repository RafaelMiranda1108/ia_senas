import pygame
import random

pygame.init()

# Obtener resolución de pantalla
info = pygame.display.Info()
ancho_pantalla = info.current_w
alto_pantalla = info.current_h

# Definir colores
negro = (0, 0, 0)
gris = (127, 127, 127)
blanco = (255, 255, 255)
rojo = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)

# Control de FPS
reloj = pygame.time.Clock()

# Crear ventana a pantalla completa
screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("ENTRE MUNDOS")

# Ocultar puntero del mouse
pygame.mouse.set_visible(0)

# Cargar imagen de fondo
fondo = pygame.image.load("fondo.png").convert()
fondo = pygame.transform.scale(fondo, (ancho_pantalla, alto_pantalla))

# Cargar imagen del jugador
player = pygame.image.load("player.png").convert()
player.set_colorkey([0, 0, 0])
player = pygame.transform.scale(player, (50, 50))

# Cargar imagen de la bacteria
bacteria_img = pygame.image.load("bact.png").convert()
bacteria_img.set_colorkey([255, 255, 255])
bacteria_img = pygame.transform.scale(bacteria_img, (90, 90))

# Crear lista de bacterias con movimiento
bacteria_list = []
for _ in range(3):
    x = random.randrange(ancho_pantalla)
    y = random.randrange(alto_pantalla)
    rect = bacteria_img.get_rect()
    rect.x = x
    rect.y = y
    vel_x = random.choice([-2, -1, 1, 2])
    vel_y = random.choice([-2, -1, 1, 2])
    bacteria_list.append({
        "image": bacteria_img,
        "rect": rect,
        "vel_x": vel_x,
        "vel_y": vel_y
    })

# Lista de partículas verdes
coor_list = []
for _ in range(60):
    x = random.randint(0, ancho_pantalla)
    y = random.randint(0, alto_pantalla)
    coor_list.append([x, y])

# Coordenadas y velocidad del cuadro animado (opcional)
cord_x = ancho_pantalla // 2
cord_y = alto_pantalla // 2
velo_x = 3
velo_y = 3

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detectar clic con el mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_click = pygame.mouse.get_pos()

            for i, bact in enumerate(bacteria_list):
                if bact["rect"].collidepoint(pos_click):
                    # Eliminar bacteria clickeada
                    del bacteria_list[i]

                    # Crear nueva bacteria aleatoria
                    x = random.randrange(ancho_pantalla)
                    y = random.randrange(alto_pantalla)
                    rect = bacteria_img.get_rect()
                    rect.x = x
                    rect.y = y
                    vel_x = random.choice([-2, -1, 1, 2])
                    vel_y = random.choice([-2, -1, 1, 2])
                    bacteria_list.append({
                        "image": bacteria_img,
                        "rect": rect,
                        "vel_x": vel_x,
                        "vel_y": vel_y
                    })
                    break  # Importante: salir del bucle para evitar errores de índice

    # Movimiento del cuadro (opcional)
    if (cord_x + 80 >= ancho_pantalla or cord_x <= 0):
        velo_x *= -1
    if (cord_y + 80 >= alto_pantalla or cord_y <= 0):
        velo_y *= -1

    cord_x += velo_x
    cord_y += velo_y

    # Posición del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Movimiento y rebote de bacterias
    for bact in bacteria_list:
        bact["rect"].x += bact["vel_x"]
        bact["rect"].y += bact["vel_y"]
        if bact["rect"].right >= ancho_pantalla or bact["rect"].left <= 0:
            bact["vel_x"] *= -1
        if bact["rect"].bottom >= alto_pantalla or bact["rect"].top <= 0:
            bact["vel_y"] *= -1

    # Dibujar fondo
    screen.blit(fondo, [0, 0])

    # Dibujar partículas
    for coord in coor_list:
        pygame.draw.circle(screen, verde, coord, 2)
        coord[1] += 1
        if coord[1] > alto_pantalla:
            coord[1] = 0

    # Dibujar bacterias
    for bact in bacteria_list:
        screen.blit(bact["image"], bact["rect"])

    # Dibujar jugador
    screen.blit(player, [mouse_x, mouse_y])

    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
