import pygame
import random
import mutagen.oggvorbis
import time
import sys
import os

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


white = (255,255,255)
import random
import mutagen.oggvorbis
import time


pausa=False

# Colores importantes
white = (255, 255, 255)
black = (0, 0, 0)


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
    def __init__(self, PC, block_width, block_height):
        # Atributos
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
        self.level = 1
        self.ball_velocity = 30 + 3*(self.level-1)
        self.ball_direction = (-1, 0)
        self.pc = PC
        self.paleta_length = 9 - (3*(self.level-1))
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
        if self.level == 1:
            music_file = 'sounds/lvl1.ogg'
        elif self.level == 2:
            music_file = 'sounds/Shadowblaze-ChampionBattle.ogg'
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
                    pygame.draw.rect(self.gameDisplay,white,[m*self.block_width, n*self.block_height,
                                                             self.block_width, self.block_height])
                else:
                    pygame.draw.rect(self.gameDisplay, black, [m * self.block_width, n * self.block_height,
                                                               self.block_width, self.block_height])

    # funcion encargada de escribir el score del jugador 1 en la matriz de juego
    def score_f(self):
        if self.friend_score == 0:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix)):
                    if (m == 15 and 2 <= n <= 6) or (n == 2 and 13 <= m <= 15) or (m == 13 and 2 <= n <= 5) or (n == 6 and 13 <= m <= 15):
                        self.game_matrix[n][m] = True
        elif self.friend_score == 1:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix)):
                    if (m == 15 and 2 <= n <= 6):
                        self.game_matrix[n][m] = True
        elif self.friend_score == 2:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 13 <= m <= 15) or (m == 15 and n == 3) or (m == 13 and n == 5) :
                        self.game_matrix[n][m] = True
        elif self.friend_score == 3:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 13 <= m <= 15) or (m == 15 and n == 5) or (m == 15 and n == 3):
                        self.game_matrix[n][m] = True
        elif self.friend_score == 4:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 15 and 2 <= n <= 6) or (m == 13 and 2 <= n <= 4) or (m == 14 and n == 4):
                        self.game_matrix[n][m] = True
        elif self.friend_score == 5:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 13 <= m <= 15) or (m == 15 and n == 5) or (m == 13 and n == 3):
                        self.game_matrix[n][m] = True
        elif self.friend_score == 6:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 13 <= m <= 15) or (m == 13 and n == 5)or (m == 15 and n == 5) or (m == 13 and n == 3):
                        self.game_matrix[n][m] = True
        elif self.friend_score == 7:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 15 and 2 <= n <= 6) or ((m == 14 or m == 13) and n == 2):
                        self.game_matrix[n][m] = True
        elif self.friend_score == 8:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 13 <= m <= 15) or ((m == 15 or m == 13) and (n == 3 or n == 5)):
                        self.game_matrix[n][m] = True
        elif self.friend_score == 9:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 15 and 2 <= n <= 6) or (m == 13 and 2 <= n <= 4) or (m == 14 and n == 4) or (m == 14 and n == 2):
                        self.game_matrix[n][m] = True
        elif self.friend_score == 10:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix)):
                    if (m == 11 and 2 <= n <= 6) or (m == 15 and 2 <= n <= 6) or (n == 2 and 13 <= m <= 15) or (m == 13 and 2 <= n <= 5) or (n == 6 and 13 <= m <= 15):
                        self.game_matrix[n][m] = True

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
        elif self.enemy_score == 10:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 23 and 2 <= n <= 6) or (m == 25 and 2 <= n <= 6) or (n == 2 and 25 <= m <= 27) or (m == 27 and 2 <= n <= 6) or (n == 6 and 25 <= m <= 27):
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
    def pause(self):
        pause = True
        for n in range(len(self.game_matrix)):
            for m in range(len(self.game_matrix)):
                if n % 2  == 0 and m == 19 and n != 0 and n != 24:
                    self.game_matrix[n][m] = False
            self.screen()
            pygame.display.update()

        while pause:
            pygame.mixer.music.pause()
            self.message_to_screen('Juego pausado', white, size='large')
            self.message_to_screen('Presione p para reanudar', white, y_displace=80)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pygame.mixer.music.unpause()
                        pause = False
                elif event.type == pygame.QUIT:
                    quit()

            pygame.display.update()

        for n in range(len(self.game_matrix)):
            for m in range(len(self.game_matrix)):
                if n % 2  == 0:
                    self.game_matrix[n][m] = True

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
                self.message_to_screen('A new challenger', white, size='medium')
                self.message_to_screen('has arrived', white, size='medium', y_displace=40)
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


