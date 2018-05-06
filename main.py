import pygame

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

block_height = 20
block_width = 24

clock = pygame.time.Clock()

class Tablero:
    def __init__(self, E_SCORE, F_SCORE, LEVEL, B_X, B_Y, B_DIRECTION, B_VELOCITY, PC, block_width, block_height):
        # Atributos
        self.width = 800
        self.height = 600
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.game_matrix = [[]]
        self.matrix_constructor()
        self.enemy_score = E_SCORE
        self.friend_score = F_SCORE
        self.scores()
        self.block_width = block_width
        self.block_height = block_height
        self.friend_score = F_SCORE
        self.enemy_score = E_SCORE
        self.level = LEVEL
        self.ball_velocity = B_VELOCITY # Cambiar
        self.ball_x = B_X
        self.ball_y = B_Y
        self.FPS = 30*self.level
        self.ball_direction = B_DIRECTION
        self.pc = PC
        self.paleta_length = 9 - 3*(self.level-1) # Cambiar

    # Metodos
    def matrix_constructor(self):
        for n in range(25):
            self.game_matrix.append([])
            for m in range(40):
                self.game_matrix[n].append(False)
        self.game_matrix = self.game_matrix[:len(self.game_matrix)-1]

    def get_matrix(self):
        return self.game_matrix

    def set_matrix(self, new_matrix):
        if not (isinstance(new_matrix, list) and isinstance(new_matrix[0], list) and len(new_matrix) == 25 and len(new_matrix[0]) == 40):
            return 'Error'
        self.game_matrix = new_matrix

    def screen(self):
        for n in range(len(self.game_matrix)):
            for m in range(len(self.game_matrix[n])):
                if self.game_matrix[n][m]:
                    pygame.draw.rect(self.gameDisplay,white,[m*self.block_width, n*self.block_height,
                                                             self.block_width, self.block_height])
                else:
                    pygame.draw.rect(self.gameDisplay, black, [m * self.block_width, n * self.block_height,
                                                               self.block_width, self.block_height])


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

    def scores(self):
        self.score_e()
        self.score_f()

    def clean_matrix(self):
        for n in range(len(self.game_matrix)):
            for m in range(len(self.game_matrix[0])):
                self.game_matrix[n][m] = False
        self.scores()


    def lose(self):
        pass

    def win(self):
        pass

    def pause(self):
        pass


class Singles(Tablero):
    def __init__(self, E_SCORE, F_SCORE, LEVEL, B_X, B_Y, B_DIRECTION, B_VELOCITY, PC, P1_Y, P2_Y, block_height, block_width):
        Tablero.__init__(self, E_SCORE, F_SCORE, LEVEL, B_X, B_Y, B_DIRECTION, B_VELOCITY, PC, block_height, block_width)
        self.player1_x = 0
        self.player1_y = P1_Y
        self.player2_x = len(self.game_matrix[0])-1
        self.player2_y = P2_Y



game_field = Singles(0, 0, 1, 19, 12, 1, 1, False, 1, 1, block_height, block_width)


class Bola:
    def __init__(self, pos_x, pos_y, block_width, block_height):
        self.width = block_width
        self.height = block_height
        self.x = pos_x
        self.y = pos_y
        self.mod_matrix()


    def mod_matrix(self):
        matrix = game_field.get_matrix()
        for n in range(len(matrix)):
            for m in range(len(matrix[0])):
                if m == self.x and n == self.y:
                    matrix[n][m] = True
        game_field.set_matrix(matrix)


class Paleta:
    def __init__(self, pos_x, pos_y, block_width, block_height):
        self.width = block_width
        self.height = block_height
        self.x = pos_x
        self.y = pos_y
        self.mod_matrix()


    def mod_matrix(self):
        matrix = game_field.get_matrix()
        for n in range(len(matrix)):
            for m in range(len(matrix[0])):
                if m == self.x and n == self.y:
                    for i in range(game_field.paleta_length):
                        matrix[n+i][m] = True
        game_field.set_matrix(matrix)



