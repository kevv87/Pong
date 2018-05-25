import pygame
from multiprocessing.connection import Listener, Client

pygame.init()
width = 800
height = 600
block_width = 20
block_height = 24
gameDisplay = pygame.display.set_mode((width, height))
white = (255, 255, 255)
black = (0, 0, 0)

client = Client(('localhost', 1234))
listen = Listener(('localhost', 1235))
conn = listen.accept()


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
    client.send(['hello', 'world'])
    matriz = conn.recv()

    # Si el mensaje recibido es la palabra close se cierra la aplicacion
    if matriz == "close":
        break
    screen(matriz)


print("Adios.")
