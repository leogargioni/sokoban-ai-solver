from game import *

class View:
    """Desenha o ambiente (o que está representado no Model) em formato texto."""
    def __init__(self, model):
        self.model = model

    def drawRowDivision(self):
        print("    ", end='')
        for _ in range(self.model.columns):
            print("+---", end='')
        print("+")

    def drawHeader(self):
        print("--- Estado do Ambiente ---")
        print("Posição agente  : {0},{1}".format(self.model.agentPos[0],self.model.agentPos[1]))

        # Imprime números das colunas
        print("   ", end='')
        for col in range(self.model.columns):
            print(" {0:2d} ".format(col), end='')

        print()

    def draw(self):
        """Desenha o jogo."""
        self.drawHeader()

        for row in range(self.model.rows):
            self.drawRowDivision()
            print(" {0:2d} ".format(row), end='') # Imprime número da linha

            for col in range(self.model.columns):
                if self.model.agentPos[0] == row and self.model.agentPos[1] == col:
                    print("| A ",end='')    # Desenha agente
                elif self.model.game.map[row][col] == WALL:
                    print("|###",end='')    # Desenha parede
                else:
                    print("| ",self.model.game.map[row][col]," ",sep='',end='')
            
            print("|")

            if row == (self.model.rows - 1):
                self.drawRowDivision()