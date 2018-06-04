import pygame
import random
import mutagen.oggvorbis
import time
import sys
import os
import pyfirmata
from multiprocessing.connection import Client, Listener
from tkinter import *


os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()


# Colores importantes
white = (255, 255, 255)
black = (0, 0, 0)

# Sonidos
select_sound = pygame.mixer.Sound('sounds/select.ogg')
pong_sound = pygame.mixer.Sound('sounds/pong.ogg')
ping_sound = pygame.mixer.Sound('sounds/ping.ogg')
point_sound = pygame.mixer.Sound('sounds/point.ogg')
fail_sound = pygame.mixer.Sound('sounds/fail.ogg')

pausa=False

# Colores importantes
white = (255, 255, 255)
black = (0, 0, 0)
green = (0,255,0)


# Fuentes predeterminadas
smallfont = pygame.font.SysFont('couriernew', 25)
mediumfont = pygame.font.SysFont('couriernew',50)
largefont = pygame.font.SysFont('couriernew', 80)

# Dimensiones de cada casilla de la matriz
block_height = 20
block_width = 24

# Reloj
clock = pygame.time.Clock()


# Clase tablero, encargada de guardar algunas variables importantes para el desarrollo de cualquier modalidad del juego
# asi como metodos que se usan en todas las modalidades del juego.

