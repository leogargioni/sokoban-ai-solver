from game import Game
from state import *
from cardinal import *
import copy

class Problem:
    """Representação de um problema a ser resolvido por um algoritmo de busca clássica.
    A formulação do problema - instância desta classe - reside na 'mente' do agente."""


    def __init__(self):
        self.initialState = State(0,0)

    def createGame(self, maxRows, maxColumns, map):
        """Este método instancia um jogo - representa o que o agente crê ser o jogo.
        @param maxRows: máximo de linhas do labirinto.
        @param maxColumns: máximo de colunas do labirinto."""
        self.gameBelief = Game(maxRows, maxColumns)
        self.gameBelief.map = map
        #self.maxRows = maxRows
        #self.maxColumns = maxColumns
        self.cost = [[0.0 for j in range(maxRows*maxColumns)]for i in range(8)]

    def suc(self, state, action):
        """Função sucessora: recebe um estado e calcula o estado sucessor ao executar uma ação.
        @param state: estado atual.
        @param action: ação a ser realizado a partir do estado state.
        @return estado sucessor"""
        row = state.row
        col = state.col

        # Incrementa a linha e coluna de acordo com a respectiva ação
        # rowIncrement e colIncrement estão definidos em cardinal.py
        row += rowIncrement[action]
        col += colIncrement[action]

        subsequentRow = row + rowIncrement[action]
        subsequentCol = col + colIncrement[action]

        # # Se tiver parede o agente fica na posição original
        # if self.gameBelief.map[row][col] == WALL:
        #     row = state.row
        #     col = state.col

        # # Retorna agora se não consegue mover
        # if row == state.row and col == state.col:
        #     return state

        #Cria um novo estado a partir de uma cópia do atual
        map = state.map
        newState = copy.deepcopy(state)

        if map[row][col] in [BOX, BOX_ON_GOAL, DEADLOCK_BOX_ON_GOAL]:
            # Empurra caixa
            if map[subsequentRow][subsequentCol] == STORAGE:
                newState.map[subsequentRow][subsequentCol] = BOX_ON_GOAL
            else:
                newState.map[subsequentRow][subsequentCol] = BOX

            if map[row][col] in [BOX_ON_GOAL, DEADLOCK_BOX_ON_GOAL]:
                newState.map[row][col] = STORAGE
            else:
                newState.map[row][col] = SPACE

        # Move o agente
        newState.row = row
        newState.col = col

        # Finaliza 
        newState.setDictKey()
        return newState

    def possibleActionsWithoutCollaterals(self, state):
        """Retorna as ações possíveis de serem executadas em um estado, desconsiderando movimentos na diagonal.
        O valor retornado é um vetor de inteiros.
        Se o valor da posição é -1 então a ação correspondente não pode ser executada, caso contrário valerá 1.
        Exemplo: se retornar [1, -1, -1, -1, -1, -1, -1, -1] apenas a ação 0 pode ser executada, ou seja, apena N.
        @param state: estado atual.
        @return ações possíveis"""
        
        actions = [1,-1,1,-1,1,-1,1,-1] # Supõe que todas as ações (menos na diagonal) são possíveis

        # @TODO: Implementação do aluno - DONE

        row = state.row
        col = state.col 

        state.staticDeadlock()
        map = state.map
        # Testa se há parede nas direções
        if actions[N] != -1 and map[row - 1][col] == WALL: # Norte
            actions[N] = -1
        if actions[L] != -1 and map[row][col + 1] == WALL: # Leste
            actions[L] = -1
        if actions[S] != -1 and map[row + 1][col] == WALL: # Sul
            actions[S] = -1
        if actions[O] != -1 and map[row][col - 1] == WALL: # Oeste
            actions[O] = -1

        # Testa se caixas podem ser empurradas (se não há parede, outra caixa ou deadlock estático no espaço seguinte)
        if actions[N] != -1 and map[row - 1][col] in [BOX, BOX_ON_GOAL, DEADLOCK_BOX_ON_GOAL]: # Norte
            if map[row - 2][col] in [BOX, BOX_ON_GOAL, WALL, DEADLOCK, DEADLOCK_BOX_ON_GOAL]:
                actions[N] = -1
        if actions[L] != -1 and map[row][col + 1] in [BOX, BOX_ON_GOAL, DEADLOCK_BOX_ON_GOAL]: # Leste
            if map[row][col + 2] in [BOX, BOX_ON_GOAL, WALL, DEADLOCK, DEADLOCK_BOX_ON_GOAL]:
                actions[L] = -1
        if actions[S] != -1 and map[row + 1][col] in [BOX, BOX_ON_GOAL, DEADLOCK_BOX_ON_GOAL]: # Sul
            if map[row + 2][col] in [BOX, BOX_ON_GOAL, WALL, DEADLOCK, DEADLOCK_BOX_ON_GOAL]:
                actions[S] = -1
        if actions[O] != -1 and map[row ][col - 1] in [BOX, BOX_ON_GOAL, DEADLOCK_BOX_ON_GOAL]: # Oeste
            if map[row][col - 2] in [BOX, BOX_ON_GOAL, WALL, DEADLOCK, DEADLOCK_BOX_ON_GOAL]:
                actions[O] = -1

        return actions

    def getActionCost(self, action):
        """Retorna o custo da ação.
        @param action:
        @return custo da ação"""
        if (action == N or action == L or action == O or action == S):
            return 1.0
        else:
            return 1.5

    def goalTest(self, currentState):
        """Testa se alcançou o estado objetivo.
        @param currentState: estado atual.
        @return True se o estado atual for igual ao estado objetivo."""

        return currentState.isSolution()
