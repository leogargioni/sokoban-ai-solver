from view import View
from game import *
from cardinal import *

class Model:
    """Model implementa um ambiente na forma de um labirinto com paredes e com um agente.
     A indexação da posição do agente é feita sempre por um par ordenado (lin, col). Ver classe Labirinto."""

    def __init__(self, rows, columns):
        """Construtor de modelo do ambiente físico
        @param rows: número de linhas do labirinto
        @param columns: número de colunas do labirinto
        """
        if rows <= 0:
            rows = 5
        if columns <= 0:
            columns = 5

        self.rows = rows
        self.columns = columns

        self.agentPos = [0,0]

        self.view = View(self)
        self.game = Game(rows,columns)

    def draw(self):
        """Desenha o labirinto em formato texto."""
        self.view.draw()

    def setAgentPos(self, row, col):
        """Utilizada para colocar o agente na posição inicial.
        @param row: a linha onde o agente será situado.
        @param col: a coluna onde o agente será situado.
        @return 1 se o posicionamento é possível, -1 se não for."""
        if (col < 0 or row < 0):
            return -1
        if (col >= self.game.maxColumns or row >= self.game.maxRows):
            return -1

        if self.game.map[row][col] == WALL or self.game.map[row][col] == BOX:
            return -1

        self.agentPos[0] = row
        self.agentPos[1] = col
        return 1

    def go(self, direction):
        """Coloca o agente na posição solicitada pela ação go, desde que seja possível.
        Não pode ultrapassar os limites do labirinto nem estar em uma parede.
        @param direciton: inteiro de 0 a 7 representado as coordenadas conforme definido em cardinal.py"""
        row = self.agentPos[0]
        col = self.agentPos[1]

        if direction == N:
            row -= 1
            subsequentRow = row - 1
            subsequentCol = col
        if direction == L:
            col += 1
            subsequentRow = row
            subsequentCol = col + 1
        if direction == S:
            row += 1
            subsequentRow = row + 1
            subsequentCol = col
        if direction == O:
            col -= 1
            subsequentRow = row
            subsequentCol = col - 1

        # Verifica se está fora do grid
        if col < 0 or col >= self.game.maxColumns:
            return
        if row < 0 or row >= self.game.maxRows:
            return

        # Verifica se bateu em uma parede
        if self.game.map[row][col] == WALL:
            return

        # Verifica se é possível mover uma caixa
        if (self.game.map[row][col] == BOX or self.game.map[row][col] == BOX_ON_GOAL) and (subsequentCol < 0 or subsequentCol >= self.game.maxColumns):
            return
        if (self.game.map[row][col] == BOX or self.game.map[row][col] == BOX_ON_GOAL) and (subsequentRow < 0 or subsequentRow >= self.game.maxRows):
            return
        if (self.game.map[row][col] == BOX or self.game.map[row][col] == BOX_ON_GOAL) and self.game.map[subsequentRow][subsequentCol] == WALL:
            return
        if (self.game.map[row][col] == BOX or self.game.map[row][col] == BOX_ON_GOAL) and (self.game.map[subsequentRow][subsequentCol] == BOX or self.game.map[subsequentRow][subsequentCol] == BOX_ON_GOAL):
            return 

        # Finalizar o movimento
        if self.game.map[row][col] == BOX or self.game.map[row][col] == BOX_ON_GOAL: # movimentando uma caixa
            #Atualiza lugar que o Agente vai Ficar
            if self.game.map[row][col] == BOX_ON_GOAL:
                self.game.map[row][col] = STORAGE
            else:
                self.game.map[row][col] = SPACE
            #Atualiza lugar que a Caixa vai Ficar
            if self.game.map[subsequentRow][subsequentCol] == STORAGE:
                self.game.map[subsequentRow][subsequentCol] = BOX_ON_GOAL
            else:
                self.game.map[subsequentRow][subsequentCol] = BOX
        self.agentPos = [row,col]
