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
    pygame.display.update()

def startup():
    global client
    msg = conn.recv()
    while msg != 'server-client':
        pass
    client = Client(('localhost', 1234))
    client.send('client-server')

startup()

while True:


    msg_tosend = [[],[],[]]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            msg_tosend[2].append('QUIT')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                msg_tosend[0].append('UP')
            elif event.key == pygame.K_DOWN:
                msg_tosend[0].append('DOWN')
            elif event.key == pygame.K_w:
                msg_tosend[0].append('W')
            elif event.key == pygame.K_s:
                msg_tosend[0].append('S')
            elif event.key == pygame.K_p:
                msg_tosend[0].append('P')
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                msg_tosend[1].append('UP')
            elif event.key == pygame.K_DOWN:
                msg_tosend[1].append('DOWN')
            elif event.key == pygame.K_w:
                msg_tosend[1].append('W')
            elif event.key == pygame.K_s:
                msg_tosend[1].append('S')
    print(msg_tosend)
    client.send(msg_tosend)
    matriz = conn.recv()
    # Si el mensaje recibido es la palabra close se cierra la aplicacion
    if matriz == "close":
        break
    screen(matriz)


print("Adios.")