def gameloop():
    game = True
    player1_x = 0
    player1_y = 1
    player2_x = len(game_field.game_matrix[0])-1
    player2_y = 1
    player1_down_y = False
    player1_up_y = False
    player2_up_y = False
    player2_down_y = False

    ball_x = 19
    ball_y = 12

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player1_up_y = True
                elif event.key == pygame.K_DOWN:
                    player1_down_y = True
                elif event.key == pygame.K_w:
                    player2_up_y = True
                elif event.key == pygame.K_s:
                    player2_down_y = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player1_up_y = False
                elif event.key == pygame.K_DOWN:
                    player1_down_y = False
                elif event.key == pygame.K_w:
                    player2_up_y = False
                elif event.key == pygame.K_s:
                    player2_down_y = False

        if player1_down_y and player1_y + game_field.paleta_length + 1 < len(game_field.game_matrix):
            player1_y += 1
        elif player1_up_y and player1_y+1 > 2:
            player1_y -= 1

        if player2_down_y and player2_y + game_field.paleta_length + 1 < len(game_field.game_matrix):
            player2_y += 1
        elif player2_up_y and player2_y+1 > 2:
            player2_y -= 1

        if (game_field.ball_velocity > 0 and ball_x + 1 == len(
                game_field.game_matrix[0])-1 and player2_y <= ball_y <= player2_y+game_field.paleta_length) or (
                game_field.ball_velocity < 0 and ball_x - 1 == 0 and player1_y <= ball_y <= player1_y + game_field.paleta_length):
            game_field.ball_velocity *= -1
            if game_field.ball_velocity < 0:
                if player2_y <= ball_y <= player2_y+game_field.paleta_length/3:
                    game_field.ball_direction = -1
                    game_field.FPS = 30
                elif player2_y+game_field.paleta_length/3 <= ball_y <= player2_y+ (2*game_field.paleta_length)/3:
                    game_field.ball_direction = 0
                    game_field.FPS = 40
                elif player2_y+(2*game_field.paleta_length/3) <= ball_y <= player2_y+ (3*game_field.paleta_length)/3:
                    game_field.ball_direction = 1
                    game_field.FPS = 30
            elif game_field.ball_velocity > 0:
                if player1_y <= ball_y <= player1_y+game_field.paleta_length/3:
                    game_field.ball_direction = -1
                    game_field.FPS = 30
                elif player1_y+game_field.paleta_length/3 <= ball_y <= player1_y+ (2*game_field.paleta_length)/3:
                    game_field.ball_direction = 0
                    game_field.FPS = 40
                elif player1_y+(2*game_field.paleta_length/3) <= ball_y <= player1_y+ (3*game_field.paleta_length)/3:
                    game_field.ball_direction = 1
                    game_field.FPS = 30
        elif game_field.ball_velocity > 0 and ball_x + 1 == len(game_field.game_matrix[0]):
            game_field.enemy_score += 1
            ball_x = 19
            ball_y = 12
        elif game_field.ball_velocity < 0 and ball_x - 1 == 0:
            game_field.friend_score += 1
            ball_x = 19
            ball_y = 12
        if (game_field.ball_direction > 0 and ball_y + 1 == len(game_field.game_matrix)-1) or (game_field.ball_direction < 0 and ball_y - 1 == 1):
            game_field.ball_direction *= -1

        game_field.clean_matrix()
        ball_x += 1 * game_field.ball_velocity
        ball_y += 1 * game_field.ball_direction
        bola = Bola(ball_x, ball_y, block_width, block_height)
        player1 = Paleta(player1_x, player1_y, block_width, block_height)
        player2 = Paleta(player2_x, player2_y, block_width, block_height)
        game_field.screen()
        pygame.display.update()

        clock.tick(game_field.FPS)


gameloop()
