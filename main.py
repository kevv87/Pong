import pygame
import random

# Inicializacion de pygame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# Colores importantes
white = (255, 255, 255)
black = (0, 0, 0)

# Sonidos
pong_sound = pygame.mixer.Sound('sounds/pong.wav')
ping_sound = pygame.mixer.Sound('sounds/ping.wav')

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
    def __init__(self, PC, block_width, block_height, SINGLES, DOUBLES):
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
        self.level = 3
        self.ball_velocity = 30*self.level
        self.ball_direction = (-1, 0)
        self.pc = PC
        self.paleta_length = 9 - 3*(self.level-1)
        self.singles = SINGLES
        self.doubles = DOUBLES

    # Metodos

    # Constructor de la matriz
    def matrix_constructor(self):
        for n in range(25):
            self.game_matrix.append([])
            for m in range(40):
                self.game_matrix[n].append(False)
        self.game_matrix = self.game_matrix[:len(self.game_matrix)-1]

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


    def lose(self):
        pass

    def win(self):
        pass

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
            message_to_screen('Juego pausado', white, size='large')
            message_to_screen('Presione p para reanudar', white, y_displace=80)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
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
                message_to_screen('A new challenger', white, size='medium')
                message_to_screen('has arrived', white, size='medium', y_displace=40)
            pygame.display.update()

    # Devuelve los marcadores a 0
    def reset_scores(self):
        self.enemy_score = 0
        self.friend_score = 0
        self.screen()


game_field = Tablero(True, block_height, block_width, True, False)


# Clase encargada de guardar la posicion de la bola y modificar la matriz del juego conforme a la misma
class Bola:
    def __init__(self, pos_x, pos_y, block_width, block_height):
        self.width = block_width
        self.height = block_height
        self.x = pos_x
        self.y = pos_y
        self.mod_matrix()

    # Modifica la matriz del juego segun la posicion de la bola
    def mod_matrix(self):
        matrix = game_field.get_matrix()
        for n in range(len(matrix)):
            for m in range(len(matrix[0])):
                if m == self.x and n == self.y:
                    matrix[n][m] = True
        game_field.set_matrix(matrix)


# Clase encargada de guardar la posicion de cada paleta y modificar la matriz del juego segun la misma y su longitud
class Paleta:
    def __init__(self, pos_x, pos_y, block_width, block_height):
        self.width = block_width
        self.height = block_height
        self.x = pos_x
        self.y = pos_y
        self.mod_matrix()

    # modifica la matriz del juego segun la posicion de la paleta y su longitud
    def mod_matrix(self):
        matrix = game_field.get_matrix()
        for n in range(len(matrix)):
            for m in range(len(matrix[0])):
                if m == self.x and n == self.y:
                    for i in range(game_field.paleta_length):
                        if n+i <=len(game_field.get_matrix())-1:
                            matrix[n+i][m] = True
        game_field.set_matrix(matrix)