class Tablero:
    def __init__(self, PC, block_width, block_height, MUTE,PT, color):
        # Atributos

        self.mute = MUTE

        self.width = 800
        self.height = 600
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.game_matrix = [[]]
        self.matrix_constructor()
        self.enemy_score = 0
        self.friend_score = 0
        self.scores()
        self.block_width = block_width
        self.block_height = block_height
        self.level = 2
        self.ball_velocity = 30 + 3*(self.level-1)
        self.ball_direction = (-1, 0)
        self.pc = PC
        self.practice = PT
        self.current_color = color
        self.paleta_length = 9 - (3*(self.level-1))
        if not self.practice:
            self.paleta_length_e = self.paleta_length
        else:
            self.paleta_length_e = 37
        self.lvl_music()

    # Metodos

    # Constructor de la matriz
    def matrix_constructor(self):
        for n in range(25):
            self.game_matrix.append([])
            for m in range(40):
                self.game_matrix[n].append(False)
        self.game_matrix = self.game_matrix[:len(self.game_matrix)-1]


    # Musica
    def lvl_music(self):

        global pong_sound
        global fail_sound
        global point_sound
        global ping_sound
        if self.mute == True:
            music_file = 'sounds/blank.ogg'
            pong_sound = pygame.mixer.Sound('sounds/blank.ogg')
            ping_sound = pygame.mixer.Sound('sounds/blank.ogg')
            point_sound = pygame.mixer.Sound('sounds/blank.ogg')
            fail_sound = pygame.mixer.Sound('sounds/blank.ogg')
        elif self.level == 1:
            music_file = 'sounds/lvl1.ogg'
        elif self.level == 2:
            music_file = 'sounds/lvl2.ogg'
        elif self.level == 3:
            music_file = 'sounds/NDY.ogg'
        sample_rate = mutagen.oggvorbis.OggVorbis(music_file).info.sample_rate
        pygame.mixer.quit()
        pygame.mixer.pre_init(sample_rate, -16, 1, 512)
        pygame.mixer.init()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)

    # Metodos set y get
    def get_matrix(self):
        return self.game_matrix

    def set_matrix(self, new_matrix):
        if not (isinstance(new_matrix, list) and isinstance(new_matrix[0], list) and len(new_matrix) == 25 and len(new_matrix[0]) == 40):
            return 'Error'
        self.game_matrix = new_matrix

    def get_ball_direction(self):
        return self.ball_direction

    def set_ball_direction(self, value):
        self.ball_direction = value

    def set_enemy_score(self, value):
        self.enemy_score = value

    def set_friend_score(self, value):
        self.friend_score = value

    def get_enemy_score(self):
        return self.enemy_score

    def get_friend_score(self):
        return self.friend_score

    def get_ball_velocity(self):
        return self.ball_velocity

    def set_ball_velocity(self, value):
        self.ball_velocity = value

    # Convierte los valores verdaderos de la matriz a casillas en blanco en la pantalla
    def screen(self):
        for n in range(len(self.game_matrix)):
            for m in range(len(self.game_matrix[n])):
                if self.game_matrix[n][m]:
                    pygame.draw.rect(self.gameDisplay,self.current_color,[m*self.block_width, n*self.block_height,
                                                             self.block_width, self.block_height])
                else:
                    pygame.draw.rect(self.gameDisplay, black, [m * self.block_width, n * self.block_height,
                                                               self.block_width, self.block_height])

    # funcion encargada de escribir el score del jugador 1 en la matriz de juego
    def score_f(self):
        global display1_leds
        A = display1_leds[0]
        B = display1_leds[1]
        C = display1_leds[2]
        D = display1_leds[3]
        E = display1_leds[4]
        F = display1_leds[5]
        G = display1_leds[6]
        DP = display1_leds[7]
        num = self.friend_score

        DP.write(False)
        if num == 0:
            A.write(False)
            B.write(False)
            C.write(False)
            D.write(False)
            E.write(False)
            F.write(False)
            G.write(True)
            DP.write(True)
        elif num == 1:
            A.write(True)
            B.write(False)
            C.write(False)
            D.write(True)
            E.write(True)
            F.write(True)
            G.write(True)
            DP.write(True)
        elif num == 1:
            A.write(True)
            B.write(False)
            C.write(False)
            D.write(True)
            E.write(True)
            F.write(True)
            G.write(True)
            DP.write(True)

        elif num == 2:
            A.write(False)
            B.write(False)
            C.write(True)
            G.write(False)
            E.write(False)
            D.write(False)
            F.write(True)
            DP.write(True)
        elif num == 3:
            B.write(False)
            A.write(False)
            G.write(False)
            C.write(False)
            D.write(False)
            E.write(True)
            F.write(True)
            DP.write(True)
        elif num == 4:
            A.write(True)
            B.write(False)
            F.write(False)
            G.write(False)
            C.write(False)
            D.write(True)
            E.write(True)
            DP.write(True)
        elif num == 5:
            A.write(False)
            B.write(True)
            C.write(False)
            D.write(False)
            E.write(True)
            G.write(False)
            F.write(False)
            DP.write(True)
        elif num == 6:
            A.write(False)
            B.write(True)
            C.write(False)
            D.write(False)
            E.write(False)
            G.write(False)
            F.write(False)
            DP.write(True)
        elif num == 7:
            A.write(False)
            B.write(False)
            C.write(False)
            D.write(True)
            E.write(True)
            F.write(True)
            G.write(True)
            DP.write(True)
        elif num == 8:
            A.write(False)
            B.write(False)
            C.write(False)
            D.write(False)
            E.write(False)
            G.write(False)
            F.write(False)
            DP.write(True)
        elif num == 9:
            A.write(False)
            B.write(False)
            C.write(False)
            D.write(False)
            E.write(True)
            G.write(False)
            F.write(False)
            DP.write(True)

    # funcion encargada de escribir el score del jugador 1 en la matriz de juego
    def score_e(self):
        if self.enemy_score == 0:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 23 and 2 <= n <= 6) or (n == 2 and 23 <= m <= 25) or (m == 25 and 2 <= n <= 6) or (n == 6 and 23 <= m <= 25):
                        self.game_matrix[n][m] = True
                    if n == 24 or n == 0:
                        self.game_matrix[n][m] = True
                    elif n % 2 == 0 and m == 19:
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 1:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 23 and 2 <= n <= 6):
                        self.game_matrix[n][m] = True
                    if n == 24 or n == 0:
                        self.game_matrix[n][m] = True
                    elif n % 2 == 0 and m == 19:
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 2:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 23 <= m <= 25) or (m == 25 and n == 3) or (m == 23 and n == 5) :
                        self.game_matrix[n][m] = True
                    if n == 24 or n == 0:
                        self.game_matrix[n][m] = True
                    elif n % 2 == 0 and m == 19:
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 3:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 23 <= m <= 25) or (m == 25 and n == 5) or (m == 25 and n == 3):
                        self.game_matrix[n][m] = True
                    if n == 24 or n == 0:
                        self.game_matrix[n][m] = True
                    elif n % 2 == 0 and m == 19:
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 4:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 25 and 2 <= n <= 6) or (m == 23 and 2 <= n <= 4) or (m == 24 and n == 4):
                        self.game_matrix[n][m] = True
                    if n == 24 or n == 0:
                        self.game_matrix[n][m] = True
                    elif n % 2 == 0 and m == 19:
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 5:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 23 <= m <= 25) or (m == 25 and n == 5) or (m == 23 and n == 3):
                        self.game_matrix[n][m] = True
                    if n == 24 or n == 0:
                        self.game_matrix[n][m] = True
                    elif n % 2 == 0 and m == 19:
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 6:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 23 <= m <= 25) or (m == 23 and n == 5)or (m == 25 and n == 5) or (m == 23 and n == 3):
                        self.game_matrix[n][m] = True
                    if n == 24 or n == 0:
                        self.game_matrix[n][m] = True
                    elif n % 2 == 0 and m == 19:
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 7:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 25 and 2 <= n <= 6) or ((m == 24 or m == 23) and n == 2):
                        self.game_matrix[n][m] = True
                    if n == 24 or n == 0:
                        self.game_matrix[n][m] = True
                    elif n % 2 == 0 and m == 19:
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 8:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 23 <= m <= 25) or ((m == 25 or m == 23) and (n == 3 or n == 5)):
                        self.game_matrix[n][m] = True
                    if n == 24 or n == 0:
                        self.game_matrix[n][m] = True
                    elif n % 2 == 0 and m == 19:
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 9:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 25 and 2 <= n <= 6) or (m == 23 and 2 <= n <= 4) or (m == 24 and n == 4) or (m == 24 and n == 2):
                        self.game_matrix[n][m] = True
                    if n == 24 or n == 0:
                        self.game_matrix[n][m] = True
                    elif n % 2 == 0 and m == 19:
                        self.game_matrix[n][m] = True


    # Llama a las funciones que modifican la matriz segun el tablero
    def scores(self):
        self.score_e()
        self.score_f()

    # Pone cada espacio de la matriz en False, excepto el marcador y la cancha
    def clean_matrix(self):
        for n in range(len(self.game_matrix)):
            for m in range(len(self.game_matrix[0])):
                if n != 0 and n != 24:
                    if n % 2 == 0 and m == 19:
                        self.game_matrix[n][m] = True
                    else:
                        self.game_matrix[n][m] = False
        self.scores()

    # Pausa el juego
    def pause(self, ins=False):
        global current_color
        global placa1
        global botones1

        pause = True
        for n in range(len(self.game_matrix)):
            for m in range(len(self.game_matrix)):
                if n % 2  == 0 and m == 19 and n != 0 and n != 24:
                    self.game_matrix[n][m] = False
            self.screen()
            pygame.display.update()


        if ins:
            self.inspector()

        while pause:
            pygame.mixer.music.pause()
            self.message_to_screen('Juego pausado', white, size='large')
            self.message_to_screen('Presione p para reanudar', white, y_displace=80)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pygame.mixer.music.unpause()
                        pause = False
                    elif event.key == pygame.K_b:
                        self.current_color = white
                    elif event.key == pygame.K_v:
                        self.current_color = green

                    elif event.key == pygame.K_ESCAPE:
                        placa1.exit()
                        pygame.quit()
                        quit()

                elif event.type == pygame.QUIT:
                    placa1.exit()
                    pygame.quit()
                    quit()

            if botones1[5].read() == 1.0:
                pygame.mixer.music.unpause()
                pause = False
            elif botones1[3].read() == 1.0:
                self.current_color = green
            elif botones1[4].read() == 1.0:
                self.current_color = white
            elif botones1[6].read() == 1.0:
                placa1.exit()
                pygame.quit()
                quit()


            self.screen()
            self.message_to_screen('Juego pausado',self.current_color, size='large')
            self.message_to_screen('Presione p para reanudar', self.current_color, y_displace=80)
            pygame.display.update()
            placa1.pass_time(0.2)

        for n in range(len(self.game_matrix)):
            for m in range(len(self.game_matrix)):
                if n % 2  == 0:
                    self.game_matrix[n][m] = True


    def inspector(self):
        global botones1
        root = Tk()

        t = Text(root, width=41, height=26,)
        i = 0
        for x in self.game_matrix:
            for y in self.game_matrix[i]:
                if y:
                    t.insert(END, 1)
                else:
                    t.insert(END, 0)
            t.insert(END, '\n')
            i += 1
        t.config(state=DISABLED)
        t.pack()
        ins = True

        quit = lambda *args: root.destroy()

        root.bind('<Escape>', quit)
        root.bind('i', quit)

        stay = True

        while stay:
            if botones1[6].read() == 1.0:
                stay = False
            elif botones1[7].read() == 1.0:
                stay = False
            root.update_idletasks()
            root.update()
            time.sleep(0.01)
            placa1.pass_time(0.2)

        quit()

    # Presenta la animacion de un nuevo jugador
    def new_player(self):
        for n in range(len(self.game_matrix)):
            for m in range(len(self.game_matrix)):
                if n % 2  == 0 and m == 19 and n != 0 and n != 24:
                    self.game_matrix[n][m] = False
            self.screen()
            pygame.display.update()
        for i in range(0,6):
            self.gameDisplay.fill(black)
            self.screen()
            clock.tick(1)
            if i%2 == 0:
                self.message_to_screen('A new challenger', current_color, size='medium')
                self.message_to_screen('has arrived', current_color, size='medium', y_displace=40)
            pygame.display.update()

    # Devuelve los marcadores a 0
    def reset_scores(self):
        self.enemy_score = 0
        self.friend_score = 0
        self.screen()

    # Se encarga de la animacion en la transicion de nivel
    def levelup_animation(self, spec=0):
        if self.level != 3:
            if not spec:
                self.level += 1
                self.update_paleta()
                self.update_velocity()
                for n in range(len(self.game_matrix)):
                    for m in range(len(self.game_matrix)):
                        if n % 2 == 0 and m == 19 and n != 0 and n != 24:
                            self.game_matrix[n][m] = False
                    self.screen()
            else:
                self.level = spec
                self.update_paleta()
                self.update_velocity()
                for n in range(len(self.game_matrix)):
                    for m in range(len(self.game_matrix)):
                        if n % 2 == 0 and m == 19 and n != 0 and n != 24:
                            self.game_matrix[n][m] = False
                self.screen()
                pygame.display.update()
        elif spec == 1:
            self.level = spec
            self.update_paleta()
            self.update_velocity()
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix)):
                    if n % 2 == 0 and m == 19 and n != 0 and n != 24:
                        self.game_matrix[n][m] = False
            self.screen()
            pygame.display.update()
        elif self.pc:
            return False
        else:
            pass
        if self.pc:
            self.music_update()
        return True

    # Metodos de actualizacion
    def update_paleta(self):
        self.paleta_length = 9 - 3*(self.level-1)
        if not self.practice:
            self.paleta_length_e = 9 - 3*(self.level-1)

    def update_velocity(self):
        self.ball_velocity = 30 + 3*self.level

    def reset_level(self):
        self.level = 1
        for n in range(len(self.game_matrix)):
            for m in range(len(self.game_matrix)):
                if n % 2  == 0 and m == 19 and n != 0 and n != 24:
                    self.game_matrix[n][m] = False
        self.update_paleta()
        self.screen()
        pygame.display.update()
        self.update_velocity()

    def music_update(self):
        self.lvl_music()

    def paleta_length_update(self):
        self.paleta_length = 9 - 3*self.level

    # Funcion encargada de renderizar el texto a poner en la pantalla, recibe un texto, un color y un tamanno y retorna
    # el texto renderizado asi como el punto central del mismo.
    def text_objects(self, text, color, size):
        if size == 'small':
            textSurface = smallfont.render(text, True, color)
        if size == 'medium':
            textSurface = mediumfont.render(text, True, color)
        elif size == 'large':
            textSurface = largefont.render(text, True, color)
        return textSurface, textSurface.get_rect()

    # Dado un mensaje, un color, un desplazamiento del centro de la pantalla en x, un desplazamiento del centor de la pantalla
    # en y y un tamanno de los ya predeterminados, este funcion muestra un texto en la pantalla.
    def message_to_screen(self, msg, color,x_displace=0, y_displace=0, size='small'):
        textSurf, textRect = self.text_objects(msg, color, size)
        textRect.center = (self.width/2) + x_displace, (self.height/2) + y_displace
        self.gameDisplay.blit(textSurf, textRect)


