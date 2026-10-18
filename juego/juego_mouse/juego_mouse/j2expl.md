import pygame  # Importa la biblioteca pygame para desarrollo de videojuegos
import random  # Importa random para generar valores aleatorios

pygame.init()  # Inicializa todos los módulos de pygame

# Obtener resolución de pantalla
info = pygame.display.Info()  # Obtiene información del sistema de video
ancho_pantalla = info.current_w  # Almacena el ancho actual de la pantalla
alto_pantalla = info.current_h  # Almacena la altura actual de la pantalla

# Definir colores en formato RGB
negro = (0, 0, 0)  # Negro puro
gris = (127, 127, 127)  # Gris medio
blanco = (255, 255, 255)  # Blanco puro
rojo = (255, 0, 0)  # Rojo puro
verde = (0, 255, 0)  # Verde puro
azul = (0, 0, 255)  # Azul puro

# Control de frames por segundo (FPS)
reloj = pygame.time.Clock()  # Crea un reloj para controlar la tasa de actualización

# Crear ventana a pantalla completa con la resolución obtenida
screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("ENTRE MUNDOS")  # Título de la ventana

# Ocultar el cursor del mouse
pygame.mouse.set_visible(0)

# Cargar imagen de fondo y escalarla al tamaño de la pantalla
fondo = pygame.image.load("fondo.png").convert()
fondo = pygame.transform.scale(fondo, (ancho_pantalla, alto_pantalla))

# Cargar y configurar imagen del jugador
player = pygame.image.load("player.png").convert()
player.set_colorkey([0, 0, 0])  # Define el color negro como transparente
player = pygame.transform.scale(player, (50, 50))  # Escala la imagen

# Cargar y configurar imagen de bacteria enemiga
bacteria_img = pygame.image.load("bact.png").convert()
bacteria_img.set_colorkey([255, 255, 255])  # Define blanco como color transparente
bacteria_img = pygame.transform.scale(bacteria_img, (90, 90))

# Crear lista de bacterias con posiciones y velocidades aleatorias
bacteria_list = []
for _ in range(3):  # Crea tres bacterias iniciales
    x = random.randrange(ancho_pantalla)
    y = random.randrange(alto_pantalla)
    rect = bacteria_img.get_rect()  # Obtiene el rectángulo de colisión
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

# Crear lista de partículas verdes simulando efecto visual
coor_list = []
for _ in range(60):
    x = random.randint(0, ancho_pantalla)
    y = random.randint(0, alto_pantalla)
    coor_list.append([x, y])

# Inicializar coordenadas y velocidades del cuadro opcional
cord_x = ancho_pantalla // 2
cord_y = alto_pantalla // 2
velo_x = 3
velo_y = 3

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Cierra el juego si se cierra la ventana

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos_click = pygame.mouse.get_pos()  # Obtiene la posición del clic

            for i, bact in enumerate(bacteria_list):
                if bact["rect"].collidepoint(pos_click):  # Detecta colisión con bacteria
                    del bacteria_list[i]  # Elimina la bacteria

                    # Genera nueva bacteria en posición aleatoria
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
                    break  # Rompe el bucle tras procesar el clic

    # Movimiento del cuadro animado opcional y detección de colisiones con bordes
    if (cord_x + 80 >= ancho_pantalla or cord_x <= 0):
        velo_x *= -1
    if (cord_y + 80 >= alto_pantalla or cord_y <= 0):
        velo_y *= -1

    cord_x += velo_x
    cord_y += velo_y

    # Posición del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Movimiento y rebote de bacterias contra los bordes de la pantalla
    for bact in bacteria_list:
        bact["rect"].x += bact["vel_x"]
        bact["rect"].y += bact["vel_y"]
        if bact["rect"].right >= ancho_pantalla or bact["rect"].left <= 0:
            bact["vel_x"] *= -1
        if bact["rect"].bottom >= alto_pantalla or bact["rect"].top <= 0:
            bact["vel_y"] *= -1

    # Dibujar imagen de fondo
    screen.blit(fondo, [0, 0])

    # Dibujar partículas verdes descendentes
    for coord in coor_list:
        pygame.draw.circle(screen, verde, coord, 2)
        coord[1] += 1
        if coord[1] > alto_pantalla:
            coord[1] = 0  # Reinicia partícula al llegar al fondo

    # Dibujar todas las bacterias en pantalla
    for bact in bacteria_list:
        screen.blit(bact["image"], bact["rect"])

    # Dibujar jugador controlado por mouse
    screen.blit(player, [mouse_x, mouse_y])

    # Actualizar pantalla con todos los elementos dibujados
    pygame.display.flip()
    reloj.tick(30)  # Limita el juego a 30 FPS

# Salir del juego correctamente
pygame.quit()