# Gameloop, recibe el modo de juego que se esta llevando a cabo.
def gameloop(singles, doubles):
    # Posiciones iniciales de los jugadores

    # Primeras paletas
    player1_1x = 0
    player1_1y = 1
    player2_1x = len(game_field.get_matrix()[0])-1
    player2_1y = 1
    # Segundas paletas
    player1_2x = 11
    player1_2y = (len(game_field.get_matrix())-game_field.paleta_length)-1
    player2_2x = len(game_field.get_matrix()[0]) - 11
    player2_2y = len(game_field.get_matrix())-1-game_field.paleta_length

    # Controlan el movimiento de los jugadores

    # Primeras paletas
    player1_2down_y = False
    player1_2up_y = False
    player2_2up_y = False
    player2_2down_y = False

    # Segundas paletas
    player1_1down_y = False
    player1_1up_y = False
    player2_1up_y = False
    player2_1down_y = False

    ball_x = 19
    ball_y = 12

    # Controlan el juego
    game = True
    pause = False


    while game:

        # Modo singles
        while singles:

            # Reconocimiento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    singles = False
                    game = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player1_1up_y = True
                    elif event.key == pygame.K_DOWN:
                        player1_1down_y = True
                    elif event.key == pygame.K_w and not game_field.pc:
                        player2_1up_y = True
                    elif event.key == pygame.K_w:
                        game_field.pc = False
                        game_field.new_player()
                        game_field.reset_scores()
                    elif event.key == pygame.K_s and not game_field.pc:
                        player2_1down_y = True
                    elif event.key == pygame.K_p:
                        game_field.pause()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        player1_1up_y = False
                    elif event.key == pygame.K_DOWN:
                        player1_1down_y = False
                    elif event.key == pygame.K_w:
                        player2_1up_y = False
                    elif event.key == pygame.K_s:
                        player2_1down_y = False

            # Movimiento de las paletas del primer jugador
            if player1_1down_y and player1_1y + game_field.paleta_length + 1 < len(game_field.get_matrix()):
                player1_1y += 1
            elif player1_1up_y and player1_1y+1 > 2:
                player1_1y -= 1

            # Movimiento de las paletas del segundo jugador
            if player2_1down_y and player2_1y + game_field.paleta_length + 1 < len(game_field.get_matrix()):
                player2_1y += 1
            elif player2_1up_y and player2_1y+1 > 2:
                player2_1y -= 1

            # Rebote de la pelota
            ball_x, ball_y = ball_bounce_singles(ball_x,ball_y,player1_1x,player1_1y,player2_1x,player2_1y)

            # Inteligencia artificial cuando la pc esta habilitada
            if game_field.pc and game_field.get_ball_direction()[0] > 0:
                if ball_x == 1 or ball_x == 20:
                    choice_hit = random.choice([-1, 0, 1])
                    y_hit = simulacion(ball_x, ball_y, game_field.get_ball_direction()[1]) + random.randint(-int(game_field.paleta_length/2)+2, 2+int(game_field.paleta_length/2))
                    while not 0 <= y_hit < 24:
                        y_hit = simulacion(ball_x, ball_y, game_field.get_ball_direction()[1]) + random.randint(
                            -int(game_field.paleta_length / 2) + 1, 1 + int(game_field.paleta_length / 2))


                if choice_hit == -1:
                    if y_hit < player2_1y and player2_1y-1 >= 1:
                       nxt_move = -1
                    elif y_hit > player2_1y and player2_1y + int(game_field.paleta_length+1) <= 24:
                        nxt_move = 1
                    elif y_hit == player2_1y:
                        nxt_move = 0
                    else:
                        nxt_move = 0
                elif choice_hit == 0:
                    if y_hit < player2_1y + int(game_field.paleta_length+1)/2 -1 and player2_1y-1 >= 1:
                        nxt_move = -1
                    elif y_hit > player2_1y + int(game_field.paleta_length+1)/2 -1 and player2_1y + int(game_field.paleta_length+1) <= 24:
                        nxt_move = 1
                    elif y_hit == player2_1y + int(game_field.paleta_length+1)/2 -1:
                        nxt_move = 0
                    else:
                        nxt_move = 0
                elif choice_hit == 1:
                    if y_hit < player2_1y + int(game_field.paleta_length) -1 and player2_1y-1 >= 1:
                        nxt_move = -1
                    elif y_hit > player2_1y + int(game_field.paleta_length) -1 and player2_1y + int(game_field.paleta_length+1) <= 24:
                        nxt_move = 1
                    elif y_hit == player2_1y + int(game_field.paleta_length) -1:
                        nxt_move = 0
                    else:
                        nxt_move = 0
                print(player2_1y)

                player2_1y += nxt_move

            # Se realizan los movimientos y se modifica la pantalla
            game_field.clean_matrix()
            ball_x += 1 * game_field.get_ball_direction()[0]
            ball_y += 1 * game_field.get_ball_direction()[1]
            bola = Bola(ball_x, ball_y, block_width, block_height)
            player1 = Paleta(player1_1x, player1_1y, block_width, block_height)
            player2 = Paleta(player2_1x, player2_1y, block_width, block_height)
            game_field.screen()
            if game_field.pc:
                message_to_screen('Press w to add a new player', white, 200, 250)
            pygame.display.update()

            # Controla la velocidad
            clock.tick(game_field.get_ball_velocity())

        # Modo doubles
        while doubles:

            # Reconocimiento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    doubles = False
                    game = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player1_1up_y = True
                    elif event.key == pygame.K_DOWN:
                        player1_1down_y = True
                    elif event.key == pygame.K_w and not game_field.pc:
                        player2_1up_y = True
                    elif event.key == pygame.K_w:
                        game_field.pc = False
                        game_field.new_player()
                        game_field.reset_scores()
                    elif event.key == pygame.K_s and not game_field.pc:
                        player2_1down_y = True
                    elif event.key == pygame.K_p:
                        game_field.pause()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        player1_1up_y = False
                    elif event.key == pygame.K_DOWN:
                        player1_1down_y = False
                    elif event.key == pygame.K_w:
                        player2_1up_y = False
                    elif event.key == pygame.K_s:
                        player2_1down_y = False

            # Movimiento de las paletas del primer jugador
            if player1_1down_y and player1_1y + game_field.paleta_length + 1 < len(game_field.get_matrix()):
                player1_1y += 1
                player1_2y -= 1
            elif player1_1up_y and player1_1y+1 > 2:
                player1_1y -= 1
                player1_2y += 1

            # Movimiento de las paletas del segundo jugador
            if player2_1down_y and player2_1y + game_field.paleta_length + 1 < len(game_field.get_matrix()):
                player2_1y += 1
                player2_2y -= 1
            elif player2_1up_y and player2_1y+1 > 2:
                player2_1y -= 1
                player2_2y += 1

            # Movimiento de la bola
            ball_x, ball_y = ball_bounce_doubles(ball_x,ball_y,player1_1x, player1_2x, player1_1y, player1_2y, player2_1x, player2_2x,
                                                 player2_1y, player2_2y)

            # Inteligencia artificial
            if game_field.pc and game_field.get_ball_direction()[0] > 0:
                nxt_move = 0
                found = False
                if ball_x < len(game_field.get_matrix()[0]) - 11:
                    if ball_x == 1 or ball_x == 20 or ball_x == 12:
                        y_hit = simulacion_2nd(ball_x, ball_y, game_field.get_ball_direction()[1]) + random.randint(-int(game_field.paleta_length/2)+2, 2+int(game_field.paleta_length/2))
                        while not 2 <= y_hit < 24:
                            y_hit = simulacion(ball_x, ball_y, game_field.get_ball_direction()[1]) + random.randint(
                                -int(game_field.paleta_length / 2) + 1, 1 + int(game_field.paleta_length / 2))

                    while not found:
                        nxt_move = random.choice([1, -1])
                        if len(game_field.get_matrix()[0])-1-ball_x > abs(
                                y_hit-((player2_1y+int(game_field.paleta_length/2)+random.randint(-1,1)) + nxt_move)) and (
                                player2_1y + game_field.paleta_length +nxt_move <= len(game_field.get_matrix())+1) and (
                                player2_1y + nxt_move > 0):
                            found = True

                else:
                    found = False
                    if ball_x == 1 or ball_x == 20:
                        y_hit = simulacion(ball_x, ball_y, game_field.get_ball_direction()[1]) + random.randint(
                            -int(game_field.paleta_length / 2) + 2, 2 + int(game_field.paleta_length / 2))
                        while not 2 <= y_hit < 24:
                            y_hit = simulacion(ball_x, ball_y, game_field.get_ball_direction()[1]) + random.randint(
                                -int(game_field.paleta_length / 2) + 1, 1 + int(game_field.paleta_length / 2))

                    while not found:
                        nxt_move = random.choice([1, -1])
                        if len(game_field.get_matrix()[0]) - 1 - ball_x > abs(
                                y_hit - ((player2_1y + int(game_field.paleta_length / 2) + random.randint(-1,
                                                                                                          1)) + nxt_move)) and (
                                player2_1y + game_field.paleta_length + nxt_move <= len(game_field.get_matrix()) + 1) and (
                                player2_1y + nxt_move > 0):
                            found = True



                player2_1y += nxt_move
                player2_2y -= nxt_move

            # Se realizan los movimientos y se modifica la pantalla
            game_field.clean_matrix()
            ball_x += 1 * game_field.get_ball_direction()[0]
            ball_y += 1 * game_field.get_ball_direction()[1]
            bola = Bola(ball_x, ball_y, block_width, block_height)
            player1_1 = Paleta(player1_1x, player1_1y, block_width, block_height)
            player2_1 = Paleta(player2_1x, player2_1y, block_width, block_height)
            player1_2 = Paleta(player1_2x, player1_2y, block_width, block_height)
            player1_2 = Paleta(player2_2x, player2_2y, block_width, block_height)
            game_field.screen()
            if game_field.pc:
                message_to_screen('Press w to add a new player', white, 200, 250)
            pygame.display.update()

            # Se controla la velocidad
            clock.tick(game_field.get_ball_velocity())