# Clase encargada de guardar la posicion de la bola y modificar la matriz del juego conforme a la misma
class Bola:
    def __init__(self, pos_x, pos_y, block_width, block_height):
        self.width = block_width
        self.height = block_height
        self.x = pos_x
        self.y = pos_y

    # Modifica la matriz del juego segun la posicion de la bola
    def mod_matrix(self, matrix):
        for n in range(len(matrix)):
            for m in range(len(matrix[0])):
                if m == self.x and n == self.y:
                    matrix[n][m] = True
        return matrix


# Clase encargada de guardar la posicion de cada paleta y modificar la matriz del juego segun la misma y su longitud
class Paleta:
    def __init__(self, pos_x, pos_y, block_width, block_height):
        self.width = block_width
        self.height = block_height
        self.x = pos_x
        self.y = pos_y

    # modifica la matriz del juego segun la posicion de la paleta y su longitud
    def mod_matrix(self, matrix, paleta_length):
        for n in range(len(matrix)):
            for m in range(len(matrix[0])):
                if m == self.x and n == self.y:
                    for i in range(paleta_length):
                        if n+i <=len(matrix)-1:
                            matrix[n+i][m] = True
        return matrix

# Clase encargada de guardar la posicion de cada obstaculo, asi como crearlos dentro de la matriz.
class Obstaculo:
    def __init__(self, posx, posy, width, height):
        self.x = posx
        self.y = posy
        self.width = width
        self.height = height

    def create(self, matrix):
        save = matrix
        for n in range(len(matrix)):
            for m in range(len(matrix[0])):
                if self.x + self.width > m >= self.x and self.y + self.height > n >= self.y:
                    matrix[n][m] = True
        return matrix

