from model import Model
from problem import Problem
from state import *
from cardinal import action
from tree import TreeNode
import copy
import sys

UNIFORME_COST = 0
A_STAR = 1
GREEDY = 2

# select Algorithm and Heuristic (1 or 2)
SEARCH_STRATEGY = A_STAR
hn = 1

# Funções utilitárias
def printExplored(explored):
    """Imprime os nós explorados pela busca.
    @param explored: lista com os nós explorados."""
    #@TODO: Implementação do aluno
    print("--- Explorados --- (TAM: {})".format(len(explored)))
    #for state in explored.values():
    #    print(state,end=' ')
    print("\n")

def printFrontier(frontier):
    """Imprime a fronteira gerada pela busca.
    @param frontier: lista com os nós da fronteira."""
    #@TODO: Implementação do aluno
    print("--- Fronteira --- (TAM: {})".format(len(frontier)))
    #for node in frontier.values():
    #    print(node,end=' ')
    print("\n")

def buildPlan(solutionNode):
    #@TODO: Implementação do aluno
    depth = solutionNode.depth
    solution = [0 for i in range(depth)]
    parent = solutionNode

    for i in range(len(solution) - 1, -1, -1):
        solution[i] = parent.action
        parent = parent.parent
    return solution


class Agent:
    """"""
    counter = -1 # Contador de passos no plano, usado na deliberação

    def __init__(self, model):
        """Construtor do agente.
        @param model: Referência do ambiente onde o agente atuará."""
        self.model = model

        self.prob = Problem()
        self.prob.createGame(self.model.rows, self.model.columns, self.model.game.map)

        # Posiciona fisicamente o agente no estado inicial
        initialState = self.gameSensor()
        self.prob.initialState = initialState
        
        # Define o estado atual do agente = estado inicial
        self.currentState = self.prob.initialState

        # Define o estado objetivo
        #self.prob.defGoalState(2, 8)
        #self.model.setGoalPos(2,8)

        # Plano de busca
        self.plan = None

    def printPlan(self):
        """Apresenta o plano de busca."""    
        print("--- PLANO ---")
        # @TODO: Implementação do aluno
        for plannedAction in self.plan:
            print("{} > ".format(action[plannedAction]),end='')
        print("FIM\n\n")

    def deliberate(self):
        #Primeira chamada, realiza busca para elaborar um plano
        #@TODO: Implementação do aluno
        if self.counter == -1: 
            self.plan = self.cheapestFirstSearch(SEARCH_STRATEGY) # 0 = custo uniforme, 1 = A*, 2 = Gulosa
            if self.plan != None:
                self.printPlan()
            else:
                print("SOLUÇÃO NÃO ENCONTRADA")
                return -1

        # Nas demais chamadas, executa o plano já calculado
        self.counter += 1

        # Atingiu o estado objetivo 
        if self.prob.goalTest(self.currentState):
            print("!!! ATINGIU O ESTADO OBJETIVO !!!")
            return -1
        # Algo deu errado, chegou ao final do plano sem atingir o objetivo
        if self.counter >= len(self.plan):
            print("### ERRO: plano chegou ao fim, mas objetivo não foi atingido.")
            return -1
        currentAction = self.plan[self.counter]

        print("--- Mente do Agente ---")
        print("{0:<20}{1}".format("Estado atual :",self.currentState))
        print("{0:<20}{1} de {2}. Ação= {3}\n".format("Passo do plano :",self.counter + 1,len(self.plan),action[currentAction]))
        self.executeGo(currentAction)

        # Atualiza o estado atual baseando-se apenas nas suas crenças e na função sucessora
        # Não faz leitura do sensor de posição
        self.currentState = self.prob.suc(self.currentState, currentAction)
        return 1

    def executeGo(self, direction):
        """Atuador: solicita ao agente física para executar a ação.
        @param direction: Direção da ação do agente
        @return 1 caso movimentação tenha sido executada corretamente."""
        self.model.go(direction)
        return 1

    def gameSensor(self):
        """Simula um sensor que realiza a leitura do jogo atual no ambiente e traduz para uma instância da classe Estado.
        @return estado que representa o jogo atual."""
        state = State(self.model.rows,self.model.columns)
        state.row = self.model.agentPos[0]
        state.col = self.model.agentPos[1]
        state.map = copy.deepcopy(self.model.game.map)
        state.setDictKey()
        return state

    # Manhattan Distance between two points
    def manDistance(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def hn1(self, state):
        """Implementa uma heurística baseada em distância Manhattan.
        @param state: estado para o qual se quer calcular o valor de h(n)."""

        # Gerar todas as possíveis combinações entre caixas e objetivos
        best = 0
        for b in state.getUnplacedBoxes():
            boxBest = sys.maxsize

            for g in state.getAllGoals():
                hMaxSize = False

                # Se quatro objetos estiverem juntos eles formam um deadlock
                if b != g:
                    if state.map[b[0]+1][b[1]] in OBJECT:
                        if state.map[b[0]+1][b[1]-1] in OBJECT:
                            if state.map[b[0]][b[1]-1] in OBJECT:
                                hMaxSize = True
                    if not hMaxSize and state.map[b[0]+1][b[1]] in OBJECT:
                        if state.map[b[0]+1][b[1]+1] in OBJECT:
                            if state.map[b[0]][b[1]+1] in OBJECT:
                                hMaxSize = True
                    if not hMaxSize and state.map[b[0]-1][b[1]] in OBJECT:
                        if state.map[b[0]-1][b[1]-1] in OBJECT:
                            if state.map[b[0]][b[1]-1] in OBJECT:
                                hMaxSize = True
                    if not hMaxSize and state.map[b[0]-1][b[1]] in OBJECT:
                        if state.map[b[0]-1][b[1]+1] in OBJECT:
                            if state.map[b[0]][b[1]+1] in OBJECT:
                                hMaxSize = True

                if not hMaxSize:
                    # Descobrir qual a Menor Distância Manhattan de uma caixa para algum dos objetivos
                    if self.manDistance(b,g) < boxBest:
                        boxBest = self.manDistance(b,g)
            
            # Se não encontrar um deadlock, somar as menores disâncias das caixas para os objetivos
            if best != sys.maxsize and boxBest < sys.maxsize:
                best += boxBest
            else:
                best = sys.maxsize

        #print("----------------------------------------- final heuristic:", best)
        return best


    def hn2(self, state):
        """Implementa uma heurística alternativa não ótima.
        @param state: estado para o qual se quer calcular o valor de h(n)."""

        solutions = []
        for b in state.getUnplacedBoxes():
            solution = []

            for g in state.getFreeGoals():
                movements = 0
                hMaxSize = False

                # Se quatro objetos estiverem juntos eles formam um deadlock
                if b != g:
                    if state.map[b[0]+1][b[1]] in OBJECT:
                        if state.map[b[0]+1][b[1]-1] in OBJECT:
                            if state.map[b[0]][b[1]-1] in OBJECT:
                                hMaxSize = True
                    if not hMaxSize and state.map[b[0]+1][b[1]] in OBJECT:
                        if state.map[b[0]+1][b[1]+1] in OBJECT:
                            if state.map[b[0]][b[1]+1] in OBJECT:
                                hMaxSize = True
                    if not hMaxSize and state.map[b[0]-1][b[1]] in OBJECT:
                        if state.map[b[0]-1][b[1]-1] in OBJECT:
                            if state.map[b[0]][b[1]-1] in OBJECT:
                                hMaxSize = True
                    if not hMaxSize and state.map[b[0]-1][b[1]] in OBJECT:
                        if state.map[b[0]-1][b[1]+1] in OBJECT:
                            if state.map[b[0]][b[1]+1] in OBJECT:
                                hMaxSize = True

                if not hMaxSize:
                    # Mover p/ esquerda
                    if g[1]<b[1]:
                        if b[1]+2 == state.cols: #Deadlock px à parede externa
                            hMaxSize = True
                        elif abs(g[0]-b[0]) == 0: # Movimento em linha reta
                            if state.col <= b[1]: #Agente do lado oposto
                                movements += 2
                            for a,v in enumerate(state.map[b[0]]): #Objeto no caminho
                                if a > g[1] and a < b[1] and v in [BOX, BOX_ON_GOAL, WALL, DEADLOCK, DEADLOCK_BOX_ON_GOAL]:
                                    movements += 2
                                    break
                        else: #Movimento em duas direções
                            movements += 1
                            if state.col <= b[1]: #Agente do lado oposto
                                if (g[0] < b[0] and state.row <= b[0]) or (g[0] > b[0] and state.row >= b[0]):
                                    #+2 caso esteja dentro da área
                                    movements += 1
                    # Mover p/ direita
                    if g[1]>b[1]:
                        if b[1]-1 == 0: #Deadlock px à parede externa
                            hMaxSize = True
                        elif abs(g[0]-b[0]) == 0: # Movimento em linha reta
                            if state.col >= b[1]: #Agente do lado oposto
                                movements += 2
                            for a,v in enumerate(state.map[b[0]]):  #Objeto no caminho
                                if a < g[1] and a > b[1] and v in [BOX, BOX_ON_GOAL, WALL, DEADLOCK, DEADLOCK_BOX_ON_GOAL]:
                                    movements += 2
                                    break
                        else: #Movimento em duas direções
                            movements += 1
                            if state.col >= b[1]: #Agente do lado oposto
                                if (g[0] < b[0] and state.row <= b[0]) or (g[0] > b[0] and state.row >= b[0]):
                                    #+2 caso esteja dentro da área
                                    movements += 1
                    # Mover p/ baixo
                    if g[0]>b[0]:
                        if b[0]-1 == 0: #Deadlock px à parede externa
                            hMaxSize = True
                        elif abs(g[1]-b[1]) == 0: # Movimento em linha reta
                            if state.row >= b[0]: #Agente do lado oposto
                                movements += 2
                            for a,v in enumerate(state.map[b[1]]): #Objeto no caminho
                                if a < g[0] and a > b[0] and v in [BOX, BOX_ON_GOAL, WALL, DEADLOCK, DEADLOCK_BOX_ON_GOAL]:
                                    movements += 2
                                    break
                        else: #Movimento em duas direções
                            movements += 1
                            if state.row >= b[0]: #Agente do lado oposto
                                if (g[1] < b[1] and state.col <= b[1]) or (g[1] > b[1] and state.col >= b[1]):
                                    #+2 caso esteja dentro da área
                                    movements += 1
                    # Mover p/ cima
                    if g[0]<b[0]:
                        if b[0]+2 == state.rows: #Deadlock px à parede externa
                            hMaxSize = True
                        elif abs(g[1]-b[1]) == 0: # Movimento em linha reta
                            if state.row <= b[0]: #Agente do lado oposto
                                movements += 2
                            for a,v in enumerate(state.map[b[1]]): #Objeto no caminho
                                if a > g[0] and a < b[0] and v in [BOX, BOX_ON_GOAL, WALL, DEADLOCK, DEADLOCK_BOX_ON_GOAL]:
                                    movements += 2
                                    break
                        else: #Movimento em duas direções
                            movements += 1
                            if state.row <= b[0]: #Agente do lado oposto
                                if (g[1] < b[1] and state.col <= b[1]) or (g[1] > b[1] and state.col >= b[1]):
                                    #+2 caso esteja dentro da área
                                    movements += 1

                if hMaxSize:
                    sol = (b, g, sys.maxsize)
                else:
                    sol = (b, g, self.manDistance(b,g) + movements)
                solution.append(sol)
            solutions.append(solution)

        #print("------ Player:", state.row, state.col)
        #print("------ Solutions:")
        #for sol in solutions:
        #    print(sol)
        #print("------")

        # selecina a melhor (qualquer combinação com o menor h).
        if solutions:
            best = sys.maxsize
            for s in solutions[0]:
                usedGoal = []
                usedBlock = []
                solution = []

                usedGoal.append(s[1])
                usedBlock.append(s[0])
                solution.append(s)
                h = s[2]
                for lin in solutions:
                    for col in lin:
                        if col[1] not in usedGoal and col[0] not in usedBlock:
                            solution.append(col)
                            usedGoal.append(col[1])
                            usedBlock.append(col[0])
                            if col[2] != sys.maxsize:
                                h = h + col[2]
                            else:
                                h = sys.maxsize
                            break
                if h < best:
                    best = h
                    result = solution

            #print("------- Result:")
            #if 'result' in locals():
            #    print(result)
            #print("goal distance: ",best)
            #print("-------")

            #Distância do Agente para a caixa mais próxima
            if best < sys.maxsize:
                w = state.getPlayer()
                d = sys.maxsize
                v = (-1,-1)
                distBoxes = 0
                for x in state.getUnplacedBoxes():
                    if self.manDistance(w, x) < d:
                        d = self.manDistance(w, x) -1
                        v = x
                    boxDist = []
                    for u in state.getUnplacedBoxes():
                        if x != u:
                            boxDist.append(self.manDistance(x, u))
                    if boxDist:
                        distBoxes += min(boxDist)
                if v is not (-1,-1):
                    best = best + d + distBoxes
            #        print("agent Distance: ", d)
            #        print("boxes Distance: ", distBoxes)
        else:
            best = 0

        #print("----------------------------------------- final heuristic:", best)
        return best

    def cheapestFirstSearch(self, searchType):
        """Realiza busca com a estratégia de custo uniforme, A* ou Gulosa conforme escolha realizada na chamada.
        @param searchType: 0=custo uniforme (Ótima), 1=A* com heurística hn1 (Ótima); 2=Gulosa com hn2
        @return plano encontrado"""
        # @TODO: Implementação do aluno
        # Atributos para análise de desempenho
        treeNodesCt = 0 # contador de nós gerados incluídos na árvore
        # nós inseridos na árvore, mas que não necessitariam porque o estado 
        # já foi explorado ou por já estar na fronteira
        exploredDicardedNodesCt = 0
        frontierDiscardedNodesCt = 0

        # Algoritmo de busca
        solution = None
        root = TreeNode(parent=None)
        root.state = self.prob.initialState
        root.gn = 0
        root.hn = 0
        root.action = -1 
        treeNodesCt += 1
        costbound = sys.maxsize

        # cria FRONTEIRA com estado inicial
        frontier = dict()
        frontier[root.state.dictKey] = root

        # cria EXPLORADOS - inicialmente vazia
        explored = dict()

        print("\n*****\n***** INICIALIZAÇÃO ÁRVORE DE BUSCA\n*****\n")
        print("\n{0:<30}{1}".format("Nós na árvore: ",treeNodesCt))
        print("{0:<30}{1}".format("Descartados já na fronteira: ",frontierDiscardedNodesCt))
        print("{0:<30}{1}".format("Descartados já explorados: ",exploredDicardedNodesCt))
        print("{0:<30}{1}".format("Total de nós gerados: ",treeNodesCt + frontierDiscardedNodesCt + exploredDicardedNodesCt))

        while len(frontier): # Fronteira não vazia
            print("\n*****\n***** Início iteração\n*****\n")
            printFrontier(frontier)

            selNode = frontier.pop(min(frontier.keys(), key=(lambda k: frontier[k].getFn(searchType)))) # retira nó com menor F(n) da fronteira
            selState = selNode.state
            #print("Selecionado para expansão: {}\n".format(selNode))

            explored[selState.dictKey] = [selState.row, selState.col]
            printExplored(explored)

            # Teste de objetivo
            if selState.isSolution():
                solution = selNode
                break

            # Obtem ações possíveis para o estado selecionado para expansão
            actions = self.prob.possibleActionsWithoutCollaterals(selState) # actions é do tipo [-1, -1, -1, 1, 1, -1, -1, -1]
            
            for actionIndex, act in enumerate(actions):
                if(act < 0): # Ação não é possível
                    continue

                # INSERE NÓ FILHO NA ÁRVORE DE BUSCA - SEMPRE INSERE, DEPOIS
                # VERIFICA SE O INCLUI NA FRONTEIRA OU NÃO
                # Instancia o filho ligando-o ao nó selecionado (nSel)  
                child = selNode.addChild()
                # Obtem o estado sucessor pela execução da ação <act>
                sucState = self.prob.suc(selState, actionIndex)
                child.state = sucState
                # Custo g(n): custo acumulado da raiz até o nó filho
                gnChild = selNode.gn + self.prob.getActionCost(actionIndex)
                if searchType == UNIFORME_COST:
                    child.setGnHn(gnChild, 0) # Deixa h(n) zerada porque é busca de custo uniforme
                elif searchType == A_STAR and hn == 1:
                    child.setGnHn(gnChild, self.hn1(sucState) )
                elif searchType == A_STAR and hn == 2:
                    child.setGnHn(gnChild, self.hn2(sucState) )
                elif searchType == GREEDY and hn == 1:
                    child.setGnHn(gnChild, self.hn1(sucState) )
                elif searchType == GREEDY and hn == 2:
                    child.setGnHn(gnChild, self.hn2(sucState) )

                #teste de consistência para A*
                #if child.getFn(searchType) < selNode.getFn(searchType):
                #    print(">> INCONSISTENTE")

                child.action = actionIndex
                # INSERE NÓ FILHO NA FRONTEIRA (SE SATISFAZ CONDIÇÕES)

                # Testa se estado do nó filho foi explorado
                alreadyExplored = False
                if child.state.dictKey in explored:
                    alreadyExplored = True

                # Testa se estado do nó filho está na fronteira, caso esteja
                # guarda o nó existente em nFront
                nodeFront = None
                if not alreadyExplored:
                    if child.state.dictKey in frontier:
                        nodeFront = frontier.get(child.state.dictKey)
                # Se ainda não foi explorado
                if not alreadyExplored:
                    # e não está na fronteira, adiciona à fronteira
                    if nodeFront == None:
                        frontier[child.state.dictKey] = child
                        # Como a fronteira é um dicionário agora, não é feito ordenação. O objeto com menor F(n) é selecionado.
                        treeNodesCt += 1
                    else:
                        # Se já está na fronteira temos que ver se é melhor
                        if nodeFront.getFn(searchType) > child.getFn(searchType):       # Nó da fronteira tem custo maior que o filho
                            del frontier[nodeFront.state.dictKey]   # Remove nó da fronteira (pior e deve ser substituído)
                            nodeFront.remove()                      # Retira-se da árvore 
                            frontier[child.state.dictKey] = child   # Adiciona filho que é melhor
                            # Como a fronteira é um dicionário agora, não é feito ordenação. O objeto com menor F(n) é selecionado.
                            # treeNodesCt não é incrementado por inclui o melhor e retira o pior
                        else:
                            # Conta como descartado porque o filho é pior que o nó da fronteira e foi descartado
                            frontierDiscardedNodesCt += 1
                else:
                    exploredDicardedNodesCt += 1
            
            print("\n{0:<30}{1}".format("Nós na árvore: ",treeNodesCt))
            print("{0:<30}{1}".format("Descartados já na fronteira: ",frontierDiscardedNodesCt))
            print("{0:<30}{1}".format("Descartados já explorados: ",exploredDicardedNodesCt))
            print("{0:<30}{1}".format("Total de nós gerados: ",treeNodesCt + frontierDiscardedNodesCt + exploredDicardedNodesCt))


        if(solution != None):
            print("!!! Solução encontrada !!!")
            print("!!! Custo:        {}".format(solution.gn))
            print("!!! Profundidade: {}\n".format(solution.depth))
            print("\n{0:<30}{1}".format("Nós na árvore: ",treeNodesCt))
            print("{0:<30}{1}".format("Descartados já na fronteira: ",frontierDiscardedNodesCt))
            print("{0:<30}{1}".format("Descartados já explorados: ",exploredDicardedNodesCt))
            print("{0:<30}{1}".format("Total de nós gerados: ",treeNodesCt + frontierDiscardedNodesCt + exploredDicardedNodesCt))
            return buildPlan(solution)
        else:
            print("### Solução NÃO encontrada ###")
            return None
