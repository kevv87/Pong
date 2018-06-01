import pyfirmata
import time

placa = pyfirmata.Arduino('/dev/ttyACM0')

pyfirmata.util.Iterator(placa).start()

A = placa.get_pin('d:13:o')
B = placa.get_pin('d:11:o')
C = placa.get_pin('d:10:o')
D = placa.get_pin('d:9:o')
E = placa.get_pin('d:8:o')
G = placa.get_pin('d:7:o')
F = placa.get_pin('d:6:o')
DP = placa.get_pin('d:12:o')


def numeros(num):
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

for i in range(1, 10):
    numeros(i)
    time.sleep(1)

