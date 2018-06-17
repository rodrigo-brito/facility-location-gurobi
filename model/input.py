import sys

class Data:
    def __init__(self, fileName):
        print("Reading input file %s" % fileName)
        self.file = open(fileName, "r")
        self.loadData()
        self.file.close()

    def nextLine(self):
        line = self.file.readline().strip()
        if not line:
            return self.nextLine()
        return line

    def loadData(self):
        self.size = int(self.nextLine())
        self.alpha = float(self.nextLine())

        ex = 1.0
        if self.size >= 170:
            ex = 5.0
        elif self.size >= 70:
            ex = 2.0

        self.fixedCost = []
        for i in range(self.size):
            self.fixedCost.append(float(self.nextLine()) * ex / 10000.0)

        self.flow = {}
        for i in range(self.size):
            line = self.nextLine()
            for j, value in enumerate(line.split()):
                self.flow[(i, j)] = float(value) / 100.0

        self.cost = {}
        for i in range(self.size):
            line = self.nextLine()
            for j, value in enumerate(line.split()):
                self.cost[(i, j)] = float(value) / 100.0



