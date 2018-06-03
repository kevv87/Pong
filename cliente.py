import pygame
from multiprocessing.connection import Listener, Client
import sys

port = int(sys.argv[1])
server_ip = str(sys.argv[2])
print(port)

pygame.init()
width = 800
height = 600
block_width = 20
block_height = 24
gameDisplay = pygame.display.set_mode((width, height))
white = (255, 255, 255)
black = (0, 0, 0)

# Fuentes predeterminadas
smallfont = pygame.font.SysFont('couriernew', 25)
mediumfont = pygame.font.SysFont('couriernew',50)
largefont = pygame.font.SysFont('couriernew', 80)

listen = Listener(('', port))
conn = listen.accept()

setups = [] # indice 0 es numero de jugador


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

# Funcion encargada de renderizar el texto a poner en la pantalla, recibe un texto, un color y un tamanno y retorna
# el texto renderizado asi como el punto central del mismo.
def text_objects(text, color, size):
    if size == 'small':
        textSurface = smallfont.render(text, True, color)
    if size == 'medium':
        textSurface = mediumfont.render(text, True, color)
    elif size == 'large':
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

    # Dado un mensaje, un color, un desplazamiento del centro de la pantalla en x, un desplazamiento del centor de la pantalla
    # en y y un tamanno de los ya predeterminados, este funcion muestra un texto en la pantalla.
def message_to_screen(msg, color,x_displace=0, y_displace=0, size='small'):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (width/2) + x_displace, (height/2) + y_displace
    gameDisplay.blit(textSurf, textRect)

def startup():
    global server_ip
    global client
    global setups
    msg, port = conn.recv()

    while msg != 'server-client':
        pass
    client = Client((server_ip, int(port)))
    client.send('client-server')
    setups = conn.recv()


def pause():
    global setups
    cmd = 'pause'
    msg_tosend = [[],[],[]]
    while cmd != 'unpause':
        #pygame.mixer.music.pause()
        message_to_screen('Juego pausado', white, size='large')
        message_to_screen('Presione p para reanudar', white, y_displace=80)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    #pygame.mixer.music.unpause()
                    msg_tosend[2].append('P')
            elif event.type == pygame.QUIT:
                quit()

        pygame.display.update()
        client.send(msg_tosend)
        cmd = conn.recv()
    print('Unpause')

startup()

while True:

    msg_tosend = [[],[],[]]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            msg_tosend[2].append('QUIT')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and setups[0] == 1:
                msg_tosend[0].append('UP')
            elif event.key == pygame.K_DOWN and setups[0] == 1:
                msg_tosend[0].append('DOWN')
            elif event.key == pygame.K_w and setups[0] == 2:
                msg_tosend[0].append('W')
            elif event.key == pygame.K_s and setups[0] == 2:
                msg_tosend[0].append('S')
            elif event.key == pygame.K_p:
                msg_tosend[0].append('P')
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and setups[0] == 1:
                msg_tosend[1].append('UP')
            elif event.key == pygame.K_DOWN and setups[0] == 1:
                msg_tosend[1].append('DOWN')
            elif event.key == pygame.K_w and setups[0] == 2:
                msg_tosend[1].append('W')
            elif event.key == pygame.K_s and setups[0] == 2:
                msg_tosend[1].append('S')
    print(msg_tosend)
    client.send(msg_tosend)
    matriz = conn.recv()
    # Si el mensaje recibido es la palabra close se cierra la aplicacion
    if matriz == "close":
        break
    elif matriz == 'pause':
        pause()
    elif isinstance(matriz, list) and isinstance(matriz[0], list):
        screen(matriz)
    elif matriz == 'sincronize':
        client.send('sincronize')
        sinc = conn.recv()
        while sinc != 'sincronize':
            sinc = conn.recv()



