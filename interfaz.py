import pygame
import mutagen.oggvorbis
import os
from tkinter import *  #Importa todo de tkinter}

MUTE= ''
#inicia pygame
pygame.init()

#Sonidos
select_sound = pygame.mixer.Sound('sounds/select.ogg')
pong_sound = pygame.mixer.Sound('sounds/pong.ogg')
ping_sound = pygame.mixer.Sound('sounds/ping.ogg')
point_sound = pygame.mixer.Sound('sounds/point.ogg')
fail_sound = pygame.mixer.Sound('sounds/fail.ogg')

#Función que crea el root con todas sus modificaciones
def root():
    pygame.init()
    root = Tk() #Hacer la ventana

    # musica de lobby
    sample_rate = mutagen.oggvorbis.OggVorbis("sounds/start_menu.ogg").info.sample_rate
    pygame.mixer.quit()
    pygame.mixer.pre_init(sample_rate, -16, 1, 512)
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/start_menu.ogg")
    pygame.mixer.music.play(-1)


    root.title() #título de la ventana

    # configuracion de la pantalla
    width = 800
    height = 600

    ws = root.winfo_screenwidth()  # largo de la pantalla
    hs = root.winfo_screenheight() # Anchura de la pantalla

    x = (ws / 2) - (width / 2)
    y = (hs / 2) - (height / 2)

    root.resizable(width = NO, height = NO) #Que el tamaño de la ventana no cambie
    root.geometry("%dx%d+%d+%d" %(width, height, x, y))

    # Se crea el canvas y se configura
    canvas = Canvas(root, width=800, height=600, bg="#000000")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(5,5,795,595, fill="#000000",  outline="#FFFFFF", width=9 )
    canvas.create_rectangle(5,5,795,595, fill="#000000",  outline="white", width=1 )
    canvas.create_rectangle(30,220,50,380,fill="white",outline="white", width=5)
    canvas.create_rectangle(750,200,770,360,fill="white",outline="white", width=5)
    canvas.create_rectangle(220,252,240,272,fill="white",outline="white", width=5)
    canvas.create_rectangle(220,312,240,332,fill="white",outline="white", width=5)
    canvas.create_rectangle(220,372,240,392,fill="white",outline="white", width=5)
    canvas.create_rectangle(220,432,240,452,fill="white",outline="white", width=5)


    #Label con la imagen del título de pong
    pong = PhotoImage(file="Images/PONG.png")
    pongL = Label(canvas, image=pong)
    pongL.pack()
    pongL.place(x=170,y=50)


    #inicializa el mixer de pygame
    pygame.mixer.init()

    #Función que crea y modifica el toplevel_help
    def toplevelHelp():
        root.withdraw()
        toplevel_help= Toplevel()
        toplevel_help.title("Help")
        ws = toplevel_help.winfo_screenwidth()  # largo de la pantalla
        hs = toplevel_help.winfo_screenheight()  # Anchura de la pantalla

        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)

        toplevel_help.resizable(width=NO, height=NO)  # Que el tamaño de la ventana no cambie
        toplevel_help.geometry("%dx%d+%d+%d" % (width, height, x, y))
        toplevel_help.configure(bg="Black")

        canvas2 = Canvas(toplevel_help, width=800, height=600, bg="#000000")  # Se crea el canvas2 y se configura
        canvas2.place(x=0, y=0)
        canvas2.create_rectangle(5, 5, 795, 595, fill="#000000", outline="#FFFFFF", width=9)
        canvas2.create_rectangle(5, 5, 795, 595, fill="#000000", outline="white", width=1)
        canvas2.create_rectangle(30, 220, 50, 380, fill="white", outline="white", width=5)
        canvas2.create_rectangle(750, 220, 770, 380, fill="white", outline="white", width=5)

        # Label con la imagen de los controles del player2
        ws = PhotoImage(file="Images/ws.png")
        wsL = Label(canvas2, image=ws)
        wsL.image = ws
        wsL.pack()
        wsL.place(x=500, y=370)

        #Label con la imagen de los controles del player1
        ab = PhotoImage(file="Images/ab.png")
        abL = Label(canvas2, image=ab)
        abL.image = ab
        abL.pack()
        abL.place(x=220, y=370)

        # función que muestra el root y destruye el toplevel
        def unir1():
            root.deiconify()
            toplevel_help.destroy()
            select_sound.play()

        #Botón para volver a el root mediante la función unir1
        boton_v = Button(toplevel_help, command=unir1 , text="<volver>",bg="black", fg="white", bd=0, font="courier 18", activebackground="white",relief=FLAT)
        boton_v.pack() #botón para la función mostrar4
        boton_v.place(x=325,y=530)

        #Label con la descripción del juego
        descripcion = Label(canvas2, text="Descripción: \n PONG es un juego tanto para 1 como 2 jugadores, el juego consiste en evitar que la pelota \n pase  su paleta y anotar pasando la bola detrás de la paleta del  contrincante. El juego \n tiene la modalidad de 1 jugador contra la máquina y 2 jugadores que se enfrentan entre sí", font="courier 10",bg="black", fg="white")
        descripcion.pack()
        descripcion.place(x=36, y=30)

        #Label que explica las dificultades
        dificultad = Label(canvas2, text="Dificultades: \n El juego consta de un sistema de dificultad el cual es diferente \n en el modo PvC (player vs computer) a el modo PvP (player vs player). \n En el modo PvC hay 3 rondas  de 10 puntos cada una con una dificultad \n mayor y en el modo PvP la dificultad aumenta mientras la \n pelota siga en juego, hasta que uno de los jugadores anote un punto", font="courier 10",bg="black", fg="white")
        dificultad.pack()
        dificultad.place(x=110, y=115)

        #Label con las instrucciones de singles y doubles
        s_d = Label(canvas2,text="Singles y Doubles: \n Además el juego consta de una opción para diversificar la jugabilidad, elija \n singles para jugar con una paleta y doubles para jugar con dos paletas",font="courier 10", bg="black", fg="white")
        s_d.pack()
        s_d.place(x=80, y=240)

        #Label que indica los controles
        controles = Label(canvas2, text="Controles:", font="courier 10",bg="black", fg="white")
        controles.pack()
        controles.place(x=350, y=320)

        #Label de interfaz que indica cuáles son los controles del player1
        player1 = Label(canvas2, text="Player1", font="courier 10",bg="black", fg="white")
        player1.pack()
        player1.place(x=220, y=480)

        #Label de interfaz que indica cuáles son los controles del player2
        player2 = Label(canvas2, text="Player2", font="courier 10",bg="black", fg="white")
        player2.pack()
        player2.place(x=500, y=480)

    #función para cambiar el valor de ver a 'singles'
    def modeS():
        global ver
        ver = 'singles'

    #valor default de ver a 'singles'
    modeS()

    #función para cambiar el valor de ver a 'doubles'
    def modeD():
        global ver
        ver = 'doubles'

    #Radiobutton que indica que se va a jugar en singles
    singlesL = Label(canvas, text="singles", bg="black", fg="white", font="courier 18")
    singlesL.pack()
    singlesL.place(x=250, y=500)
    singles = Radiobutton(canvas,command=modeS, bg="black", value=1, variable=1)
    singles.pack()
    singles.place(x=290, y=540)

    #Radiobutton que indica que se va a jugar en doubles
    doublesL= Label(canvas, text="doubles",bg="black", fg="white", font="courier 18")
    doublesL.pack()
    doublesL.place(x=440,y=500)
    doubles = Radiobutton(canvas, command=modeD,bg="black", value=2,variable=1)
    doubles.pack()
    doubles.place(x=480,y=540)


    # función  que abre el toplevelHelp y oculta el root, además de ejecutar el sonido de select
    def unir2():
        select_sound.play()
        toplevelHelp()

    # función usada para unir otras funciones: ejecutar el sonido select, destruir el root y ejecutar la clase Game en modo pvpc
    def unir3():
        global ver
        global MUTE
        MODE = ver
        pygame.mixer.music.stop()
        root.withdraw()
        os.system('python3 main.py %s %r %r %r' %(MODE, True, MUTE, ''))
        pygame.mixer.music.play(-1)
        muteI()
        root.deiconify()


    # función usada para unir otras funciones: ejecutar el sonido select, destruir el root y ejecutar la clase Game en modo pvp
    def unir4():
        global ver
        global MUTE
        global PT
        MODE = ver
        pygame.mixer.music.stop()
        root.withdraw()
        os.system('python3 main.py %s %r %r %r' %(MODE, '', MUTE, ''))
        pygame.mixer.music.play(-1)
        muteI()

        root.deiconify()

    def unir5():
        global ver
        global MUTE
        global PT
        MODE = ver
        pygame.mixer.music.stop()
        root.withdraw()
        os.system('python3 main.py %s %r %r %r' %(MODE, '', MUTE, True))
        pygame.mixer.music.play(-1)
        muteI()

        root.deiconify()


    # botón que ejecuta el juego en modo pvp mediante unir4
    pvp = Button(canvas, command= unir4, text="Player vs Player",bg="black", fg="white", bd=0, font="courier 18", activebackground="white",relief=FLAT)
    pvp.place(x=260, y=240)

    # botón que ejeucta el juego en modo pvpc mediante unir3
    pvpc = Button(canvas, command=unir3, text="Player vs PC",bg="black", fg="white", bd=0, font="courier 18", activebackground="white",relief=FLAT)
    pvpc.place(x=260, y=300)

    # botón que ejecuta la ventana de toplevelHelp mediante unir2
    help1 = Button(canvas,command=unir2, text="Help",bg="black", fg="white", bd=0, font="courier 18", activebackground="white",relief=FLAT) #botón que ejecuta la ventana de toplevelHelp mediante unir2
    help1.place(x=260, y=360)

    # botón que ejeucta el juego en práctica
    pract = Button(canvas, command=unir5, text="Práctica", bg="black", fg="white", bd=0, font="courier 18",activebackground="white", relief=FLAT)
    pract.place(x=260, y=420)

    def muteF():
        global MUTE
        if MUTE== '':
            MUTE = True
            pygame.mixer.music.pause()
        else:
            MUTE = ''
            pygame.mixer.music.unpause()

    def muteI():
        global MUTE

        if MUTE== '':
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()


    #boton que mutea el sonido
    muteP = PhotoImage(file="Images/mute.png")
    muteR = muteP.subsample(x=11,y=11)

    muteB = Button(canvas,command=muteF, bg="black",image=muteR ,fg="white", bd=0, activebackground="black",relief=FLAT)
    muteB.place(x=738, y=12)

    muteI()

    # mainloop del root
    root.mainloop()

root()#botón que ejecuta la ventan#botón que ejecuta la ventana de toplevelHelp mediante unir2a de toplevelHelp mediante unir2
