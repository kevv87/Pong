import pygame
# importamos el modulo socket
import socket

# instanciamos un objeto para trabajar con el socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Con el metodo bind le indicamos que puerto debe escuchar y de que servidor esperar conexiones
# Es mejor dejarlo en blanco para recibir conexiones externas si es nuestro caso
s.bind(("", 9999))

# Aceptamos conexiones entrantes con el metodo listen, y ademas aplicamos como parametro
# El numero de conexiones entrantes que vamos a aceptar
s.listen(1)

# Instanciamos un objeto sc (socket cliente) para recibir datos, al recibir datos este
# devolvera tambien un objeto que representa una tupla con los datos de conexion: IP y puerto
sc, addr = s.accept()

pygame.init()
width = 800
height = 600
block_width = 20
block_height = 24
gameDisplay = pygame.display.set_mode((width, height))
white = (255, 255, 255)
black = (0, 0, 0)


# Convierte los valores verdaderos de la matriz a casillas en blanco en la pantalla
def screen(matrix):
    for n in range(len(matrix)):
        for m in range(len(matrix[n])):
            if matrix[n][m]:
                pygame.draw.rect(gameDisplay,white,[m*block_width, n*block_height,
                                                             block_width, block_height])
            else:
                pygame.draw.rect(gameDisplay, black, [m * block_width, n * block_height,
                                                               block_width, block_height])


while True:
    # Recibimos el mensaje, con el metodo recv recibimos datos y como parametro
    # la cantidad de bytes para recibir
    matriz = sc.recv(1024).decode()

    if not (isinstance(matriz, list) and isinstance(matriz[0], list)):
        print('Error')
        break

    # Si el mensaje recibido es la palabra close se cierra la aplicacion
    if matriz == "close":
        break
    screen(matriz)


print("Adios.")

# Cerramos la instancia del socket cliente y servidor
sc.close()
s.close()