# Funcion recursiva encargada de simular el movimiento de la bola dadas una pos inicial en x y y y una direccion hacia
# donde se mueve la misma. Retorna la posicion en y donde va a pegar la bola al lado derecho. Se utiliza para la inteligencia
# artificial. Version singles.
def simulacion(pos_x, pos_y, direction):
    if direction == 0:
        return pos_y
    elif pos_x == 39:
        return pos_y
    elif pos_y == 1:
        return simulacion(pos_x, pos_y+1, direction*-1)
    elif pos_y == 23:
        return simulacion(pos_x, pos_y-1, direction*-1)
    elif direction == 1:
        return simulacion(pos_x+1, pos_y+1, direction)
    elif direction == -1:
        return simulacion(pos_x+1, pos_y-1, direction)

# Funcion recursiva encargada de simular el movimiento de la bola dadas una pos inicial en x y y y una direccion hacia
# donde se mueve la misma. Retorna la posicion en y donde va a pegar la bola al lado derecho. Se utiliza para la inteligencia
# artificial. Version doubles.
def simulacion_2nd(pos_x, pos_y, direction):
    if direction == 0:
        return pos_y
    elif pos_x == len(game_field.get_matrix()[0]) - 11:
        return pos_y
    elif pos_y == 1:
        return simulacion(pos_x, pos_y+1, direction*-1)
    elif pos_y == 23:
        return simulacion(pos_x, pos_y-1, direction*-1)
    elif direction == 1:
        return simulacion(pos_x+1, pos_y+1, direction)
    elif direction == -1:
        return simulacion(pos_x+1, pos_y-1, direction)

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
    textRect.center = (game_field.width/2) + x_displace, (game_field.height/2) + y_displace
    game_field.gameDisplay.blit(textSurf, textRect)

