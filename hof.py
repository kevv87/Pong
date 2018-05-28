import pygame

class HOF:
    def __init__(self):
        self.path = 'highscores.txt'

        self.file = open(self.path, 'r')

        contents = []

        for line in self.file:
            contents.append(line[:len(line)-1])

        self.final = []

        k = 0

        for i in contents:
            self.final.append(i.split('%'))
            self.final[k][1] = int(self.final[k][1])
            k += 1

        self.file.close()

    def verify(self, valor):
        self.file = open(self.path, 'w')
        name = input()
        cont = False
        for line in self.final:
            if valor < line[1] and not cont:
                self.file.write(name+'%'+str(valor)+'\n')
                cont = True
            else:
                self.file.write(line[0]+'%'+str(line[1])+'\n')
a = HOF()
a.verify(4)