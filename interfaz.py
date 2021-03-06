import pygame
import mutagen.oggvorbis
import os
from tkinter import *  #Importa todo de tkinter}
import random
import serial
import time

MUTE= ''
#inicia pygame
pygame.init()

selected = 0


#Sonidos
select_sound = pygame.mixer.Sound('sounds/select.ogg')
pong_sound = pygame.mixer.Sound('sounds/pong.ogg')
ping_sound = pygame.mixer.Sound('sounds/ping.ogg')
point_sound = pygame.mixer.Sound('sounds/point.ogg')
fail_sound = pygame.mixer.Sound('sounds/fail.ogg')


green = '#000fff000'
current_color = 'white'

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


    canvas.create_rectangle(5,5,795,595, fill="#000000",  outline=current_color, width=9 )
    canvas.create_rectangle(5,5,795,595, fill="#000000",  outline=current_color, width=1 )
    canvas.create_rectangle(30,220,50,380,fill=current_color,outline=current_color, width=5)
    canvas.create_rectangle(750,220,770,380,fill=current_color,outline=current_color, width=5)



    #Label con la imagen del título de pong
    pong_white = PhotoImage(file="Images/PONG.png")
    pong_green = PhotoImage(file="Images/PONG_GREEN.png")
    pong = pong_white

    pongL = Label(canvas, image=pong, highlightbackground=current_color)

    pongL.pack()
    pongL.place(x=170,y=50)


    #inicializa el mixer de pygame
    pygame.mixer.init()

    #Función que crea y modifica el toplevel_help
    def toplevelHelp():
        global toplevel_help, unir1
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



        #Label con la imagen de los controles
        controler = PhotoImage(file="Images/controller.png")
        controlerR = controler.subsample(x=2,y=2)
        controlerL = Label(canvas2,image=controlerR)
        controlerL.image = controlerR
        controlerL.pack()
        controlerL.place(x=210,y=300)

        # función que muestra el root y destruye el toplevel
        def unir1():
            root.deiconify()
            toplevel_help.destroy()
            select_sound.play()

        #Botón para volver a el root mediante la función unir1

        boton_v = Button(toplevel_help, command=unir1 , text="<volver>",bg="black", fg=current_color, bd=0, font="courier 18", activebackground=current_color,relief=FLAT,state=ACTIVE)

        boton_v.pack() #botón para la función mostrar4
        boton_v.place(x=640,y=540)

        #Label con la descripción del juego
        descripcion = Label(canvas2, text="Descripción: \n PONG es un juego tanto para 1 como 2 jugadores, el juego consiste en evitar que la pelota \n pase  su paleta y anotar pasando la bola detrás de la paleta del  contrincante. El juego \n tiene la modalidad de 1 jugador contra la máquina y 2 jugadores que se enfrentan entre sí", font="courier 10",bg="black", fg="white")
        descripcion.pack()
        descripcion.place(x=36, y=20)

        #Label que explica las dificultades
        dificultad = Label(canvas2, text="Dificultades: \n El juego consta de un sistema de dificultad el cual es diferente \n en el modo PvC (player vs computer) a el modo PvP (player vs player). \n En el modo PvC hay 3 rondas  de 10 puntos cada una con una dificultad \n mayor y en el modo PvP la dificultad aumenta mientras la \n pelota siga en juego, hasta que uno de los jugadores anote un punto", font="courier 10",bg="black", fg="white")
        dificultad.pack()
        dificultad.place(x=110, y=105)

        #Label con las instrucciones de singles y doubles
        s_d = Label(canvas2,text="Singles y Doubles: \n Además el juego consta de una opción para diversificar la jugabilidad, elija \n singles para jugar con una paleta y doubles para jugar con dos paletas",font="courier 10", bg="black", fg="white")
        s_d.pack()
        s_d.place(x=80, y=220)

    def toplevelHS():
        global unir1, boton_v
        root.withdraw()
        toplevel_hs = Toplevel()
        toplevel_hs.title("Highscores")

        ws = toplevel_hs.winfo_screenwidth()  # largo de la pantalla
        hs = toplevel_hs.winfo_screenheight()  # Anchura de la pantalla

        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)

        toplevel_hs.resizable(width=NO, height=NO)  # Que el tamaño de la ventana no cambie
        toplevel_hs.geometry("%dx%d+%d+%d" % (width, height, x, y))
        toplevel_hs.configure(bg="Black")

        canvas2 = Canvas(toplevel_hs, width=800, height=600, bg="#000000")  # Se crea el canvas2 y se configura
        canvas2.place(x=0, y=0)
        canvas2.create_rectangle(5, 5, 795, 595, fill="#000000", outline="#FFFFFF", width=9)
        canvas2.create_rectangle(5, 5, 795, 595, fill="#000000", outline="white", width=1)
        canvas2.create_rectangle(30, 220, 50, 380, fill="white", outline="white", width=5)
        canvas2.create_rectangle(750, 220, 770, 380, fill="white", outline="white", width=5)

        t = open("highscores.txt","r")
        var1 = t.readlines(1)
        var2 = t.readlines(2)
        var3 = t.readlines(3)
        t.close()

        pp = str(var1).replace("\\n","").replace("{","").replace("'","").replace("[","").replace("]","").replace("%","   ")
        ss = str(var2).replace("\\n","").replace("{","").replace("'","").replace("[","").replace("]","").replace("%","   ")
        tt = str(var3).replace("\\n","").replace("{","").replace("'","").replace("[","").replace("]","").replace("%","   ")

        nombres = Label(canvas2, text="Names", bg="black", fg="white", font="courier 30")
        nombres.pack()
        nombres.place(x=220,y=50)

        scores = Label(canvas2, text="Scores", bg="black", fg="white", font="courier 30")
        scores.pack()
        scores.place(x=400,y=50)

        hs1 = Label(canvas2, text=pp, bg="black", fg="white", font="courier 30")
        hs1.pack()
        hs1.place(x=240,y=130)

        hs2 = Label(canvas2, text=ss, bg="black", fg="white", font="courier 30")
        hs2.pack()
        hs2.place(x=240, y=255)

        hs3 = Label(canvas2, text=tt, bg="black", fg="white", font="courier 30")
        hs3.pack()
        hs3.place(x=240, y=380)

        # función que muestra el root y destruye el toplevel
        def unir1():
            root.deiconify()
            toplevel_hs.destroy()
            select_sound.play()

        #Botón para volver a el root mediante la función unir1
        boton_v = Button(toplevel_hs, command=unir1 , text="<volver>",bg="black", fg="white", bd=0, font="courier 18", activebackground="white",relief=FLAT)
        boton_v.pack() #botón para la función mostrar4
        boton_v.place(x=325,y=530)



    def pra_dif_ele():
        global unir1, unir2, unir3, unir4, boton_v, boton_e, boton_m, boton_h
        root.withdraw()
        toplevel_de = Toplevel()
        toplevel_de.title("Dificultad de práctica")

        ws = toplevel_de.winfo_screenwidth()  # largo de la pantalla
        hs = toplevel_de.winfo_screenheight()  # Anchura de la pantalla

        x = (ws / 2) - (450 / 2)
        y = (hs / 2) - (600 / 2)

        toplevel_de.resizable(width=NO, height=NO)  # Que el tamaño de la ventana no cambie
        toplevel_de.geometry("%dx%d+%d+%d" % (450, 600, x, y))
        toplevel_de.configure(bg="Black")

        canvas3 = Canvas(toplevel_de, width=800, height=600, bg="#000000")  # Se crea el canvas2 y se configura
        canvas3.place(x=0, y=0)
        canvas3.create_rectangle(5, 5, 445, 595, fill="#000000", outline="#FFFFFF", width=9)
        canvas3.create_rectangle(5, 5, 445, 595, fill="#000000", outline="white", width=1)
        canvas3.create_rectangle(30, 220, 50, 380, fill="white", outline="white", width=5)
        canvas3.create_rectangle(400, 220, 420, 380, fill="white", outline="white", width=5)

        # función que muestra el root y destruye el toplevel
        def unir1():
            root.deiconify()
            toplevel_de.destroy()
            select_sound.play()

        def unir2():
            global ver
            global MUTE
            global PT
            global tramp
            MODE = ver
            OBS = tramp
            pygame.mixer.music.stop()
            root.withdraw()
            toplevel_de.destroy()
            if current_color != '#000fff000':
                os.system('python3 main.py %s %r %r %r %s %r %s' % (MODE, '', MUTE, True, 'white', OBS, '1'))
            else:
                os.system('python3 main.py %s %r %r %r %s %r %s' % (MODE, '', MUTE, True, 'green', OBS, '1'))
            pygame.mixer.music.play(-1)
            muteI()
            root.deiconify()

        def unir3():
            global ver
            global MUTE
            global PT
            global tramp
            MODE = ver
            OBS = tramp
            pygame.mixer.music.stop()
            root.withdraw()
            toplevel_de.destroy()
            if current_color != '#000fff000':
                os.system('python3 main.py %s %r %r %r %s %r %s' % (MODE, '', MUTE, True, 'white', OBS, '2'))
            else:
                os.system('python3 main.py %s %r %r %r %s %r %s' % (MODE, '', MUTE, True, 'green', OBS, '2'))
            pygame.mixer.music.play(-1)
            muteI()
            root.deiconify()


        def unir4():
            global ver
            global MUTE
            global PT
            global tramp
            MODE = ver
            OBS = tramp
            pygame.mixer.music.stop()
            root.withdraw()
            toplevel_de.destroy()
            if current_color != '#000fff000':
                os.system('python3 main.py %s %r %r %r %s %r %s' % (MODE, '', MUTE, True, 'white', OBS, '3'))
            else:
                os.system('python3 main.py %s %r %r %r %s %r %s' % (MODE, '', MUTE, True, 'green', OBS, '3'))
            pygame.mixer.music.play(-1)
            muteI()
            root.deiconify()


        boton_e = Button(toplevel_de, command=unir2, text="    Easy    ", bg="black", fg="white", bd=0, font="courier 18", activebackground="white", relief=FLAT)
        boton_e.pack()  # botón para la función mostrar4
        boton_e.place(x=130, y=100)

        boton_m = Button(toplevel_de, command=unir3, text="   Medium   ", bg="black", fg="white", bd=0, font="courier 18", activebackground="white", relief=FLAT)
        boton_m.pack()  # botón para la función mostrar4
        boton_m.place(x=130, y=250)

        boton_h = Button(toplevel_de, command=unir4, text="    Hard    ", bg="black", fg="white", bd=0, font="courier 18",activebackground="white", relief=FLAT)
        boton_h.pack()  # botón para la función mostrar4
        boton_h.place(x=130, y=400)


        # Botón para volver a el root mediante la función unir1
        boton_v = Button(toplevel_de, command=unir1, text="<volver>", bg="black", fg="white", bd=0, font="courier 18", activebackground="white", relief=FLAT)
        boton_v.pack()  # botón para la función mostrar4
        boton_v.place(x=150, y=530)


    def lan_win():
        global isserver
        global isclient
        global lan
        global back, selected
        root.withdraw()
        lan = Toplevel()
        # configuracion de la pantalla
        width = 800
        height = 600
        ws = lan.winfo_screenwidth()  # largo de la pantalla
        hs = lan.winfo_screenheight()  # Anchura de la pantalla

        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)

        lan.resizable(width=NO, height=NO)  # Que el tamaño de la ventana no cambie
        lan.geometry("%dx%d+%d+%d" % (width, height, x, y))

        canvas = Canvas(lan, width=800, height=600, bg="#000000")
        canvas.place(x=0, y=0)

        canvas.create_rectangle(5, 5, 795, 595, fill="#000000", outline="#FFFFFF", width=9)

        canvas.create_rectangle(5, 5, 795, 595, fill="#000000", outline="white", width=1)
        canvas.create_line(300, 0, 300, 600, fill='white')
        canvas.create_line(300, 300, 800, 300, fill='white')

        isserver = True
        isclient = False

        def beserver():
            global isserver
            global isclient
            isserver = True
            isclient = False

        def beclient():
            global isclient
            global isserver
            isclient = True
            isserver = False

        # Radiobutton que indica que se va a ser el server
        serverL = Label(canvas, text="Servidor", bg="black", fg="white", font="courier 30")
        serverL.pack()
        serverL.place(x=20, y=90)
        server = Radiobutton(canvas, bg="black", value=1, variable=1, command=beserver)
        server.pack()
        server.place(x=100, y=150)

        # Radiobutton que indica que se va a ser un cliente
        clientL = Label(canvas, text="Cliente", bg="black", fg="white", font="courier 30")
        clientL.pack()
        clientL.place(x=20, y=390)
        client = Radiobutton(canvas, bg="black", value=2, variable=1, command=beclient)
        client.pack()
        client.place(x=100, y=450)

        serverT = Label(canvas, text="Servidor", bg="black", fg="white", font="courier 30")
        serverT.pack()
        serverT.place(x=445, y=20)

        clientT = Label(canvas, text="Cliente", bg="black", fg="white", font="courier 30")
        clientT.pack()
        clientT.place(x=450, y=320)

        client1_ip_L = Label(canvas, text='Ip de cliente 1:', fg='white', bg='black', font='courier')
        client2_ip_L = Label(canvas, text='Ip de cliente 2:', fg='white', bg='black', font='courier')
        client1_ip_L.pack()
        client2_ip_L.pack()
        client1_ip_L.place(x=320, y=100)
        client2_ip_L.place(x=320, y=175)

        client1_ip = Entry(canvas)
        client2_ip = Entry(canvas)
        client2_ip.pack()
        client1_ip.pack()
        client2_ip.place(x=520, y=120)
        client1_ip.place(x=520, y=195)

        server_button = Button(canvas, text="Start", bg="black", fg="white", bd=0,
                               font="courier 18", activebackground="white", relief=FLAT)
        server_button.pack()
        server_button.place(x=480, y=240)

        jugador_L = Label(canvas, text='Jugador:', bg='black', fg='white', font='courier 22')
        jugador_L.pack()
        jugador_L.place(x=320, y=380)

        jugador1_r = Radiobutton(canvas, bg="black", value=2, variable=2)
        jugador2_r = Radiobutton(canvas, bg="black", value=1, variable=2)
        jugador1_r.pack()
        jugador2_r.pack()
        jugador1_r.place(x=530, y=390)
        jugador2_r.place(x=650, y=390)
        jugador1_r.select()

        jugador1_r_L = Label(canvas, bg='black', fg='white', text='1', font='courier 16')
        jugador2_r_L = Label(canvas, bg='black', fg='white', text='2', font='courier 16')
        jugador1_r_L.pack()
        jugador2_r_L.pack()
        jugador1_r_L.place(x=570, y=387)
        jugador2_r_L.place(x=690, y=387)

        server_ip_L = Label(canvas, bg='black', fg='white', text='Ip del servidor:', font='courier 18')
        server_ip_L.pack()
        server_ip_L.place(x=320, y=450)
        server_ip = Entry(canvas)
        server_ip.pack()
        server_ip.place(x=520, y=490)

        client_button = Button(canvas, text="Start", bg="black", fg="white", bd=0,
                               font="courier 18", activebackground="white", relief=FLAT)
        client_button.pack()
        client_button.place(x=480, y=530)

        def back():
            lan.destroy()
            root.deiconify()
            looping = False

        boton_v = Button(canvas, text="<volver>", bg="black", fg="white", bd=0, font="courier 18",
                         activebackground="white", relief=FLAT, command=back, state=ACTIVE)
        boton_v.pack()  # botón para la función mostrar4
        boton_v.place(x=20, y=540)

        looping = True

        while looping:

            if isserver:
                server.select()
                client1_ip.config(state=NORMAL)
                client2_ip.config(state=NORMAL)
                server_button.config(state=NORMAL)
                jugador1_r.config(state=DISABLED)
                jugador2_r.config(state=DISABLED)
                server_ip.config(state=DISABLED)
                client_button.config(state=DISABLED)
            elif isclient:
                client.select()
                client1_ip.config(state=DISABLED)
                client2_ip.config(state=DISABLED)
                server_button.config(state=DISABLED)
                jugador1_r.config(state=NORMAL)
                jugador2_r.config(state=NORMAL)
                server_ip.config(state=NORMAL)
                client_button.config(state=NORMAL)
            lan.update_idletasks()
            lan.update()
            time.sleep(0.01)



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

    #función para definir que se va a jugar sin trampolines
    def sinT():
        global tramp
        tramp = ''
    #valor default de tramp
    sinT()

    #función para definir que se va a jugar con trampolines
    def conT():
        global tramp
        tramp = True


    #Radiobutton que indica si se va a jugar en doubles o no
    doublesL2 = Label(canvas, text="Doubles", bg="black", fg="white", font="courier 14")
    doublesL2.pack()
    doublesL2.place(x=220,y=460)

    singlesL = Label(canvas, text="OFF", bg="black", fg="white", font="courier 14")
    singlesL.pack()
    singlesL.place(x=173, y=490)

    singles = Radiobutton(canvas,command=modeS, bg="black", variable=1, value=1, highlightbackground=current_color)
    singles.pack()
    singles.place(x=175, y=530)

    doublesL= Label(canvas, text="ON",bg="black", fg="white", font="courier 14")
    doublesL.pack()
    doublesL.place(x=318,y=490)

    doubles = Radiobutton(canvas, command=modeD, bg="black", variable=1,  value=2,highlightbackground=current_color)
    doubles.pack()
    doubles.place(x=315,y=530)

    #Radiobuttons que indican si se va a jugar con trampolines y sus labels
    trampolinesL = Label(canvas, text="Trampolines", bg="black", fg="white", font="courier 14")
    trampolinesL.pack()
    trampolinesL.place(x=460,y=460)

    tOnL = Label(canvas, text="ON", bg="black", fg="white", font="courier 14")
    tOnL.pack()
    tOnL.place(x=578,y=490)

    tOn = Radiobutton(canvas, command=conT, bg="black", value=2, variable=2)
    tOn.pack()
    tOn.place(x=575, y=530)

    tOffL = Label(canvas, text="OFF", bg="black", fg="white", font="courier 14")
    tOffL.pack()
    tOffL.place(x=433, y=490)

    tOff = Radiobutton(canvas, command=sinT, bg="black", value=1, variable=2)
    tOff.pack()
    tOff.place(x=435, y=530)

    # función  que abre el toplevelHelp y oculta el root, además de ejecutar el sonido de select
    def unir2():
        select_sound.play()
        toplevelHelp()

    # función usada para unir otras funciones: ejecutar el sonido select, destruir el root y ejecutar la clase Game en modo pvpc
    def unir3():
        global tramp
        global ver
        global current_color
        global MUTE

        MODE = ver
        OBS = tramp
        pygame.mixer.music.stop()
        root.withdraw()
        if arduino1 != 0:
            arduino1.close()

        if arduino2 != 0:
            arduino2.close()
        if current_color != '#000fff000':
            os.system('python3 main.py %s %r %r %r %s %r %s' %(MODE, True, MUTE, '', 'white', OBS, '1'))
        else:
            os.system('python3 main.py %s %r %r %r %s %r %s' %(MODE, True, MUTE, '', 'green', OBS, '1'))
        arduinos_setup()
        pygame.mixer.music.play(-1)
        muteI()
        root.deiconify()

    # función usada para unir otras funciones: ejecutar el sonido select, destruir el root y ejecutar la clase Game en modo pvp
    def unir4():
        global tramp
        global ver
        global MUTE
        global PT
        global select, starting
        global current_color
        global arduino1, arduino2
        MODE = ver
        OBS = tramp
        pygame.mixer.music.stop()
        root.withdraw()
        if arduino1 != 0:
            arduino1.close()
        if arduino2 != 0:
            arduino2.close()
        time.sleep(2)
        if current_color != '#000fff000':
            os.system('python3 main.py %s %r %r %r %s %r %s' %(MODE, '', MUTE, '', 'white', OBS, '1'))
        else:
            os.system('python3 main.py %s %r %r %r %s %r %s' %(MODE, '',MUTE, '', 'green', OBS, '1'))
        arduinos_setup()
        pygame.mixer.music.play(-1)
        muteI()

        root.deiconify()

    def color_w(*args):
        global current_color
        global pong
        current_color = 'white'
        pong = pong_white
        update_color()
        pongL.config(image=pong)


    def color_g(*args):
        global current_color
        global pong
        current_color = '#000fff000'
        pong = pong_green
        update_color()
        pongL.config(image=pong)

    def update_color():
        pvp.config(fg=current_color, activebackground=current_color)
        help1.config(fg=current_color, activebackground=current_color)
        pvpc.config(fg=current_color, activebackground=current_color)
        canvas.create_rectangle(5,5,795,595, fill="#000000",  outline=current_color, width=9 )
        canvas.create_rectangle(5,5,795,595, fill="#000000",  outline=current_color, width=1 )
        canvas.create_rectangle(30,220,50,380,fill=current_color,outline=current_color, width=5)
        canvas.create_rectangle(750,220,770,380,fill=current_color,outline=current_color, width=5)

        doubles.config(highlightbackground=current_color)
        singles.config(highlightbackground=current_color)
        doublesL.config(fg=current_color)
        singlesL.config(fg=current_color)
        hs.config(fg=current_color)
        pract.config(fg=current_color)
        lan.config(fg=current_color)

    root.bind('b', color_w)
    root.bind('v', color_g)

    def unir5():
        global ver
        global MUTE
        global PT
        global arduino1, arduino2
        MODE = ver
        pygame.mixer.music.stop()
        root.withdraw()
        if arduino1 != 0:
            arduino1.close()
        if arduino2 != 0:
            arduino2.close()
        os.system('python3 main.py %s %r %r %r' %(MODE, '', MUTE, True))
        arduinos_setup()
        pygame.mixer.music.play(-1)
        muteI()

        root.deiconify()

    def unir6():
        select_sound.play()
        toplevelHS()


    # botón que ejecuta el juego en modo pvp mediante unir4
    pvp = Button(canvas, command= unir4, text="Player vs Player",bg="black", fg="white", bd=0, font="courier 16", activebackground="white",relief=FLAT)
    pvp.place(x=145, y=255)

    # botón que ejeucta el juego en modo pvpc mediante unir3
    pvpc = Button(canvas, command=unir3, text="  Player vs PC  ",bg="black", fg="white", bd=0, font="courier 16", activebackground="white",relief=FLAT)
    pvpc.place(x=145, y=320)

    # botón que ejecuta la ventana de toplevelHelp mediante unir2
    help1 = Button(canvas,command=unir2, text="      Help      ",bg="black", fg="white", bd=0, font="courier 16", activebackground="white",relief=FLAT) #botón que ejecuta la ventana de toplevelHelp mediante unir2
    help1.place(x=145, y=385)

    # botón que ejeucta el juego en práctica
    pract = Button(canvas, command=pra_dif_ele, text="    Práctica    ", bg="black", fg="white", bd=0, font="courier 16",activebackground="white", relief=FLAT)
    pract.place(x=405, y=320)

    # bontón que ejecuta la ventana de highscores
    hs = Button(canvas, command=unir6, text="   Highscores   ", bg="black", fg="white", bd=0, font="courier 16", activebackground="white", relief=FLAT)  # botón que ejecuta la ventana de toplevelHelp mediante unir2
    hs.place(x=405, y=255)

    # bontón que ejecuta la ventana de el modo lan

    lan = Button(canvas, command=lan_win, text="    LAN Mode    ", bg="black", fg="white", bd=0, font="courier 16",activebackground="white", relief=FLAT)  # botón que ejecuta la ventana de toplevelHelp mediante unir2
    lan.place(x=405, y=385)

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

    update_color()

    singles.select()


    pygame.mixer.music.play(-1)

    selected =0

    while True:
        root.update_idletasks()
        root.update()
        if arduino1 != 0:
            raw1 = arduino1.read()
            arduino1_cmd = raw1.decode()
        else:
            arduino1_cmd = 'x'

        if arduino2 != 0:
            raw2 = arduino2.read()
            arduino2_cmd = raw2.decode()
        else:
            arduino2_cmd = 'x'


        if arduino1_cmd == 'u' or arduino2_cmd == 'u':
            if selected > 0 and selected-1 != 19 and selected-1 != 18:
                selected -= 1
        elif arduino1_cmd == 'd' or arduino2_cmd == 'd':
            if selected < 10 or 20 <= selected <= 23:
                selected += 1
        elif arduino1_cmd == 'v' or arduino2_cmd == 'v':
            color_g()
        elif arduino1_cmd == 'b' or arduino2_cmd == 'b':
            color_w()
        elif arduino1_cmd == 'm' or arduino2_cmd == 'm':
            muteF()
        if arduino1_cmd == 's' or arduino2_cmd == 's':
            select = True
        else:
            select = False
        if selected == 0:
            pvp.config(state=ACTIVE)
            pvpc.config(state=NORMAL)
            help1.config(state=NORMAL)
            pract.config(state=NORMAL)
            singles.config(state=NORMAL)
            doubles.config(state=NORMAL)
            hs.config(state=NORMAL)
            pract.config(state=NORMAL)
            lan.config(state=NORMAL)
            tOn.config(stat=NORMAL)
            tOff.config(stat=NORMAL)
            if select:
                unir4()
        elif selected == 1:
            pvp.config(state=NORMAL)
            pvpc.config(state=NORMAL)
            help1.config(state=NORMAL)
            pract.config(state=NORMAL)
            singles.config(state=NORMAL)
            doubles.config(state=NORMAL)
            hs.config(state=ACTIVE)
            pract.config(state=NORMAL)
            lan.config(state=NORMAL)
            tOn.config(stat=NORMAL)
            tOff.config(stat=NORMAL)
            if select:
                unir6()
                boton_v.config(state=ACTIVE)
                selected = 10
        elif selected == 2:
            pvp.config(state=NORMAL)
            pvpc.config(state=ACTIVE)
            help1.config(state=NORMAL)
            pract.config(state=NORMAL)
            singles.config(state=NORMAL)
            doubles.config(state=NORMAL)
            hs.config(state=NORMAL)
            pract.config(state=NORMAL)
            lan.config(state=NORMAL)
            tOn.config(stat=NORMAL)
            tOff.config(stat=NORMAL)
            if select:
                unir3()
        elif selected == 3:
            pvp.config(state=NORMAL)
            pvpc.config(state=NORMAL)
            help1.config(state=NORMAL)
            pract.config(state=ACTIVE)
            singles.config(state=NORMAL)
            doubles.config(state=NORMAL)
            hs.config(state=NORMAL)
            lan.config(state=NORMAL)
            tOn.config(stat=NORMAL)
            tOff.config(stat=NORMAL)
            if select:
                pra_dif_ele()
                selected = 20
        elif selected == 4:
            pvp.config(state=NORMAL)
            pvpc.config(state=NORMAL)
            help1.config(state=ACTIVE)
            pract.config(state=NORMAL)
            singles.config(state=NORMAL)
            doubles.config(state=NORMAL)
            hs.config(state=NORMAL)
            pract.config(state=NORMAL)
            lan.config(state=NORMAL)
            tOn.config(stat=NORMAL)
            tOff.config(stat=NORMAL)
            if select:
                unir2()
                selected = 10
        elif selected == 5:
            pvp.config(state=NORMAL)
            pvpc.config(state=NORMAL)
            help1.config(state=NORMAL)
            pract.config(state=NORMAL)
            singles.config(state=NORMAL)
            doubles.config(state=NORMAL)
            hs.config(state=NORMAL)
            pract.config(state=NORMAL)
            lan.config(state=ACTIVE)
            tOn.config(stat=NORMAL)
            tOff.config(stat=NORMAL)
            if select:
                lan_win()
                selected = 0
        elif selected == 6:
            pvp.config(state=NORMAL)
            pvpc.config(state=NORMAL)
            help1.config(state=NORMAL)
            pract.config(state=NORMAL)
            singles.config(state=ACTIVE)
            doubles.config(state=NORMAL)
            hs.config(state=NORMAL)
            pract.config(state=NORMAL)
            lan.config(state=NORMAL)
            tOn.config(stat=NORMAL)
            tOff.config(stat=NORMAL)
            if select:
                singles.select()
                modeS()
        elif selected == 7:
            pvp.config(state=NORMAL)
            pvpc.config(state=NORMAL)
            help1.config(state=NORMAL)
            pract.config(state=NORMAL)
            singles.config(state=NORMAL)
            doubles.config(state=ACTIVE)
            hs.config(state=NORMAL)
            pract.config(state=NORMAL)
            lan.config(state=NORMAL)
            tOn.config(stat=NORMAL)
            tOff.config(stat=NORMAL)
            if select:
                doubles.select()
                modeD()
        elif selected == 8:
            pvp.config(state=NORMAL)
            pvpc.config(state=NORMAL)
            help1.config(state=NORMAL)
            pract.config(state=NORMAL)
            singles.config(state=NORMAL)
            doubles.config(state=NORMAL)
            hs.config(state=NORMAL)
            pract.config(state=NORMAL)
            lan.config(state=NORMAL)
            tOn.config(stat=NORMAL)
            tOff.config(stat=ACTIVE)
            if select:
                tOff.select()
                sinT()
        elif selected == 9:
            pvp.config(state=NORMAL)
            pvpc.config(state=NORMAL)
            help1.config(state=NORMAL)
            pract.config(state=NORMAL)
            singles.config(state=NORMAL)
            doubles.config(state=NORMAL)
            hs.config(state=NORMAL)
            pract.config(state=NORMAL)
            lan.config(state=NORMAL)
            tOn.config(stat=ACTIVE)
            tOff.config(stat=NORMAL)
            if select:
                tOn.select()
                conT()
        elif selected == 10:
            if select:
                selected = 0
                unir1()
        elif selected == 20:
            boton_e.config(state=ACTIVE)
            boton_m.config(state=NORMAL)
            boton_v.config(state=NORMAL)
            boton_h.config(state=NORMAL)
            if select:
                unir2()
        elif selected == 21:
            boton_m.config(state=ACTIVE)
            boton_e.config(state=NORMAL)
            boton_h.config(state=NORMAL)
            boton_v.config(state=NORMAL)
            if select:
                unir3()
        elif selected == 22:
            boton_h.config(state=ACTIVE)
            boton_e.config(state=NORMAL)
            boton_m.config(state=NORMAL)
            boton_v.config(state=NORMAL)
            if select:
                unir4()
        elif selected == 23:
            boton_v.config(state=ACTIVE)
            boton_e.config(state=NORMAL)
            boton_m.config(state=NORMAL)
            boton_h.config(state=NORMAL)
            if select:
                selected = 0
                unir1()


def arduinos_setup():
    global arduino2, arduino1
    try:
        arduino1 = serial.Serial('/dev/ttyACM0', 9600)
    except:
        arduino1 = 0

    try:
        arduino2 = serial.Serial('/dev/ttyUSB0', 4800)
    except:
        arduino2 = 0

arduinos_setup()
root()