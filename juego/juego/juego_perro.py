import pygame
import random

pygame.init()

# Obtener resolución de la pantalla
info = pygame.display.Info()
ancho_pantalla = info.current_w
alto_pantalla = info.current_h

#Definir colores
negro = (0, 0, 0)
gris = (127, 127, 127)
blanco = (255, 255, 255)
rojo = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)

#Tamaño de la ventana
tamano = (800, 800)

#Controla los frames del videojuego
reloj = pygame.time.Clock()
reloj2 = pygame.time.Clock()

coor_list = []
for i in range(60):
	x = random.randint (0, ancho_pantalla)
	y = random.randint (0, alto_pantalla)
	coor_list.append ( [x, y] )


#Crear ventana
screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("ENTRE MUNDOS")

#Coordenadas del cuadrado
cord_x = ancho_pantalla //2
cord_y = alto_pantalla //2

#Velocidad de animacion del cuadrado
velo_x = 3
velo_y = 3

#ocultar puntero
pygame.mouse.set_visible(0)

#imagen de fondo
fondo = pygame.image.load("fondo.png").convert()
fondo = pygame.transform.scale(fondo, (ancho_pantalla, alto_pantalla))

#Estilo del mouse
player = pygame.image.load("player.png").convert()
player.set_colorkey([0,0,0])
player = pygame.transform.scale(player, (50, 50))

#Estilo enemigo
bacteria = pygame.image.load("bact.png").convert()
bacteria.set_colorkey([255,255,255])
bacteria = pygame.transform.scale(bacteria, (90, 90))

bacteria_list = []

for r in range(3):
	bacteria_rect_x = random.randrange(ancho_pantalla)
	bacteria_rect_y = random.randrange(alto_pantalla)
	rect = bacteria_img.get_rect()
	rect.x = bacteria_rect_x
	rect.y = bacteria_rect_y
	bacteria_list.append({"image": bacteria_img, "rect": rect})


running = True
while running:
	#Funcion para cerrar ventana
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		#print (event)

	#------Logica del videojuego
	if (cord_x + 80 >= ancho_pantalla or cord_x <= 0):
		velo_x *= -1


	if (cord_y + 80 >= alto_pantalla or cord_y <= 0):
		velo_y *= -1

	cord_x += velo_x
	cord_y += velo_y




	mouse_pos = pygame.mouse.get_pos()
	mouse_x = mouse_pos[0]
	mouse_y = mouse_pos[1]
	print (mouse_pos)
	#------Final de la logica



	screen.blit(fondo, [0,0])
	#-----------Inicia la zona para poder dibujar
	for coord in coor_list:
		pygame.draw.circle(screen, verde, coord, 2)
		coord[1] += 1
		if coord[1] > 500:
			coord[1] = 0

						#screen.blit(bacteria, [cord_x, cord_y])
	all_sprite_list.draw(screen)

	screen.blit(player, [mouse_x, mouse_y])
	#-----------Finaliza la zona para poder dibujar
	pygame.display.flip()
	reloj.tick(30)
pygame.quit()