class Game:
    global mode
    def __init__(self, MODE, PC, MUTE, PT, SERVER, color):
        global choosed
        global start_boring_timer

        arduino1_setup()

        if color == 'white' or (255,255,255):
            self.color = (255,255,255)
        else:
            self.color = (0,255,0)
        self.client1 = None
        self.listener1 = None
        self.conn1 = None
        self.client2 = None
        self.listener2 = None
        self.conn2 = None

        if color == 'white':
            self.color = (255,255,255)
        else:
            self.color = (0,255,0)
        # Instancia del Tablero
        self.game_field = Tablero(bool(PC), block_height, block_width, MUTE, PT, self.color)
        # Posiciones iniciales de los jugadores

        # Primeras paletas
        self.player1_1x = 0
        self.player1_1y = 1
        self.player2_1x = len(self.game_field.get_matrix()[0]) - 1
        self.player2_1y = 1
        # Segundas paletas
        self.player1_2x = 11
        self.player1_2y = (len(self.game_field.get_matrix()) - self.game_field.paleta_length) - 1
        self.player2_2x = len(self.game_field.get_matrix()[0]) - 11
        self.player2_2y = len(self.game_field.get_matrix()) - 1 - self.game_field.paleta_length_e

        # Controlan el movimiento de los jugadores

        # Primeras paletas
        self.player1_2down_y = False
        self.player1_2up_y = False
        self.player2_2up_y = False
        self.player2_2down_y = False

        # Segundas paletas
        self.player1_1down_y = False
        self.player1_1up_y = False
        self.player2_1up_y = False
        self.player2_1down_y = False

        self.ball_x = 19
        self.ball_y = 12

        self.obstaculo_list = []

        self.timer_clock = pygame.time.Clock()
        self.time_playing = 0
        self.obstaculos()

        self.timer_clock = pygame.time.Clock()
        self.time_playing = 0

        # Controlan el juego
        self.game = True

        self.mode = MODE
        self.pc = bool(PC)
        self.server = SERVER
        self.mute = bool(MUTE)
        self.practice = bool(PT)

        # Abriendo el archivo de highscores y guardando los datos en una lista
        self.path = 'highscores.txt'

        self.file = open(self.path, 'r')

        contents = []

        for line in self.file:
            contents.append(line[:len(line) - 1])

        self.final = []

        k = 0

        #for i in contents:
         #   self.final.append(i.split('%'))
          #  self.final[k][1] = int(self.final[k][1])
           # k += 1

        self.file.close()
        self.server = SERVER
        if self.server:
            print(sys.argv[7])
            print(sys.argv[8])
            self.start_server(sys.argv[7], sys.argv[8])
        self.gameloop(MODE)


    def gameloop(self, mode):
        global start_boring_timer
        global choosed
        self.choosed = False
        start_boring_timer = time.time()
        self.timer_clock.tick()
        if mode == 'singles':
            self.singles()
        elif mode == 'doubles':
            self.doubles()
        else:
            return 'Err'

    def singles(self):
        global start_boring_timer
        global choosed
        global botones1
        while self.game:
            self.timer_clock.tick()
            # Reconocimiento de eventos
            if self.conn1 == None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.player1_1up_y = True
                        elif event.key == pygame.K_DOWN:
                            self.player1_1down_y = True
                        elif event.key == pygame.K_w and not self.pc:
                            self.player2_1up_y = True
                        elif event.key == pygame.K_w:
                            self.game_field.pc = False
                            self.game_field.reset_level()
                            self.game_field.new_player()
                            self.game_field.reset_scores()
                            start_boring_timer = time.time()
                        elif event.key == pygame.K_s and not self.pc:
                            self.player2_1down_y = True
                        elif event.key == pygame.K_p:
                            self.game_field.pause()
                        elif event.key == pygame.K_i:
                            self.game_field.pause(True)
                            self.timer_clock.tick()
                        elif event.key == pygame.K_m:
                            self.game_field.mute = not self.mute
                            self.mute = not self.mute
                            self.game_field.music_update()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            self.player1_1up_y = False
                        elif event.key == pygame.K_DOWN:
                            self.player1_1down_y = False
                        elif event.key == pygame.K_w:
                            self.player2_1up_y = False
                        elif event.key == pygame.K_s:
                            self.player2_1down_y = False
            else:
                eventos1er = self.conn1.recv()
                eventos2do = self.conn2.recv()
                print(eventos2do)
                print(eventos1er)
                eventos = self.juntar(eventos1er, eventos2do)

                for keydown in eventos[0]:
                    if keydown == 'UP':
                        self.player1_1up_y = True
                    elif keydown == 'DOWN':
                        self.player1_1down_y = True
                    elif keydown == 'P':
                        self.pause(1)
                        break
                for keyup in eventos[1]:
                    if keyup == 'UP':
                        self.player1_1up_y = False
                    elif keyup == 'DOWN':
                        self.player1_1down_y = False
                for keydown in eventos[3]:
                    if keydown == 'W':
                        self.player2_1up_y = True
                    elif keydown == 'S':
                        self.player2_1down_y = True
                    elif keydown == 'P':
                        self.pause(2)
                        break
                for keyup in eventos[4]:
                    if keyup == 'W':
                        self.player2_1up_y = False
                    elif keyup == 'S':
                        self.player2_1down_y = False


            if botones1[2].read() and self.player1_1y + self.game_field.paleta_length + 1 < len(self.game_field.get_matrix()):
                self.player1_1y += 1
            elif botones1[0].read() and self.player1_1y-1 > 2:
                self.player1_1y -= 1
            elif botones1[3].read() == 1.0:
                self.color = white
                self.game_field.current_color = white
            elif botones1[4].read() == 1.0:
                self.color = green
                self.game_field.current_color = green
            elif botones1[5].read() == 1.0:
                self.game_field.pause()
                self.timer_clock.tick()
            elif botones1[7].read() == 1.0:
                self.game_field.pause(True)
                self.timer_clock.tick()

            # Movimiento de las paletas del primer jugador
            if self.player1_1down_y and self.player1_1y + self.game_field.paleta_length + 1 < len(self.game_field.get_matrix()):
                self.player1_1y += 1
            elif self.player1_1up_y and self.player1_1y+1 > 2:
                self.player1_1y -= 1

            # Movimiento de las paletas del segundo jugador
            if self.player2_1down_y and self.player2_1y + self.game_field.paleta_length_e + 1 < len(self.game_field.get_matrix()):
                self.player2_1y += 1
            elif self.player2_1up_y and self.player2_1y+1 > 2:
                self.player2_1y -= 1

            # Rebote de la pelota
            self.ball_x, self.ball_y = self.ball_bounce_singles(self.ball_x,self.ball_y,self.player1_1x,self.player1_1y,self.player2_1x,self.player2_1y)
            # Sube la dificultad si no hay goles
            if time.time() - start_boring_timer > 10 and not self.game_field.pc and not self.game_field.practice:
                self.game_field.levelup_animation()
                self.message_to_screen('Level Up!!', self.color, size = 'large')
                self.player1_1y = 1
                self.player2_1y = 1
                self.player1_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length-1
                self.player2_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length_e-1
                start_boring_timer = time.time()
            # Inteligencia artificial cuando la pc esta habilitada
                try:
                    choosed
                except:
                    choosed = False
                nxt_move = 0
                if self.ball_x == 1:
                    choice_hit = random.choice([-1, 0, 1])
                    choosed = True
                elif self.ball_x == 12 and not choosed:
                    choice_hit = random.choice([-1, 0, 1])
                    choosed = True
                elif self.ball_x == 20 and not choosed:
                    choice_hit = random.choice([-1, 0, 1])
                    choosed = True
                elif self.ball_x == 27:
                    choice_hit = random.choice([-1, 0, 1])
                    choosed = True
            if self.game_field.pc and self.game_field.get_ball_direction()[0] > 0:
                if self.ball_x == 1 or self.ball_x == 20:
                    choice_hit = random.choice([-1, 0, 1])
                    y_hit = self.simulacion(self.ball_x, self.ball_y, self.game_field.get_ball_direction()[1]) + random.randint(-int(self.game_field.paleta_length/2)+2, 2+int(self.game_field.paleta_length/2))
                    while not 0 <= y_hit < 24:
                        y_hit = self.simulacion(self.ball_x, self.ball_y, self.game_field.get_ball_direction()[1]) + random.randint(
                            -int(self.game_field.paleta_length / 2) + 1, 1 + int(self.game_field.paleta_length / 2))
                if choice_hit == -1:
                    if y_hit < self.player2_1y and self.player2_1y-1 >= 1:
                        nxt_move = -1
                    elif y_hit > self.player2_1y and self.player2_1y + int(self.game_field.paleta_length+1) <= 24:
                        nxt_move = 1
                    elif y_hit == self.player2_1y:
                        nxt_move = 0
                    else:
                        nxt_move = 0
                elif choice_hit == 0:
                    if y_hit < self.player2_1y + int(self.game_field.paleta_length+1)/2 -1 and self.player2_1y-1 >= 1:
                        nxt_move = -1
                    elif y_hit > self.player2_1y + int(self.game_field.paleta_length+1)/2 -1 and self.player2_1y + int(
                            self.game_field.paleta_length+1) <= 24:
                        nxt_move = 1
                    elif y_hit == self.player2_1y + int(self.game_field.paleta_length+1)/2 -1:
                        nxt_move = 0
                    else:
                        nxt_move = 0
                elif choice_hit == 1:
                    if y_hit < self.player2_1y + int(self.game_field.paleta_length) -1 and self.player2_1y-1 >= 1:
                        nxt_move = -1
                    elif y_hit > self.player2_1y + int(self.game_field.paleta_length) -1 and self.player2_1y + int(self.game_field.paleta_length+1) <= 24:
                        nxt_move = 1
                    elif y_hit == self.player2_1y + int(self.game_field.paleta_length) -1:
                        nxt_move = 0
                    else:
                        nxt_move = 0

                self.player2_1y += nxt_move

            # Se realizan los movimientos y se modifica la pantalla

            self.game_field.clean_matrix()
            self.game_field.screen()
            matrix = self.game_field.get_matrix()
            self.ball_x += 1 * self.game_field.get_ball_direction()[0]
            self.ball_y += 1 * self.game_field.get_ball_direction()[1]
            self.bola = Bola(self.ball_x, self.ball_y, block_width, block_height)
            self.bola.mod_matrix(matrix)
            self.player1 = Paleta(self.player1_1x, self.player1_1y, block_width, block_height)
            self.player2 = Paleta(self.player2_1x, self.player2_1y, block_width, block_height)
            self.player1.mod_matrix(matrix, self.game_field.paleta_length)
            self.player2.mod_matrix(matrix, self.game_field.paleta_length_e)
            for i in self.obstaculo_list:
                matrix = i.create(matrix)
            self.game_field.set_matrix(matrix)
            self.game_field.screen()
            if self.game_field.pc and not self.game_field.practice:
                self.message_to_screen('Press w to add a new player', self.color, 200, 250)

            if self.server:
                self.send_matrix(matrix)
            pygame.display.update()

            # Controla la velocidad
            clock.tick(self.game_field.get_ball_velocity())

            self.time_playing += self.timer_clock.tick()/1000

    def doubles(self):
        global start_boring_timer
        global choosed
        while self.game:
            self.timer_clock.tick()
            # Reconocimiento de eventos
            if self.conn1 == None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.player1_1up_y = True
                        elif event.key == pygame.K_DOWN:
                            self.player1_1up_y = True
                        elif event.key == pygame.K_w and not self.pc:
                            self.player2_1up_y = True
                        elif event.key == pygame.K_w:
                            self.game_field.pc = False
                            self.game_field.reset_level()
                            self.game_field.new_player()
                            self.game_field.reset_scores()
                            start_boring_timer = time.time()
                        elif event.key == pygame.K_s and not self.pc:
                            self.player2_1down_y = True
                        elif event.key == pygame.K_p:
                            self.game_field.pause()
                        elif event.key == pygame.K_i:
                            self.game_field.pause(True)
                            self.timer_clock.tick()
                        elif event.key == pygame.K_m:
                            self.game_field.mute = not self.mute
                            self.mute = not self.mute
                            self.game_field.music_update()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            self.player1_1up_y = False
                        elif event.key == pygame.K_DOWN:
                            self.player1_1down_y = False
                        elif event.key == pygame.K_w:
                            self.player2_1up_y = False
                        elif event.key == pygame.K_s:
                            self.player2_1down_y = False
            else:
                eventos1er = self.conn1.recv()
                eventos2do = self.conn2.recv()
                eventos = self.juntar(eventos1er, eventos2do)
                for keydown in eventos[0]:
                    if keydown == 'UP':
                        self.player1_1up_y = True
                    elif keydown == 'DOWN':
                        self.player1_1down_y = True
                    elif keydown == 'P':
                        self.game_field.pause()
                for keyup in eventos[1]:
                    if keyup == 'UP':
                        self.player1_1up_y = False
                    elif keyup == 'DOWN':
                        self.player1_1down_y = False
                for keydown in eventos[3]:
                    if keydown == 'W':
                        self.player2_1up_y = True
                    elif keydown == 'S':
                        self.player2_1down_y = True
                    elif keydown == 'P':
                        self.game_field.pause()
                for keyup in eventos[4]:
                    if keyup == 'W':
                        self.player2_1up_y = False
                    elif keyup == 'S':
                        self.player2_1down_y = False
            print('jelou')
            if botones1[0].read() and self.player1_1y-1 > 0:
                self.player1_1y -= 1
                self.player1_2y += 1
            elif botones1[2].read() and self.player1_1y + self.game_field.paleta_length + 1 < len(self.game_field.get_matrix()):
                self.player1_1y += 1
                self.player1_2y -= 1
            elif botones1[3].read() == 1.0:
                self.color = white
                self.game_field.current_color = white
            elif botones1[4].read() == 1.0:
                self.color = green
                self.game_field.current_color = green
            elif botones1[5].read() == 1.0:
                self.game_field.pause()
                self.timer_clock.tick()
            elif botones1[7].read() == 1.0:
                self.game_field.pause(True)
                self.timer_clock.tick()

            # Movimiento de las paletas del primer jugador
            if self.player1_1down_y and self.player1_1y + self.game_field.paleta_length + 1 < len(self.game_field.get_matrix()):
                self.player1_1y += 1
                self.player1_2y -= 1
            elif self.player1_1up_y and self.player1_1y-1 > 0:
                self.player1_1y -= 1
                self.player1_2y += 1

            # Movimiento de las paletas del segundo jugador
            if self.player2_1down_y and self.player2_1y + self.game_field.paleta_length + 1 < len(self.game_field.get_matrix()):
                self.player2_1y += 1
                self.player2_2y -= 1
            elif self.player2_1up_y and self.player2_1y+1 > 2:
                self.player2_1y -= 1
                self.player2_2y += 1

            # Movimiento de la bola
            if not self.game_field.practice :
                self.ball_x, self.ball_y = self.ball_bounce_doubles(self.ball_x,self.ball_y,self.player1_1x, self.player1_2x,self.player1_1y, self.player1_2y, self.player2_1x, self.player2_2x,
                                                                   self.player2_1y, self.player2_2y)
            elif self.game_field.ball_direction[0]<0:
                self.ball_x, self.ball_y = self.ball_bounce_doubles(self.ball_x,self.ball_y,self.player1_1x, self.player1_2x,self.player1_1y, self.player1_2y, self.player2_1x, self.player2_2x,
                                                                   self.player2_1y, self.player2_2y)
            else:
                self.ball_x, self.ball_y = self.ball_bounce_singles(self.ball_x,self.ball_y,self.player1_1x,self.player1_1y, self.player2_1x,
                                                                    self.player2_1y)

            # Sube la dificultad si no hay goles
            if time.time() - start_boring_timer > 10 and not self.game_field.pc and not self.game_field.practice:
                self.game_field.levelup_animation()
                self.message_to_screen('Level Up!!', self.color, size = 'large')
                self.player1_1y = 1
                self.player2_2y = 1
                self.player1_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length-1
                self.player2_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length-1
                start_boring_timer = time.time()

            # Inteligencia artificial
            if self.game_field.pc and self.game_field.get_ball_direction()[0] > 0:
                try:
                    choosed
                except:
                    choosed = False
                nxt_move = 0
                if self.ball_x == 1:
                    choice_hit = random.choice([-1, 0, 1])
                    paleta_choose = random.choice([1, 2])
                    choosed = True
                elif self.ball_x == 12 and not choosed:
                    choice_hit = random.choice([-1, 0, 1])
                    paleta_choose = random.choice([1, 2])
                    choosed = True
                elif self.ball_x == 20 and not choosed:
                    choice_hit = random.choice([-1, 0, 1])
                    paleta_choose = random.choice([1, 2])
                    choosed = True
                elif self.ball_x == 27:
                    choice_hit = random.choice([-1, 0, 1])
                    paleta_choose = 1
                    choosed = True
                if paleta_choose == 1:
                    if self.ball_x == 1 or self.ball_x == 20 or self.ball_x == 12:
                        y_hit = self.simulacion(self.ball_x, self.ball_y, self.game_field.get_ball_direction()[1]) + random.randint(-int(self.game_field.paleta_length/2)+2, 2+int(self.game_field.paleta_length/2))
                        while not 2 <= y_hit < 29:
                            y_hit = self.simulacion(self.ball_x, self.ball_y, self.game_field.get_ball_direction()[1]) + random.randint(
                                -int(self.game_field.paleta_length / 2) + 1, 1 + int(self.game_field.paleta_length / 2))

                    if choice_hit == -1:
                        if y_hit < self.player2_1y and self.player2_1y - 1 >= 1:
                            nxt_move = -1
                        elif y_hit > self.player2_1y and self.player2_1y + int(self.game_field.paleta_length + 1) + 1 < 24:
                            nxt_move = 1
                        elif y_hit == self.player2_1y:
                            nxt_move = 0
                        else:
                            nxt_move = 0
                    elif choice_hit == 0:
                        if y_hit < self.player2_1y + int(self.game_field.paleta_length + 1) / 2 - 1 and self.player2_1y - 1 >= 1:
                            nxt_move = -1
                        elif y_hit > self.player2_1y + int(self.game_field.paleta_length + 1) / 2 - 1 and self.player2_1y + int(
                                self.game_field.paleta_length + 1) <= 24:
                            nxt_move = 1
                        elif y_hit == self.player2_1y + int(self.game_field.paleta_length + 1) / 2 - 1:
                            nxt_move = 0
                        else:
                            nxt_move = 0
                    elif choice_hit == 1:
                        if y_hit < self.player2_1y + int(self.game_field.paleta_length) - 1 and self.player2_1y - 1 >= 1:
                            nxt_move = -1
                        elif y_hit > self.player2_1y + int(self.game_field.paleta_length) - 1 and self.player2_1y + int(
                                self.game_field.paleta_length + 1) <= 24:
                            nxt_move = 1
                        elif y_hit == self.player2_1y + int(self.game_field.paleta_length) - 1:
                            nxt_move = 0
                        else:
                            nxt_move = 0

                else:
                    if self.ball_x == 1 or self.ball_x == 20 or self.ball_x == 12:
                        choice_hit = random.choice([-1, 0, 1])
                        y_hit = self.simulacion_2nd(self.ball_x, self.ball_y, self.game_field.get_ball_direction()[1]) + random.randint(
                            -int(self.game_field.paleta_length / 2) + 2, 2 + int(self.game_field.paleta_length / 2))
                        while not 2 <= y_hit < 29:
                            y_hit = self.simulacion_2nd(self.ball_x, self.ball_y, self.game_field.get_ball_direction()[1]) + random.randint(
                                -int(self.game_field.paleta_length / 2) + 1, 1 + int(self.game_field.paleta_length / 2))

                    if choice_hit == -1:
                        if y_hit < self.player2_2y and self.player2_1y + int(self.game_field.paleta_length + 1) + 1 <= 24:
                            nxt_move = 1
                        elif y_hit > self.player2_2y and self.player2_1y - 1 >= 1:
                            nxt_move = -1
                        elif y_hit == self.player2_2y:
                            nxt_move = 0
                        else:
                            nxt_move = 0
                    elif choice_hit == 0:
                        if y_hit < self.player2_2y + int(self.game_field.paleta_length + 1) / 2 - 1 and self.player2_1y + int(
                                self.game_field.paleta_length + 1) <= 24:
                            nxt_move = 1
                        elif y_hit > self.player2_2y + int(self.game_field.paleta_length + 1) / 2 - 1 and  self.player2_1y - 1 >= 1:
                            nxt_move = -1
                        elif y_hit == self.player2_2y + int(self.game_field.paleta_length + 1) / 2 - 1:
                            nxt_move = 0
                        else:
                            nxt_move = 0
                    elif choice_hit == 1:
                        if y_hit < self.player2_2y + int(self.game_field.paleta_length) - 1 and self.player2_1y + int(
                                self.game_field.paleta_length + 1) + 1 <= 24:
                            nxt_move = 1
                        elif y_hit > self.player2_2y + int(self.game_field.paleta_length) - 1 and self.player2_1y - 1 >= 1 :
                            nxt_move = -1
                        elif y_hit == self.player2_2y + int(self.game_field.paleta_length) - 1:
                            nxt_move = 0
                        else:
                            nxt_move = 0



                self.player2_1y += nxt_move
                self.player2_2y -= nxt_move

            # Se realizan los movimientos y se modifica la pantalla
            self.game_field.clean_matrix()

            matrix = self.game_field.get_matrix()
            self.ball_x += 1 * self.game_field.get_ball_direction()[0]
            self.ball_y += 1 * self.game_field.get_ball_direction()[1]
            self.bola = Bola(self.ball_x, self.ball_y, block_width, block_height)
            self.bola.mod_matrix(matrix)
            self.player1_1 = Paleta(self.player1_1x, self.player1_1y, block_width, block_height)
            self.player2_1 = Paleta(self.player2_1x, self.player2_1y, block_width, block_height)
            self.player1_2 = Paleta(self.player1_2x, self.player1_2y, block_width, block_height)
            self.player2_2 = Paleta(self.player2_2x, self.player2_2y, block_width, block_height)
            self.player1_1.mod_matrix(matrix, self.game_field.paleta_length)
            self.player2_2.mod_matrix(matrix, self.game_field.paleta_length_e)
            self.player2_1.mod_matrix(matrix, self.game_field.paleta_length_e)
            self.player1_2.mod_matrix(matrix, self.game_field.paleta_length)
            for i in self.obstaculo_list:
                matrix = i.create(matrix)
            self.game_field.set_matrix(matrix)
            if self.conn1 == None:
                self.game_field.screen()
            else:
                self.send_matrix(matrix)
            if self.game_field.pc:
                self.message_to_screen('Press w to add a new player', self.color, 200, 250)
            pygame.display.update()

            # Se controla la velocidad
            clock.tick(self.game_field.get_ball_velocity())

            self.time_playing += self.timer_clock.tick()


    # Funcion recursiva encargada de simular el movimiento de la bola dadas una pos inicial en x y y y una direccion hacia
    # donde se mueve la misma. Retorna la posicion en y donde va a pegar la bola al lado derecho. Se utiliza para la inteligencia
    # artificial. Version singles.
    def simulacion(self, pos_x, pos_y, direction):
        if direction == 0:
            return pos_y
        elif pos_x == 38:
            return pos_y
        elif pos_y == 1:
            return self.simulacion(pos_x, pos_y + 1, direction * -1)
        elif pos_y == 23:
            return self.simulacion(pos_x, pos_y - 1, direction * -1)
        elif direction == 1:
            return self.simulacion(pos_x + 1, pos_y + 1, direction)
        elif direction == -1:
            return self.simulacion(pos_x + 1, pos_y - 1, direction)

    # Funcion recursiva encargada de simular el movimiento de la bola dadas una pos inicial en x y y y una direccion hacia
    # donde se mueve la misma. Retorna la posicion en y donde va a pegar la bola al lado derecho. Se utiliza para la inteligencia
    # artificial. Version doubles.
    def simulacion_2nd(self, pos_x, pos_y, direction):
        if direction == 0:
            return pos_y
        elif pos_x == len(self.game_field.get_matrix()[0]) - 12:
            return pos_y
        elif pos_y == 1:
            return self.simulacion_2nd(pos_x, pos_y + 1, direction * -1)
        elif pos_y == 23:
            return self.simulacion_2nd(pos_x, pos_y - 1, direction * -1)
        elif direction == 1:
            return self.simulacion_2nd(pos_x + 1, pos_y + 1, direction)
        elif direction == -1:
            return self.simulacion_2nd(pos_x + 1, pos_y - 1, direction)

    # Funcion encargada del rebote de la bola en bordes o en paletas. Version single
    # E: posicion de la bola en x, posicion de la bola en y, posicion de la paleta del jugador 1 en x y y, posicion de la paleta
    # del jugador 2 en x y y.
    # S: Nueva posicion de la bola en x y y
    # R: -
    def ball_bounce_singles(self, ball_x, ball_y, player1_1x, player1_1y, player2_1x, player2_1y):
        global start_boring_timer
        if (self.game_field.get_ball_direction()[
                0] > 0 and ball_x + 1 == player2_1x and (
                    player2_1y <= ball_y <= player2_1y + self.game_field.paleta_length_e or (
                    self.game_field.get_ball_direction()[
                        1] > 0 and player2_1y <= ball_y + 1 <= player2_1y + self.game_field.paleta_length_e) or (
                            self.game_field.get_ball_direction()[
                                1] < 0 and player2_1y <= ball_y - 1 <= player2_1y + self.game_field.paleta_length_e))) or (
                self.game_field.get_ball_direction()[
                    0] < 0 and ball_x - 1 == 0 and (player1_1y <= ball_y <= player1_1y + self.game_field.paleta_length or (
                self.game_field.get_ball_direction()[
                    1] > 0 and player1_1y <= ball_y + 1 <= player1_1y + self.game_field.paleta_length) or (
                                                            self.game_field.get_ball_direction()[
                                                                1] > 0 and player1_1y <= ball_y + 1 <= player1_1y + self.game_field.paleta_length)
                )):

            self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0] * -1, self.game_field.get_ball_direction()[1]))

            if self.game_field.get_ball_direction()[0] < 0:
                if player2_1y <= ball_y <= player2_1y + self.game_field.paleta_length_e / 3 -1:
                    if not self.game_field.practice:
                        self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 1))
                        self.game_field.set_ball_velocity(self.game_field.ball_velocity)
                    else:
                        self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], random.randint(-1,1)))
                        self.game_field.set_ball_velocity(self.game_field.ball_velocity)
                elif player2_1y + self.game_field.paleta_length_e / 3 <= ball_y <= player2_1y + (
                        2 * self.game_field.paleta_length_e) / 3 -1:
                    if not self.game_field.practice:
                        self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 0))
                        self.game_field.set_ball_velocity(self.game_field.ball_velocity)
                    else:
                        self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], random.randint(-1,1)))
                        self.game_field.set_ball_velocity(self.game_field.ball_velocity)
                elif player2_1y + (2 * self.game_field.paleta_length_e / 3) <= ball_y <= player2_1y + (
                        3 * self.game_field.paleta_length_e) / 3 -1:
                    if not self.game_field.practice:
                        self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], -1))
                        self.game_field.set_ball_velocity(self.game_field.ball_velocity)
                    else:
                        self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], random.randint(-1,1)))
                        self.game_field.set_ball_velocity(self.game_field.ball_velocity)
                # Pong
                pong_sound.play()
            elif self.game_field.get_ball_direction()[0] > 0:
                if player1_1y <= ball_y <= player1_1y + self.game_field.paleta_length / 3 - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 1))
                    self.game_field.set_ball_velocity(self.game_field.ball_velocity)
                elif player1_1y + self.game_field.paleta_length / 3 <= ball_y <= player1_1y + (
                        2 * self.game_field.paleta_length) / 3 - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 0))
                    self.game_field.set_ball_velocity(self.game_field.ball_velocity)
                elif player1_1y + (2 * self.game_field.paleta_length / 3) <= ball_y <= player1_1y + (
                        3 * self.game_field.paleta_length) / 3 - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], -1))
                    self.game_field.set_ball_velocity(self.game_field.ball_velocity)
                # Ping
                ping_sound.play()
        elif self.game_field.get_ball_direction()[0] > 0 and ball_x + 1 == len(self.game_field.get_matrix()[0]) + 2:
            if self.game_field.get_friend_score() < 9:
                self.game_field.set_friend_score(self.game_field.get_friend_score() + 1)
                point_sound.play()
                start_boring_timer = time.time()
                if not self.pc:
                    self.game_field.levelup_animation(spec=1)
                ball_x = 19
                ball_y = 12
            elif self.game_field.pc:
                if self.game_field.pc:
                    self.game_field.reset_scores()
                    lvlup = self.game_field.levelup_animation()
                    if lvlup:
                        self.message_to_screen('Level Up!!', self.color, size='large')
                        self.player1_1y = 1
                        self.player2_1y = 1
                        self.player1_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length-1
                        self.player2_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length_e-1
                        self.obstaculos()
                    else:
                        self.win(1)
                clock.tick(3)
                ball_x = 19
                ball_y = 12
            else:
                self.win(1)
        elif self.game_field.get_ball_direction()[0] < 0 and ball_x - 1 == -1:
            if self.game_field.get_enemy_score() < 9:
                self.game_field.set_enemy_score(self.game_field.get_enemy_score() + 1)
                start_boring_timer = time.time()
                if self.game_field.pc:
                    fail_sound.play()
                else:
                    self.game_field.levelup_animation(spec=1)
                    point_sound.play()
                ball_x = 19
                ball_y = 12
            elif self.game_field.pc:
                self.win(-1)
                clock.tick(3)
                ball_x = 19
                ball_y = 12
            else:
                self.win(-1)
        for i in self.obstaculo_list:
                if i.y == ball_y and i.x == ball_x:
                    print('here')
                if (self.game_field.get_ball_direction()[
                0] > 0 and ball_x + 1 == i.x and (
                    i.y <= ball_y <= i.y + i.height or (
                    self.game_field.get_ball_direction()[
                        1] > 0 and i.y <= ball_y + 1 <= i.y + i.height) or (
                            self.game_field.get_ball_direction()[
                                1] < 0 and i.y <= ball_y - 1 <= i.y + i.height))) or (
                self.game_field.get_ball_direction()[
                    0] < 0 and ball_x - 1 == i.x and (i.y <= ball_y <= i.y + i.height or (
                self.game_field.get_ball_direction()[
                    1] > 0 and i.y <= ball_y + 1 <= i.y + i.height) or (
                                                            self.game_field.get_ball_direction()[
                                                                1] > 0 and i.y <= ball_y + 1 <= i.y + i.height)
                )):
                    self.game_field.set_ball_direction(
                        (self.game_field.get_ball_direction()[0] * -1, random.randint(-1,1)))
                    break
        if (self.game_field.get_ball_direction()[1] > 0 and ball_y + 1 == len(self.game_field.get_matrix()) - 1) or (
                self.game_field.get_ball_direction()[1] < 0 and ball_y - 1 == 1):
            self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], self.game_field.get_ball_direction()[1] * -1))

        return ball_x, ball_y

    # Funcion encargada del rebote de la bola en bordes o en paletas. Version doubles
    # E: posicion de la bola en x, posicion de la bola en y, posicion de las paletas del jugador 1 en x y y,
    # posicion de las paletas
    # del jugador 2 en x y y.
    # S: Nueva posicion de la bola en x y y.
    # R: -
    def ball_bounce_doubles(self, ball_x, ball_y, player1_1x, player1_2x, player1_1y, player1_2y, player2_1x, player2_2x,
                            player2_1y, player2_2y):
        global start_boring_timer
        global choosed
        if (self.game_field.get_ball_direction()[0] > 0 and (
                (ball_x + 1 == player2_1x and (player2_1y <= ball_y <= player2_1y + self.game_field.paleta_length_e or (
                        self.game_field.get_ball_direction()[1] > 0 and player2_1y <= ball_y + 1 <= player2_1y) or (
                                                       self.game_field.get_ball_direction()[
                                                           1] < 0 and player2_1y <= ball_y - 1 <= player2_1y))) or (
                        ball_x + 1 == player2_2x and (player2_2y <= ball_y <= player2_2y + self.game_field.paleta_length_e or (
                        self.game_field.get_ball_direction()[1] > 0 and player2_2y <= ball_y + 1 <= player2_2y) or (
                                                              self.game_field.get_ball_direction()[
                                                                  1] < 0 and player2_2y <= ball_y - 1 <= player2_2y))))) or (
                self.game_field.get_ball_direction()[0] < 0 and (
                ball_x - 1 == player1_1x and (player1_1y <= ball_y <= player1_1y + self.game_field.paleta_length or (
                self.game_field.get_ball_direction()[1] > 0 and player1_1y <= ball_y + 1 <= player1_1y) or (
                                                      self.game_field.get_ball_direction()[
                                                          1] > 0 and player1_1y <= ball_y + 1 <= player1_2y)) or (
                        ball_x - 1 == player1_2x and (player1_2y <= ball_y <= player1_2y + self.game_field.paleta_length or (
                        self.game_field.get_ball_direction()[1] > 0 and player1_2y <= ball_y + 1 <= player2_1y) or (
                                                              self.game_field.get_ball_direction()[
                                                                  1] > 0 and player1_2y <= ball_y + 1 <= player2_1y))))):
            self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0] * -1, self.game_field.get_ball_direction()[1]))
            if self.game_field.get_ball_direction()[0] < 0 and ball_x > len(self.game_field.get_matrix()[0]) - 10:
                if player2_1y <= ball_y <= player2_1y + (self.game_field.paleta_length_e / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 1))
                    self.game_field.set_ball_velocity(30)
                elif player2_1y + self.game_field.paleta_length_e / 3 <= ball_y <= player2_1y + (
                        (2 * self.game_field.paleta_length_e) / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 0))
                    self.game_field.set_ball_velocity(40)
                elif player2_1y + (2 * self.game_field.paleta_length_e / 3) <= ball_y <= player2_1y + (( 3 * self.game_field.paleta_length_e) / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], -1))
                    self.game_field.set_ball_velocity(30)
                # Pong
                pong_sound.play()
                if self.game_field.pc:
                    choosed = False
            elif self.game_field.get_ball_direction()[0] < 0:
                if player2_2y <= ball_y <= player2_2y + (self.game_field.paleta_length_e / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 1))
                    self.game_field.set_ball_velocity(30)
                elif player2_2y + self.game_field.paleta_length_e / 3 <= ball_y <= player2_2y + (
                        (2 * self.game_field.paleta_length_e) / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 0))
                    self.game_field.set_ball_velocity(40)
                elif player2_2y + (2 * self.game_field.paleta_length_e / 3) <= ball_y <= player2_2y + ((3 * self.game_field.paleta_length_e) / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], -1))
                    self.game_field.set_ball_velocity(30)
                # Pong
                pong_sound.play()
                if self.game_field.pc:
                    choosed = False
            elif self.game_field.get_ball_direction()[0] > 0 and ball_x < 11:
                if player1_1y <= ball_y <= player1_1y + (self.game_field.paleta_length / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 1))
                    self.game_field.set_ball_velocity(30)
                elif player1_1y + self.game_field.paleta_length / 3 <= ball_y <= (
                        player1_1y + (2 * self.game_field.paleta_length) / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 0))
                    self.game_field.set_ball_velocity(40)
                elif (player1_1y + (2 * self.game_field.paleta_length / 3)) <= ball_y <= player1_1y + (
                        (3 * self.game_field.paleta_length) / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], -1))
                    self.game_field.set_ball_velocity(30)

                # Ping
                ping_sound.play()
            elif self.game_field.get_ball_direction()[0] > 0:
                if player1_2y <= ball_y <= player1_2y + (self.game_field.paleta_length / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 1))
                    self.game_field.set_ball_velocity(30)
                elif player1_2y + self.game_field.paleta_length / 3 <= ball_y <= (
                        player1_2y + (2 * self.game_field.paleta_length) / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 0))
                    self.game_field.set_ball_velocity(40)
                elif (player1_2y + (2 * self.game_field.paleta_length / 3)) <= ball_y <= player1_2y + (
                        (3 * self.game_field.paleta_length) / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], -1))
                    self.game_field.set_ball_velocity(30)
                # Ping
                ping_sound.play()

        elif self.game_field.get_ball_direction()[0] > 0 and ball_x + 1 == len(self.game_field.get_matrix()[0]) + 1:
            if self.game_field.get_friend_score() < 9:
                self.game_field.set_friend_score(self.game_field.get_friend_score() + 1)
                point_sound.play()
                start_boring_timer = time.time()
                ball_x = 19
                ball_y = 12
                if self.game_field.pc:
                    choosed = False
                else:
                    self.game_field.levelup_animation(spec=1)
            else:
                if self.game_field.pc:
                    self.game_field.reset_scores()
                    lvlup = self.game_field.levelup_animation()
                    if lvlup:
                        self.message_to_screen('Level Up!!', self.color, size='large')
                        self.player1_1y = 1
                        self.player2_1y = 1
                        self.player1_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length-1
                        self.player2_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length_e-1
                        self.obstaculos()
                    else:
                        self.win(1)
                else:
                    self.win(1)
                clock.tick(3)
                ball_x = 19
                ball_y = 12
        elif self.game_field.get_ball_direction()[0] < 0 and ball_x - 1 == -1:
            if self.game_field.get_enemy_score() < 9:
                self.game_field.set_enemy_score(self.game_field.get_enemy_score() + 1)
                if self.game_field.pc:
                    fail_sound.play()
                else:
                    start_boring_timer = time.time()
                    self.game_field.levelup_animation(spec=1)
                    point_sound.play()
                start_boring_timer = time.time()
                ball_x = 19
                ball_y = 12
            else:
                if self.game_field.pc:
                    self.win(-1)
                else:
                    self.win(-1)
                clock.tick(3)
                ball_x = 19
                ball_y = 12
        for i in self.obstaculo_list:
            if i.y == ball_y and i.x == ball_x:
                print('here')
            if (self.game_field.get_ball_direction()[
                    0] > 0 and ball_x + 1 == i.x and (
                        i.y <= ball_y <= i.y + i.height or (
                        self.game_field.get_ball_direction()[
                            1] > 0 and i.y <= ball_y + 1 <= i.y + i.height) or (
                                self.game_field.get_ball_direction()[
                                    1] < 0 and i.y <= ball_y - 1 <= i.y + i.height))) or (
                    self.game_field.get_ball_direction()[
                        0] < 0 and ball_x - 1 == i.x and (i.y <= ball_y <= i.y + i.height or (
                    self.game_field.get_ball_direction()[
                        1] > 0 and i.y <= ball_y + 1 <= i.y + i.height) or (
                                                                  self.game_field.get_ball_direction()[
                                                                      1] > 0 and i.y <= ball_y + 1 <= i.y + i.height)
                    )):
                self.game_field.set_ball_direction(
                    (self.game_field.get_ball_direction()[0] * -1, random.randint(-1, 1)))
                break
        if (self.game_field.get_ball_direction()[1] > 0 and ball_y + 1 == len(self.game_field.get_matrix()) - 1) or (
                self.game_field.get_ball_direction()[1] < 0 and ball_y - 1 == 1):
            self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], self.game_field.get_ball_direction()[1] * -1))

        return ball_x, ball_y

    # Funcion encargada de renderizar el texto a poner en la pantalla, recibe un texto, un color y un tamanno y retorna
    # el texto renderizado asi como el punto central del mismo.
    def text_objects(self, text, color, size):
        if size == 'small':
            textSurface = smallfont.render(text, True, color)
        if size == 'medium':
            textSurface = mediumfont.render(text, True, color)
        elif size == 'large':
            textSurface = largefont.render(text, True, color)
        return textSurface, textSurface.get_rect()

    # Dado un mensaje, un color, un desplazamiento del centro de la pantalla en x, un desplazamiento del centor de la pantalla
    # en y y un tamanno de los ya predeterminados, este funcion muestra un texto en la pantalla.
    def message_to_screen(self, msg, color,x_displace=0, y_displace=0, size='small'):
        textSurf, textRect = self.text_objects(msg, color, size)
        textRect.center = (self.game_field.width/2) + x_displace, (self.game_field.height/2) + y_displace
        self.game_field.gameDisplay.blit(textSurf, textRect)

    def win(self, winner):
        global botones1
        win_screen = True
        x_displace_fromcenter = winner*200
        cont = False
        while win_screen:
            for i in range(len(self.game_field.game_matrix)):
                for j in range(len(self.game_field.game_matrix[0])):
                    if i != 0 and i != 24 and i % 2 == 0 and j == 19:
                        self.game_field.game_matrix[i][j] = False
            self.game_field.screen()
            self.message_to_screen('You', self.color, size='large', x_displace=-x_displace_fromcenter, y_displace=-50)
            self.message_to_screen('won!', self.color, size='large', x_displace=-x_displace_fromcenter, y_displace=40)
            self.message_to_screen('You', self.color, size='large', x_displace=x_displace_fromcenter, y_displace=-50)
            self.message_to_screen('lose!',self.color, size='large', x_displace=x_displace_fromcenter, y_displace=40)
            self.message_to_screen('Press enter to play again', self.color, y_displace=200)
            self.message_to_screen('or space to return to main menu', self.color, y_displace=250)
            if self.pc and winner == 1 and not cont:
                self.verify()
                cont = True

            # Reconocimiento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    placa1.exit()
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.__init__(self.mode, self.pc, self.mute, self.practice, self.color)
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_RETURN:
                        self.__init__(self.mode, self.pc, self.mute, self.practice, self.color)
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_SPACE:
                        placa1.exit()
                        pygame.quit()
                        quit()

            if botones1[6].read() == 1.0:
                placa1.exit()
                pygame.quit()
                quit()
            elif botones1[1].read():
                self.__init__(self.mode, self.pc, self.mute, self.practice, self.color)
                pygame.quit()
                quit()


            pygame.display.update()


    def verify(self):
        self.file = open(self.path, 'w')
        name = 'alv'
        cont = False
        for line in self.final:
            if int(self.time_playing/1000) < int(line[1]) and not cont:
                self.file.write(name+'%'+str(self.time_playing/1000)+'\n')
                cont = True
            else:
                self.file.write(line[0]+'%'+str(line[1])+'\n')

    def obstaculos(self):
        matrix = self.game_field.get_matrix()
        if self.game_field.level == 1:
            for i in range(1):
                self.obstaculo_list.append('')
            for i in range(1):
                self.obstaculo_list[i] = Obstaculo(random.randint(15,25), random.randint(1,23), 2, 2)
        elif self.game_field.level == 2:
            for i in range(2):
                self.obstaculo_list.append('')
            for i in range(2):
                self.obstaculo_list[i] = Obstaculo(random.randint(15,25), random.randint(1,23), 2, 2)
        else:
            for i in range(3):
                self.obstaculo_list.append('')
            for i in range(3):
                self.obstaculo_list[i] = Obstaculo(random.randint(15,25), random.randint(1,23), 2, 2)

    def start_server(self, client1_ip, client2_ip):
        self.client1 = Client((client1_ip, 1235))
        self.client1.send(['server-client', 1234])
        self.listener1 = Listener(('', 1234))
        self.conn1 = self.listener1.accept()
        msg = self.conn1.recv()
        while msg != 'client-server':
            pass
        setups = [1, self.mode, self.pc]
        self.client1.send(setups)
        print('Connected to first player')
        self.client2 = Client((client2_ip, 1237))
        self.client2.send(['server-client',1236])
        self.listener2 = Listener(('', 1236))
        self.conn2 = self.listener2.accept()
        msg = self.conn2.recv()
        while msg != 'client-server':
            pass
        setups = [2, self.mode, self.pc]
        self.client2.send(setups)
        print('Connected to second player')
        print('Connection stablished')

    def send_matrix(self, matrix):
        if self.client1 != None and self.client2 != None:
            self.client1.send(matrix)
            self.client2.send(matrix)

    def juntar(self, lista1, lista2):
        for i in lista2:
            lista1.append(i)
        return lista1


