from os.path import dirname, abspath, join
import sys
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, 'pkg'))
sys.path.append(CODE_DIR)
from model import Model
from agent import Agent
import time


def buildgame(model):
    model.game.putVerticalWall(0,7,0)
    model.game.putVerticalWall(0,7,7)
    model.game.putHorizontalWall(0,7,0)
    model.game.putHorizontalWall(0,7,7)

    model.game.putVerticalWall(3,5,4)
    model.game.putHorizontalWall(1,2,3)


def main():
    # Cria o ambiente (modelo) = Labirinto com suas paredes
    Rows = 8
    Columns = 8
    model = Model(Rows, Columns)
    buildgame(model)

    # Define a posição inicial das caixas no ambiente - corresponde ao estado inicial
    model.game.setBoxPos(2,2)
    model.game.setBoxPos(2,4)
    model.game.setBoxPos(3,3)
    model.game.setBoxPos(4,5)
    model.game.setBoxPos(5,2)
    model.game.setBoxPos(5,3)


    # Define a posição inicial dos objetivos no ambiente - corresponde ao estado inicial
    model.game.setStoragePos(6,1)
    model.game.setStoragePos(6,2)
    model.game.setStoragePos(6,3)
    model.game.setStoragePos(6,4)
    model.game.setStoragePos(6,5)
    model.game.setStoragePos(6,6)

    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    model.setAgentPos(4,1)

    # Cria um agente
    agent = Agent(model)

    model.draw()
    print("\n Início do ciclo de raciocínio do agente \n")
    start_time = time.time()
    while agent.deliberate() != -1:
        model.draw()
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
