import pyfirmata
import time
import pygame
import random

pygame.init()

placa1 = pyfirmata.Arduino('/dev/ttyACM0')

pyfirmata.util.Iterator(placa1).start()
display1_leds = []

display1_leds.append(placa1.get_pin('d:9:o'))
display1_leds.append(placa1.get_pin('d:8:o'))
display1_leds.append(placa1.get_pin('d:5:o'))
display1_leds.append(placa1.get_pin('d:6:o'))
display1_leds.append(placa1.get_pin('d:7:o'))
display1_leds.append(placa1.get_pin('d:2:o'))
display1_leds.append(placa1.get_pin('d:3:o'))
display1_leds.append(placa1.get_pin('d:13:o'))


A = display1_leds[0]
B = display1_leds[1]
C = display1_leds[2]
D = display1_leds[3]
E = display1_leds[4]
F = display1_leds[5]
G = display1_leds[6]
DP = display1_leds[7]

def numeros(num):
    global A,B,C,D,E,F,G,DP
    if num == 1:
        A.write(True)
        B.write(False)
        C.write(False)
        D.write(True)
        E.write(True)
        F.write(True)
        G.write(True)
        DP.write(True)
    if num == 2:
        A.write(False)
        B.write(False)
        C.write(True)
        G.write(False)
        E.write(False)
        D.write(False)
        F.write(True)
        DP.write(True)
    if num == 3:
        B.write(False)
        A.write(False)
        G.write(False)
        C.write(False)
        D.write(False)
        E.write(True)
        F.write(True)
        DP.write(True)
    if num == 4:
        A.write(True)
        B.write(False)
        F.write(False)
        G.write(False)
        C.write(False)
        D.write(True)
        E.write(True)
        DP.write(True)
    if num == 5:
        A.write(False)
        B.write(True)
        C.write(False)
        D.write(False)
        E.write(True)
        G.write(False)
        F.write(False)
        DP.write(True)
    if num == 6:
        A.write(False)
        B.write(True)
        C.write(False)
        D.write(False)
        E.write(False)
        G.write(False)
        F.write(False)
        DP.write(True)
    if num == 7:
        A.write(False)
        B.write(False)
        C.write(False)
        D.write(True)
        E.write(True)
        F.write(True)
        G.write(True)
        DP.write(True)
    if num == 8:
        A.write(False)
        B.write(False)
        C.write(False)
        D.write(False)
        E.write(False)
        G.write(False)
        F.write(False)
        DP.write(True)
    if num == 9:
        A.write(False)
        B.write(False)
        C.write(False)
        D.write(False)
        E.write(True)
        G.write(False)
        F.write(False)
        DP.write(True)

while True:
    A.write(False)
    B.write(False)
    C.write(False)
    D.write(False)
    E.write(False)
    G.write(False)
    F.write(False)
    DP.write(False)



#for i in range(10):
   # print(i)
   # numeros(i)
   # time.sleep(1)
'''

entrada1 = placa.get_pin('d:8:i')
entrada1.enable_reporting()

entrada2 = placa.get_pin('d:9:i')
entrada2.enable_reporting()

entrada3 = placa.get_pin('d:10:i')
entrada3.enable_reporting()

white = (255,255,255)
green = (0,255,0)

gameDisplay = pygame.display.set_mode((800,600))
x = random.randint(0,600)
y = random.randint(0,400)
if entrada1.read() == 1.0:
    print("HOLA1")
        pygame.draw.rect(gameDisplay, green, [x, y,
                                                  20, 24])
        elif entrada2.read():
            print("HOLA2")
            pygame.draw.rect(gameDisplay, white, [x, y,
                                                  20, 24])
        elif entrada3.read():
            print("HOLA3")
            pygame.draw.rect(gameDisplay, white, [x, y,
                                                  20, 24])
        else:
            pass
        pygame.display.update()
        placa.pass_time(0.2)
finally:
    placa.exit()
'''