from ggame import CircleAsset, Color, LineStyle, Sprite
from ggame import App
from time import time

red = Color(0xff0000, 1.0)
blue = Color(0x0000ff, 1.0)
black = Color(0,1.0)

CELLDIAMETER = 10


class Cell(object):
    freereds = []
    freeblues = []
    reds = []
    blues = []
    redcircle = CircleAsset(CELLDIAMETER/2, LineStyle(0, black), red)
    bluecircle = CircleAsset(CELLDIAMETER/2, LineStyle(0, black), blue)
    adjacentdelta = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
    adjacentcoords = lambda pos, delta: [(pos[0]+x[0], pos[1]+x[1]) for x in delta]
    alive = set()   # coordinate pairs for alive cells
    alivecells = [] # list of living Cell objects
    deadcells = []  # list of dead Cell objects
    celldict = {}   # use to look up a Cell if you know the coordinates
    
    def __init__(self, logicalpos):
        self.makenew(logicalpos)

    def _setphysicalposition(self, pos):
        self.cell.position = (pos[0]*CELLDIAMETER, pos[1]*CELLDIAMETER)
        
    def makenew(self, pos):
        self.pos = pos
        self.alive.add(self.pos)
        self.alivecells.append(self)
        if self.freereds:
            self.cell = self.freereds.pop()
            self.cell.visible = True
        else:
            self.cell = Sprite(self.redcircle, (0,0))
        self._setphysicalposition(pos)
        self.celldict[self.pos] = self
        self.reds.append(self.cell)
        self.age = 0
        

    def ageoneday(self):
        # convert from red to blue
        if self.age == 0:
            newcell = None
            if self.freeblues:
                newcell = self.freeblues.pop()
                newcell.visible = True
            else:
                newcell = Sprite(self.bluecircle, (0,0))

            # move a blue cell to the active list
            self.blues.append(newcell)
            self.cell.visible = False  
            # move the red cell to free list
            self.freereds.append(self.cell)
            self.reds.remove(self.cell)
            newcell.position = self.cell.position
            self.cell = newcell
            self.age = 1
            
    def die(self):
        # make invisible and move sprite to free list
        if self.age == 1:
            freelist = self.freeblues
            activelist = self.blues
        else:
            freelist = self.freereds
            activelist = self.reds
        self.cell.visible = False
        activelist.remove(self.cell)
        freelist.append(self.cell)
        self.alive.remove(self.pos)
        self.alivecells.remove(self)
        self.deadcells.append(self)

    @classmethod
    def neighbors(cls, pos):
        """
        Count living neighbors.
        """
        return sum([1 if x in cls.alive else 0 for 
            x in cls.adjacentcoords(pos, cls.adjacentdelta)])

    def openneighbors(self):
        """
        Get a list of open neighbor cells.
        """ 
        return filter(lambda x: x not in Cell.alive, Cell.adjacentcoords(self.pos, self.adjacentdelta))

    @classmethod
    def Initialize(cls):
        for c in cls.alive:
            c.visible = False
            
    @classmethod
    def NewCell(cls, pos):
        try:
            c = cls.deadcells.pop()
            c.makenew(pos)
            c.visible = True
        except IndexError:
            c = Cell(pos)
            
    @classmethod
    def KillCell(cls, pos):
        cell = cls.celldict.pop(pos)
        cell.die()

def step():
    print("!", time())
    todie = []
    empties = set()
    tobirth = []
    print("*", time())
    for c in Cell.alivecells:
        c.ageoneday()
        n = Cell.neighbors(c.pos)
        if n > 3 or n < 2:
            todie.append(c)
        empties.update(c.openneighbors())
    print(" ", time())
    for c in empties:
        if Cell.neighbors(c) == 3:
            tobirth.append(c)
    for c in todie:
        Cell.KillCell(c.pos)
    for pos in tobirth:
        Cell.NewCell(pos)
    #print(len(Cell.alivecells), len(Cell.deadcells))

def MakeAGlider(pos):
    deltas = [(0,0), (1,1), (2,1), (2,0), (2,-1)]
    for p in deltas:
        Cell.NewCell((pos[0]+p[0],pos[1]+p[1]) 

for i in range(10):
    MakeAGlider((i*6, i*2))

#for c in Cell.alivecells:
    #print(c.pos, c.adjacentdelta)
    #print(Cell.adjacentcoords(c.pos, c.adjacentdelta))
    #print(list(c.openneighbors()))
    #print(list(filter(lambda x: x not in Cell.alive, Cell.adjacentcoords(c.pos, c.adjacentdelta))))

myapp = App()
myapp.run(step)