def arduino1_setup():
    global placa1, botones1, display1_leds
    placa1 = pyfirmata.Arduino('/dev/ttyACM0')
    pyfirmata.util.Iterator(placa1).start()

    botones1 = []

    botones1.append(placa1.get_pin('d:10:i')) # boton arriba
    botones1.append(placa1.get_pin('d:11:i')) # boton select
    botones1.append(placa1.get_pin('d:12:i')) # boton abajo
    botones1.append(placa1.get_pin('a:4:i')) # boton verde
    botones1.append(placa1.get_pin('a:3:i')) # boton blanco
    botones1.append(placa1.get_pin('a:2:i')) # boton pausa
    botones1.append(placa1.get_pin('a:0:i')) # boton back
    botones1.append(placa1.get_pin('a:1:i')) # boton inspector
    botones1.append(placa1.get_pin('a:5:i')) # boton mute


    for i in botones1:
        i.enable_reporting()

    display1_leds = [0,1,2,3,4,5,6,7,8]

    display1_leds[0] = placa1.get_pin('d:9:o')
    display1_leds[1] = placa1.get_pin('d:8:o')
    display1_leds[2] = placa1.get_pin('d:5:o')
    display1_leds[3] = placa1.get_pin('d:6:o')
    display1_leds[4] = placa1.get_pin('d:7:o')
    display1_leds[5] = placa1.get_pin('d:2:o')
    display1_leds[6] = placa1.get_pin('d:3:o')
    display1_leds[7] = placa1.get_pin('d:13:o')

for i in sys.argv:
    print(i)
Game(sys.argv[1], bool(sys.argv[2]), bool(sys.argv[3]), bool(sys.argv[4]), sys.argv[5], sys.argv[6])
global placa
# Finalizacion del juego
placa1.exit()
pygame.quit()
quit()
