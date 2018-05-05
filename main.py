import pygame

pygame.init()

white = (255,255,255)

class Tablero:
    def __init__(self, E_SCORE, F_SCORE, LEVEL, B_X, B_Y, PC):
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
        self.pc = PC
        self.paleta_length = self.level*9 # Cambiar
        self.screen()


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
                    pygame.draw.rect(self.gameDisplay,white,[m*20, n*24, self.block_width, self.block_height])

        pygame.display.update()

    def score(self):
        if self.friend_score == 0:
            pass
        elif self.friend_score == 1:
            pass
        elif self.friend_score == 0:
            pass
        elif self.friend_score == 1:
            pass
        elif self.friend_score == 0:
            pass
        elif self.friend_score == 1:
            pass
        elif self.friend_score == 0:
            pass
        elif self.friend_score == 1:
            pass
        elif self.friend_score == 0:
            pass
        elif self.friend_score == 1:
            pass

        if self.enemy_score == 0:
            pass
        elif self.enemy_score == 1:
            pass
        elif self.enemy_score == 0:
            pass
        elif self.enemy_score == 1:
            pass
        elif self.enemy_score == 0:
            pass
        elif self.enemy_score == 1:
            pass
        elif self.enemy_score == 0:
            pass
        elif self.enemy_score == 1:
            pass
        elif self.enemy_score == 0:
            pass
        elif self.enemy_score == 1:
            pass


a = Tablero(0,0,1,0,0,False)

while True:
    pass