class Game:
    global mode
    def __init__(self, MODE, PC):
        global choosed
        global start_boring_timer
        print(PC)

        # Instancia del Tablero
        self.game_field = Tablero(bool(PC), block_height, block_width)
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
        self.player2_2y = len(self.game_field.get_matrix()) - 1 - self.game_field.paleta_length

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

        # Controlan el juego
        self.game = True
        self.pause = False

        self.mode = MODE
        self.pc = bool(PC)

        self.gameloop(MODE)

    def gameloop(self, mode):
        global start_boring_timer
        global choosed
        self.choosed = False
        start_boring_timer = time.time()
        if mode == 'singles':
            self.singles()
        elif mode == 'doubles':
            self.doubles()
        else:
            return 'Err'

    def singles(self):
        global start_boring_timer
        global choosed
        while self.game:

            # Reconocimiento de eventos

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
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.player1_1up_y = False
                    elif event.key == pygame.K_DOWN:
                        self.player1_1down_y = False
                    elif event.key == pygame.K_w:
                        self.player2_1up_y = False
                    elif event.key == pygame.K_s:
                        self.player2_1down_y = False

            # Movimiento de las paletas del primer jugador
            if self.player1_1down_y and self.player1_1y + self.game_field.paleta_length + 1 < len(self.game_field.get_matrix()):
                self.player1_1y += 1
            elif self.player1_1up_y and self.player1_1y+1 > 2:
                self.player1_1y -= 1

            # Movimiento de las paletas del segundo jugador
            if self.player2_1down_y and self.player2_1y + self.game_field.paleta_length + 1 < len(self.game_field.get_matrix()):
                self.player2_1y += 1
            elif self.player2_1up_y and self.player2_1y+1 > 2:
                self.player2_1y -= 1

            # Rebote de la pelota
            self.ball_x, self.ball_y = self.ball_bounce_singles(self.ball_x,self.ball_y,self.player1_1x,self.player1_1y,self.player2_1x,self.player2_1y)
            # Sube la dificultad si no hay goles
            if time.time() - start_boring_timer > 10 and not self.game_field.pc:
                self.game_field.levelup_animation()
                self.message_to_screen('Level Up!!', white, size = 'large')
                self.player1_1y = 1
                self.player2_2y = 1
                self.player1_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length-1
                self.player2_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length-1
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
            self.player2.mod_matrix(matrix, self.game_field.paleta_length)
            self.game_field.set_matrix(matrix)
            self.game_field.screen()
            if self.game_field.pc:
                self.message_to_screen('Press w to add a new player', white, 200, 250)
            pygame.display.update()

            # Controla la velocidad
            clock.tick(self.game_field.get_ball_velocity())

    def doubles(self):
        global start_boring_timer
        global choosed
        while self.game:

            # Reconocimiento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player1_1up_y = True
                    elif event.key == pygame.K_DOWN:
                        self.player1_1down_y = True
                    elif event.key == pygame.K_w and not self.game_field.pc:
                        self.player2_1up_y = True
                    elif event.key == pygame.K_w:
                        self.game_field.pc = False
                        self.game_field.reset_level()
                        self.game_field.new_player()
                        self.game_field.reset_scores()
                        start_boring_timer = time.time()

                    elif event.key == pygame.K_s and not self.game_field.pc:
                        self.player2_1down_y = True
                    elif event.key == pygame.K_p:
                        self.game_field.pause()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.player1_1up_y = False
                    elif event.key == pygame.K_DOWN:
                        self.player1_1down_y = False
                    elif event.key == pygame.K_w:
                        self.player2_1up_y = False
                    elif event.key == pygame.K_s:
                        self.player2_1down_y = False

            # Movimiento de las paletas del primer jugador
            if self.player1_1down_y and self.player1_1y + self.game_field.paleta_length + 1 < len(self.game_field.get_matrix()):
                self.player1_1y += 1
                self.player1_2y -= 1
            elif self.player1_1up_y and self.player1_1y+1 > 2:
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
            self.ball_x, self.ball_y = self.ball_bounce_doubles(self.ball_x,self.ball_y,self.player1_1x, self.player1_2x,self.player1_1y, self.player1_2y, self.player2_1x, self.player2_2x,
                                                 self.player2_1y, self.player2_2y)

            # Sube la dificultad si no hay goles
            if time.time() - start_boring_timer > 10 and not self.game_field.pc:
                self.game_field.levelup_animation()
                self.message_to_screen('Level Up!!', white, size = 'large')
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
            self.player2_2.mod_matrix(matrix, self.game_field.paleta_length)
            self.player2_1.mod_matrix(matrix, self.game_field.paleta_length)
            self.player1_2.mod_matrix(matrix, self.game_field.paleta_length)
            self.game_field.set_matrix(matrix)
            self.game_field.screen()
            if self.game_field.pc:
                self.message_to_screen('Press w to add a new player', white, 200, 250)
            pygame.display.update()

            # Se controla la velocidad
            clock.tick(self.game_field.get_ball_velocity())

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
                    player2_1y <= ball_y <= player2_1y + self.game_field.paleta_length or (
                    self.game_field.get_ball_direction()[
                        1] > 0 and player2_1y <= ball_y + 1 <= player2_1y + self.game_field.paleta_length) or (
                            self.game_field.get_ball_direction()[
                                1] < 0 and player2_1y <= ball_y - 1 <= player2_1y + self.game_field.paleta_length))) or (
                self.game_field.get_ball_direction()[
                    0] < 0 and ball_x - 1 == 0 and (player1_1y <= ball_y <= player1_1y + self.game_field.paleta_length or (
                self.game_field.get_ball_direction()[
                    1] > 0 and player1_1y <= ball_y + 1 <= player1_1y + self.game_field.paleta_length) or (
                                                            self.game_field.get_ball_direction()[
                                                                1] > 0 and player1_1y <= ball_y + 1 <= player1_1y + self.game_field.paleta_length)
                )):

            self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0] * -1, self.game_field.get_ball_direction()[1]))

            if self.game_field.get_ball_direction()[0] < 0:
                if player2_1y <= ball_y <= player2_1y + self.game_field.paleta_length / 3 -1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 1))
                    self.game_field.set_ball_velocity(self.game_field.ball_velocity)
                elif player2_1y + self.game_field.paleta_length / 3 <= ball_y <= player2_1y + (
                        2 * self.game_field.paleta_length) / 3 -1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 0))
                    self.game_field.set_ball_velocity(self.game_field.ball_velocity)
                elif player2_1y + (2 * self.game_field.paleta_length / 3) <= ball_y <= player2_1y + (
                        3 * self.game_field.paleta_length) / 3 -1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], -1))
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
            if self.game_field.get_friend_score() < 10:
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
                        self.message_to_screen('Level Up!!', white, size='large')
                        self.player1_1y = 1
                        self.player2_1y = 1
                        self.player1_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length-1
                        self.player2_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length-1
                    else:
                        self.win(1)
                clock.tick(3)
                ball_x = 19
                ball_y = 12
            else:
                self.win(1)
        elif self.game_field.get_ball_direction()[0] < 0 and ball_x - 1 == -1:
            if self.game_field.get_enemy_score() < 10:
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
                (ball_x + 1 == player2_1x and (player2_1y <= ball_y <= player2_1y + self.game_field.paleta_length or (
                        self.game_field.get_ball_direction()[1] > 0 and player2_1y <= ball_y + 1 <= player2_1y) or (
                                                       self.game_field.get_ball_direction()[
                                                           1] < 0 and player2_1y <= ball_y - 1 <= player2_1y))) or (
                        ball_x + 1 == player2_2x and (player2_2y <= ball_y <= player2_2y + self.game_field.paleta_length or (
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
                if player2_1y <= ball_y <= player2_1y + (self.game_field.paleta_length / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 1))
                    self.game_field.set_ball_velocity(30)
                elif player2_1y + self.game_field.paleta_length / 3 <= ball_y <= player2_1y + (
                        (2 * self.game_field.paleta_length) / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 0))
                    self.game_field.set_ball_velocity(40)
                elif player2_1y + (2 * self.game_field.paleta_length / 3) <= ball_y <= player2_1y + (( 3 * self.game_field.paleta_length) / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], -1))
                    self.game_field.set_ball_velocity(30)
                # Pong
                pong_sound.play()
                if self.game_field.pc:
                    choosed = False
            elif self.game_field.get_ball_direction()[0] < 0:
                if player2_2y <= ball_y <= player2_2y + (self.game_field.paleta_length / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 1))
                    self.game_field.set_ball_velocity(30)
                elif player2_2y + self.game_field.paleta_length / 3 <= ball_y <= player2_2y + (
                        (2 * self.game_field.paleta_length) / 3) - 1:
                    self.game_field.set_ball_direction((self.game_field.get_ball_direction()[0], 0))
                    self.game_field.set_ball_velocity(40)
                elif player2_2y + (2 * self.game_field.paleta_length / 3) <= ball_y <= player2_2y + ((3 * self.game_field.paleta_length) / 3) - 1:
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
            if self.game_field.get_friend_score() < 10:
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
                        self.message_to_screen('Level Up!!', white, size='large')
                        self.player1_1y = 1
                        self.player2_1y = 1
                        self.player1_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length-1
                        self.player2_2y = len(self.game_field.get_matrix())-self.game_field.paleta_length-1
                    else:
                        self.win(1)
                else:
                    self.win(1)
                clock.tick(3)
                ball_x = 19
                ball_y = 12
        elif self.game_field.get_ball_direction()[0] < 0 and ball_x - 1 == -1:
            if self.game_field.get_enemy_score() < 10:
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
        win_screen = True
        x_displace_fromcenter = winner*200
        while win_screen:
            for i in range(len(self.game_field.game_matrix)):
                for j in range(len(self.game_field.game_matrix[0])):
                    if i != 0 and i != 24 and i % 2 == 0 and j == 19:
                        self.game_field.game_matrix[i][j] = False
            self.game_field.screen()
            self.message_to_screen('You', white, size='large', x_displace=-x_displace_fromcenter, y_displace=-50)
            self.message_to_screen('won!', white, size='large', x_displace=-x_displace_fromcenter, y_displace=40)
            self.message_to_screen('You', white, size='large', x_displace=x_displace_fromcenter, y_displace=-50)
            self.message_to_screen('lose!', white, size='large', x_displace=x_displace_fromcenter, y_displace=40)
            self.message_to_screen('Press enter to play again', white, y_displace=200)
            self.message_to_screen('or space to return to main menu', white, y_displace=250)

            # Reconocimiento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_RETURN:
                        self.__init__(self.mode, self.pc)
                    elif event.key == pygame.K_SPACE:
                        pygame.quit()
                        quit()

            pygame.display.update()

Game(sys.argv[1], bool(sys.argv[2]))

# Finalizacion del juego
pygame.quit()
quit()
