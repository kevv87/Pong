import pygame
from tkinter import *  #Importa todo de tkinter



pygame.init()





white = (255,255,255)

class Tablero:
    def __init__(self, E_SCORE, F_SCORE, LEVEL, B_X, B_Y, B_DIRECTION, PC):
        # Atributos
        self.width = 800
        self.height = 600
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.game_matrix = [[]]
        self.matrix_constructor()
        self.block_width = 20
        self.block_height = 24
        self.FPS = 30
        self.friend_score = F_SCORE
        self.enemy_score = E_SCORE
        self.level = LEVEL
        self.ball_velocity = self.level*1 # Cambiar
        self.ball_x = B_X
        self.ball_y = B_Y
        self.ball_direction = B_DIRECTION
        self.pc = PC
        self.paleta_length = 9 - 3*(self.level-1) # Cambiar

        # Ejecutando metodos
        self.score_f()
        self.score_e()
        self.screen()

    # Metodos
    def matrix_constructor(self):
        for n in range(25):
            self.game_matrix.append([])
            for m in range(40):
                if n == 24 or n == 0:
                    self.game_matrix[n].append(True)
                elif n%2 == 0 and m == 19:
                    self.game_matrix[n].append(True)
                else:
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

        pygame.display.update()

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
                    if ((n == 2 or n == 4 or n == 6) and 23 <= m <= 25) or (m == 23 and n == 5)or (m == 25 and n == 5) or (m == 23 and n == 3):
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
        elif self.enemy_score == 1:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 23 and 2 <= n <= 6):
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 2:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 23 <= m <= 25) or (m == 25 and n == 3) or (m == 23 and n == 5) :
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 3:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 23 <= m <= 25) or (m == 25 and n == 5) or (m == 25 and n == 3):
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 4:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 25 and 2 <= n <= 6) or (m == 23 and 2 <= n <= 4) or (m == 24 and n == 4):
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 5:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 23 <= m <= 25) or (m == 25 and n == 5) or (m == 23 and n == 3):
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 6:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 23 <= m <= 25) or (m == 23 and n == 5)or (m == 25 and n == 5) or (m == 23 and n == 3):
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 7:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 25 and 2 <= n <= 6) or ((m == 24 or m == 23) and n == 2):
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 8:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if ((n == 2 or n == 4 or n == 6) and 23 <= m <= 25) or ((m == 25 or m == 23) and (n == 3 or n == 5)):
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 9:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 25 and 2 <= n <= 6) or (m == 23 and 2 <= n <= 4) or (m == 24 and n == 4) or (m == 24 and n == 2):
                        self.game_matrix[n][m] = True
        elif self.enemy_score == 10:
            for n in range(len(self.game_matrix)):
                for m in range(len(self.game_matrix[0])):
                    if (m == 23 and 2 <= n <= 6) or (m == 25 and 2 <= n <= 6) or (n == 2 and 25 <= m <= 27) or (m == 27 and 2 <= n <= 6) or (n == 6 and 25 <= m <= 27):
                        self.game_matrix[n][m] = True

    def move_ball(self):
        if self.ball_direction == 'up':
            self.ball_y -= 1
        else:
            self.ball_y += 1

        if self.ball_velocity > 0:
            self.ball_x += 1
        elif self.ball_velocity < 0:
            self.ball_x -= 1

        ball = Ball(self.ball_x, self.ball_y)

    def lose(self):
        pass

    def win(self):
        pass

    def pause(self):
        pass