# Funcion encargada del rebote de la bola en bordes o en paletas. Version single
# E: posicion de la bola en x, posicion de la bola en y, posicion de la paleta del jugador 1 en x y y, posicion de la paleta
# del jugador 2 en x y y.
# S: Nueva posicion de la bola en x y y
# R: -
def ball_bounce_singles(ball_x, ball_y, player1_1x, player1_1y, player2_1x, player2_1y):
    if (game_field.get_ball_direction()[
            0] > 0 and ball_x + 1 == player2_1x and (player2_1y <= ball_y <= player2_1y + game_field.paleta_length or (
            game_field.get_ball_direction()[1] > 0 and player2_1y <= ball_y+1 <= player2_1y + game_field.paleta_length) or (
            game_field.get_ball_direction()[1] < 0 and player2_1y <= ball_y-1 <= player2_1y + game_field.paleta_length))) or (
            game_field.get_ball_direction()[
                0] < 0 and ball_x - 1 == 0 and (player1_1y <= ball_y <= player1_1y + game_field.paleta_length or (
            game_field.get_ball_direction()[1] > 0 and player1_1y <= ball_y+1 <= player1_1y + game_field.paleta_length) or (
            game_field.get_ball_direction()[1] > 0 and player1_1y <= ball_y+1 <= player1_1y + game_field.paleta_length)
    )):

        game_field.set_ball_direction((game_field.get_ball_direction()[0] * -1, game_field.get_ball_direction()[1]))

        if game_field.get_ball_direction()[0] < 0:
            if player2_1y <= ball_y <= player2_1y + game_field.paleta_length / 3:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], -1))
                game_field.set_ball_velocity(30)
            elif player2_1y + game_field.paleta_length / 3 < ball_y < player2_1y + (2 * game_field.paleta_length) / 3:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], 0))
                game_field.set_ball_velocity(40)
            elif player2_1y + (2 * game_field.paleta_length / 3) <= ball_y <= player2_1y + (
                    3 * game_field.paleta_length) / 3:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], 1))
                game_field.set_ball_velocity(30)
            # Pong
            pong_sound.play()
        elif game_field.get_ball_direction()[0] > 0:
            if player1_1y <= ball_y < player1_1y + game_field.paleta_length / 3:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], -1))
                game_field.set_ball_velocity(30)
            elif player1_1y + game_field.paleta_length / 3 < ball_y < player1_1y + (2 * game_field.paleta_length) / 3:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], 0))
                game_field.set_ball_velocity(40)
            elif player1_1y + (2 * game_field.paleta_length / 3) < ball_y <= player1_1y + (
                    3 * game_field.paleta_length) / 3:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], 1))
                game_field.set_ball_velocity(30)
            # Ping
            ping_sound.play()
    elif game_field.get_ball_direction()[0] > 0 and ball_x + 1 == len(game_field.get_matrix()[0])+2:
        game_field.set_friend_score(game_field.get_friend_score() + 1)
        ball_x = 19
        ball_y = 12
    elif game_field.get_ball_direction()[0] < 0 and ball_x - 1 == -1:
        game_field.set_enemy_score(game_field.get_enemy_score() + 1)
        ball_x = 19
        ball_y = 12
    if (game_field.get_ball_direction()[1] > 0 and ball_y + 1 == len(game_field.get_matrix()) - 1) or (
            game_field.get_ball_direction()[1] < 0 and ball_y - 1 == 1):
        game_field.set_ball_direction((game_field.get_ball_direction()[0], game_field.get_ball_direction()[1] * -1))

    return ball_x, ball_y


