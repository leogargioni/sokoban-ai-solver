BOX = '$'
STORAGE = '.'
SPACE = ' '
WALL = '#'
BOX_ON_GOAL = '*'
DEADLOCK = 'x'
DEADLOCK_BOX_ON_GOAL = '%'

OBJECT = frozenset([WALL, BOX, BOX_ON_GOAL, DEADLOCK_BOX_ON_GOAL])

class State:
    """Representa um estado do problema."""

    def __init__(self, maxRows, maxColumns):
        self.map = [[SPACE for j in range(maxColumns)] for i in range(maxRows)]
        self.row = 0
        self.col = 0

        self.rows = maxRows
        self.cols = maxColumns

    def setDictKey(self):
        """ Cria uma string para identificar o estado a fim de ser usada como chave nos dicionários"""
        string = ""
        for y,a in enumerate(self.map):
            for x,b in enumerate(self.map[y]):
                if y == self.row and x == self.col:
                    string += "A"
                elif self.map[y][x] == DEADLOCK:
                    string += SPACE
                elif self.map[y][x] == DEADLOCK_BOX_ON_GOAL:
                    string += BOX_ON_GOAL
                else:
                    string += self.map[y][x]
        self.dictKey = string

    def getSomething(self, something):
        result = []
        y = 0
        for l in self.map:
            x = 0
            for i in l:
                if i == something:
                    result.append((y,x))
                x += 1
            y += 1

        return result

    def _getSeveralThings(self, somethings):
        total = []
        for thing in somethings:
            total.extend(self.getSomething(thing))
        return total

    def getUnplacedBoxes(self):
        return self.getSomething(BOX)

    def getDeadlocks(self):
        return self._getSeveralThings([DEADLOCK, DEADLOCK_BOX_ON_GOAL])

    def getAllGoals(self):
        return self._getSeveralThings([STORAGE, BOX_ON_GOAL, DEADLOCK_BOX_ON_GOAL])

    def getFreeGoals(self):
        return self.getSomething(STORAGE)

    def getBoxes(self):
        return self._getSeveralThings([BOX, BOX_ON_GOAL, DEADLOCK_BOX_ON_GOAL])

    def getPlayer(self):
        return (self.row, self.col)
    
    def isSolution(self):
        return (len(self.getUnplacedBoxes()) == 0)

    def staticDeadlock(self):

        def _place_deadlock(y,x,delta_y,delta_x):
            try:
                if self.map[y+delta_y][x] == WALL and \
                   self.map[y][x+delta_x] == WALL:
                    if self.map[y][x] == SPACE:
                        self.map[y][x] = DEADLOCK
                        return True
                    elif self.map[y][x] == BOX_ON_GOAL:
                        self.map[y][x] = DEADLOCK_BOX_ON_GOAL
                        return True
            except IndexError:
                pass
            return False

        # Place Deadlock Markers in corners (without goals)
        for y,a in enumerate(self.map):
            for x,b in enumerate(self.map[y]):
                if self.map[y][x] in [SPACE, BOX_ON_GOAL]:
                    _place_deadlock(y,x,-1,-1) or \
                    _place_deadlock(y,x,-1,1) or \
                    _place_deadlock(y,x,1,-1) or \
                    _place_deadlock(y,x,1,1)

        # Connect Deadlock Markers if they next to a contin. wall w/o goals
        def connect_markers(dy,dx, view):
            up = True
            down = True
            found = False
            x = dx

            while x > 1:
                x -= 1
                try:
                    if view.get((dy,x)) in [DEADLOCK, DEADLOCK_BOX_ON_GOAL]:
                        found = True
                        break
                    elif view.get((dy,x)) == STORAGE:
                        break
                except IndexError:
                    break

            if found:
                sx = x
                while x != dx:
                    x += 1
                    try:
                        if view.get((dy+1,x)) not in [WALL, BOX, BOX_ON_GOAL] and down:
                            down = False
                    except IndexError:
                        down = False
                    try:
                        if view.get((dy-1,x)) not in [WALL, BOX, BOX_ON_GOAL] and up:
                            up = False
                    except IndexError:
                        up = False
                    try:
                        if not view.get((dy,x)) in [SPACE, DEADLOCK, DEADLOCK_BOX_ON_GOAL]:
                            up = down = False
                    except IndexError:
                        down = up = False

                if up or down:
                    x = sx
                    while x != dx:
                        val = view.get((dy,x))
                        if val == SPACE:
                            view.set((dy,x), DEADLOCK)
                        x += 1

        yx_v = self.DirectView(self.map)
        xy_v = self.Swap_XY_View(yx_v)
        for dead in self.getDeadlocks():
            (dy,dx) = dead
            connect_markers(dy, dx, yx_v)
            connect_markers(dx, dy, xy_v)

    class DirectView:
        def __init__(self, map):
            self.map = map

        def get(self, y_x):
            y, x = y_x
            return self.map[y][x]

        def set(self, y_x, val):
            y, x = y_x
            self.map[y][x] = val
            return

        def y_len(self):
            return len(self.map)

        def x_len(self):
            return max([row.len for row in self.map])

    class Proxy_View:
        def __init__(self, v):
            self.v = v

        def _map(self, p):
            return p

        def get(self, p):
            return self.v.get(self._map(p))

        def set(self, p, val):
            return self.v.set(self._map(p), val)

        def y_len(self):
            return self.v.y_len()

        def x_len(self):
            return self.v.x_len()

    class Swap_XY_View(Proxy_View):
        def _map(self, y_x):
            y, x = y_x
            return (x,y)

        def y_len(self):
            return self.v.x_len()

        def x_len(self):
            return self.v.y_len()

    def __eq__(self, other):
        if self.row == other.row and self.col == other.col and self.map == other.map:
            return True
        else:
            return False

    def __str__(self): 
        # Permite fazer um print(state) diretamente
        return "({0:d}, {1:d})".format(self.row, self.col)