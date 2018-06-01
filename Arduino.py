import pyfirmata

placa = pyfirmata.Arduino('/dev/ttyACM0')

pyfirmata.util.Iterator(placa).start()

entrada = placa.get_pin('d:8:i')
entrada.enable_reporting()
salida = placa.get_pin('d:12:o')

try:
    encendido = False
    while True:
        if entrada.read():
            encendido = not encendido
            salida.write(encendido)
            placa.pass_time(0.2)

finally:
    salida.write(False)
    placa.exit()