# Funcion encargada del rebote de la bola en bordes o en paletas. Version doubles
# E: posicion de la bola en x, posicion de la bola en y, posicion de las paletas del jugador 1 en x y y,
# posicion de las paletas
# del jugador 2 en x y y.
# S: Nueva posicion de la bola en x y y.
# R: -
def ball_bounce_doubles(ball_x, ball_y, player1_1x, player1_2x, player1_1y, player1_2y, player2_1x, player2_2x, player2_1y, player2_2y):
    if (game_field.get_ball_direction()[0] > 0 and (
            (ball_x + 1 == player2_1x and (player2_1y <= ball_y <= player2_1y + game_field.paleta_length or (
            game_field.get_ball_direction()[1] > 0 and player2_1y <= ball_y+1 <= player2_1y) or (
            game_field.get_ball_direction()[1] < 0 and player2_1y <= ball_y - 1 <= player2_1y))) or (
            ball_x + 1 == player2_2x and (player2_2y <= ball_y <= player2_2y + game_field.paleta_length or (
            game_field.get_ball_direction()[1] > 0 and player2_2y <= ball_y+1 <= player2_2y) or (
            game_field.get_ball_direction()[1] < 0 and player2_2y <= ball_y - 1 <= player2_2y))))) or (
            game_field.get_ball_direction()[0] < 0 and (
            ball_x - 1 == player1_1x and (player1_1y <= ball_y <= player1_1y + game_field.paleta_length or (
            game_field.get_ball_direction()[1] > 0 and player1_1y <= ball_y+1 <= player1_1y) or (
            game_field.get_ball_direction()[1] > 0 and player1_1y <= ball_y+1 <= player1_2y)) or (
            ball_x - 1 == player1_2x and (player1_2y <= ball_y <= player1_2y + game_field.paleta_length or (
            game_field.get_ball_direction()[1] > 0 and player1_2y <= ball_y+1 <= player2_1y) or (
            game_field.get_ball_direction()[1] > 0 and player1_2y <= ball_y+1 <= player2_1y))))):
        game_field.set_ball_direction((game_field.get_ball_direction()[0] * -1, game_field.get_ball_direction()[1]))
        if game_field.get_ball_direction()[0] < 0 and ball_x > len(game_field.get_matrix()[0]) - 10:
            if player2_1y <= ball_y < player2_1y + (game_field.paleta_length / 3)-1:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], -1))
                game_field.set_ball_velocity(30)
            elif player2_1y + game_field.paleta_length / 3 <= ball_y <= player2_1y + (
                    (2 * game_field.paleta_length) / 3) - 1:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], 0))
                game_field.set_ball_velocity(40)
            elif player2_1y + (2 * game_field.paleta_length / 3) < ball_y <= player2_1y + ((
                    3 * game_field.paleta_length) / 3)-1:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], 1))
                game_field.set_ball_velocity(30)
            # Pong
            pong_sound.play()
        elif game_field.get_ball_direction()[0] < 0:
            if player2_2y <= ball_y < player2_2y + (game_field.paleta_length / 3)-1:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], -1))
                game_field.set_ball_velocity(30)
            elif player2_2y + game_field.paleta_length / 3 <= ball_y <= player2_2y + (
                    (2 * game_field.paleta_length) / 3) - 1:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], 0))
                game_field.set_ball_velocity(40)
            elif player2_2y + (2 * game_field.paleta_length / 3) < ball_y <= player2_2y + ((
                    3 * game_field.paleta_length) / 3)-1:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], 1))
                game_field.set_ball_velocity(30)
            # Ping
            ping_sound.play()
        elif game_field.get_ball_direction()[0] > 0 and ball_x < 11:
            if player1_1y <= ball_y <= player1_1y + (game_field.paleta_length / 3)-1:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], -1))
                game_field.set_ball_velocity(30)
            elif player1_1y + game_field.paleta_length / 3 <= ball_y <= (player1_1y + (2 * game_field.paleta_length) / 3)-1:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], 0))
                game_field.set_ball_velocity(40)
            elif (player1_1y + (2 * game_field.paleta_length / 3)) <= ball_y <= player1_1y + (
                    (3 * game_field.paleta_length) / 3)-1:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], 1))
                game_field.set_ball_velocity(30)
        elif game_field.get_ball_direction()[0] > 0:
            if player1_2y <= ball_y <= player1_2y + (game_field.paleta_length / 3)-1:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], -1))
                game_field.set_ball_velocity(30)
            elif player1_2y + game_field.paleta_length / 3 <= ball_y <= (player1_2y + (2 * game_field.paleta_length) / 3)-1:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], 0))
                game_field.set_ball_velocity(40)
            elif (player1_2y + (2 * game_field.paleta_length / 3)) <= ball_y <= player1_2y + (
                    (3 * game_field.paleta_length) / 3)-1:
                game_field.set_ball_direction((game_field.get_ball_direction()[0], 1))
                game_field.set_ball_velocity(30)

    elif game_field.get_ball_direction()[0] > 0 and ball_x + 1 == len(game_field.get_matrix()[0])+1:
        game_field.set_friend_score(game_field.get_friend_score() + 1)
        ball_x = 19
        ball_y = 12
    elif game_field.get_ball_direction()[0] < 0 and ball_x - 1 == -1:
        game_field.set_enemy_score(game_field.get_enemy_score() + 1)
        ball_x = 19
        ball_y = 12

    if (game_field.get_ball_direction()[1] > 0 and ball_y + 1 == len(game_field.get_matrix()) - 1) or (
            game_field.get_ball_direction()[1] < 0 and ball_y - 1 == 1):
        game_field.set_ball_direction((game_field.get_ball_direction()[0], game_field.get_ball_direction()[1] * -1))

    return ball_x, ball_y


gameloop(game_field.singles, game_field.doubles)

# Finalizacion del juego
pygame.quit()
quit()
