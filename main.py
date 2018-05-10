import pygame
from tkinter import *  #Importa todo de tkinter
from tkinter import font

pygame.init()


root = Tk() #Hacer la ventana

root.title() #título de la ventana
root.minsize(800,600) #Tamaño mínimo de la ventana
root.resizable(width = NO, height = NO) #Que el tamaño de la ventana no cambie

canvas = Canvas(root, width=800, height=600, bg="#000000") #Se crea el canvas y se configura
canvas.place(x=0, y=0)
canvas.create_rectangle(5,5,795,595, fill="#000000",  outline="#FFFFFF", width=9 )
canvas.create_rectangle(5,5,795,595, fill="#000000",  outline="white", width=1 )
canvas.create_rectangle(30,220,50,380,fill="white",outline="white", width=5)
canvas.create_rectangle(750,220,770,380,fill="white",outline="white", width=5)
canvas.create_rectangle(220,272,240,292,fill="white",outline="white", width=5)
canvas.create_rectangle(220,332,240,352,fill="white",outline="white", width=5)
canvas.create_rectangle(220,392,240,412,fill="white",outline="white", width=5)

pong = PhotoImage(file="PONG.png")
pongL = Label(canvas, image=pong)
pongL.pack()
pongL.place(x=170,y=50)

pygame.mixer.init()
pygame.mixer.music.load("Blip_Select.wav")

def play_sound():
    pygame.mixer.music.play()

def toplevelHelp():
    root.withdraw()
    toplevel_help= Toplevel()
    toplevel_help.title("Help")
    toplevel_help.minsize(800,600)
    toplevel_help.resizable(width=NO, height=NO)
    toplevel_help.configure(bg="Black")

    canvas2 = Canvas(toplevel_help, width=800, height=600, bg="#000000")  # Se crea el canvas y se configura
    canvas2.place(x=0, y=0)
    canvas2.create_rectangle(5, 5, 795, 595, fill="#000000", outline="#FFFFFF", width=9)
    canvas2.create_rectangle(5, 5, 795, 595, fill="#000000", outline="white", width=1)
    canvas2.create_rectangle(30, 220, 50, 380, fill="white", outline="white", width=5)
    canvas2.create_rectangle(750, 220, 770, 380, fill="white", outline="white", width=5)

    ws = PhotoImage(file="ws.png")
    wsL = Label(canvas2, image=ws)
    wsL.image = ws
    wsL.pack()
    wsL.place(x=50, y=50)

    ab = PhotoImage(file="ab.png")
    abL = Label(canvas2, image=ab)
    abL.image = ab
    abL.pack()
    abL.place(x=120, y=50)

    def mostrar(): #función que muestra el root y destruye el toplevel
        root.deiconify()
        toplevel_help.destroy()

    def unir2():
        play_sound()
        root.deiconify()
        toplevel_help.destroy()

    boton_v = Button(toplevel_help, command=unir2 , text="<volver>",bg="black", fg="white", bd=0, font="courier 18", activebackground="white",relief=FLAT)
    boton_v.pack() #botón para la función mostrar4
    boton_v.place(x=350,y=530)

    instrucciones = Label(canvas2, text="Descripción: \n PONG es un juego tanto para 1 como 2 jugadores, el juego consiste en evitar que la pelota pase \n su paleta y anotar pasando la bola detrás de la paleta del contrincante", font="courier 10",bg="black", fg="white")
    instrucciones.pack()
    instrucciones.place(x=0, y=0)

def unir1():
    play_sound()
    toplevelHelp()


pvp = Button(canvas, command= play_sound, text="Player vs Player",bg="black", fg="white", bd=0, font="courier 18", activebackground="white",relief=FLAT)
pvp.place(x=260, y=260)

pvpc = Button(canvas, command=play_sound, text="Player vs PC",bg="black", fg="white", bd=0, font="courier 18", activebackground="white",relief=FLAT)
pvpc.place(x=260, y=320)

help1 = Button(canvas,command=unir1, text="Help",bg="black", fg="white", bd=0, font="courier 18", activebackground="white",relief=FLAT)
help1.place(x=260, y=380)

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

root.mainloop()