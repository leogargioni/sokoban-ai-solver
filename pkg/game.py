BOX = '$'
STORAGE = '.'
SPACE = ' '
WALL = '#'
BOX_ON_GOAL = '*'

class Game:
    """Maze representa um labirinto com paredes. A indexação das posições do labirinto é dada por par ordenado (linha, coluna).
    A linha inicial é zero e a linha máxima é (maxLin - 1). A coluna inicial é zero e a máxima é (maxCol - 1)."""

    def __init__(self, maxRows, maxColumns):
        """Construtor do labirinto
        @param maxRows: número de linhas do labirinto
        @param maxColumns: número de colunas do labirinto
        """
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.map = [[SPACE for j in range(maxColumns)] for i in range(maxRows)] # Matriz que representa o jogo

    def putHorizontalWall(self, begin, end, row):
        """Constrói parede horizontal da coluna begin até a coluna end(inclusive) na linha row.
        @param begin: coluna inicial entre 0 e maxColumns - 1.
        @param end: coluna final (deve ser maior que begin).
        @param row: linha onde a parede deve ser colocada."""
        if(end >= begin and begin >= 0 and end < self.maxColumns and row >= 0 and row < self.maxRows):
            for col in range(begin,end+1,1):
                self.map[row][col] = WALL
    
    def putVerticalWall(self, begin, end, col):
        """Constrói parede horizontal da linha begin até a linha end(inclusive) na coluna col.
        @param begin: linha inicial entre 0 e maxRows - 1.
        @param end: linha final (deve ser maior que begin).
        @param col: coluna onde a parede deve ser colocada."""
        if(end >= begin and begin >= 0 and end < self.maxRows and col >= 0 and col < self.maxColumns):
            for row in range(begin,end+1,1):
                self.map[row][col] = WALL

    def setBoxPos(self, row, col):
        """Utilizada para colocar um objetivo na posição inicial.
        @param row: a linha onde o objetivo será situado.
        @param col: a coluna onde o objetivo será situado.
        @return 1 se o posicionamento é possível, -1 se não for."""
        if (col < 0 or row < 0):
            return -1
        if (col >= self.maxColumns or row >= self.maxRows):
            return -1
        
        if self.map[row][col] == WALL or self.map[row][col] == BOX or self.map[row][col] == STORAGE:
            return -1

        self.map[row][col] = BOX
        return 1

    def setStoragePos(self, row, col):
        """Utilizada para colocar um objetivo na posição inicial.
        @param row: a linha onde o objetivo será situado.
        @param col: a coluna onde o objetivo será situado.
        @return 1 se o posicionamento é possível, -1 se não for."""
        if (col < 0 or row < 0):
            return -1
        if (col >= self.maxColumns or row >= self.maxRows):
            return -1
        
        if self.map[row][col] == WALL or self.map[row][col] == BOX or self.map[row][col] == STORAGE:
            return -1

        self.map[row][col] = STORAGE
        return 1