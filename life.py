from ggame import CircleAsset, Color, LineStyle, Sprite
from ggame import App

red = Color(0xff0000, 1.0)
blue = Color(0xff0000, 1.0)
black = Color(0,1.0)

CELLDIAMETER = 10


class Cell(object):
    freereds = []
    freeblues = []
    reds = []
    blues = []
    redcircle = CircleAsset(CELLDIAMETER/2, LineStyle(0, black), red)
    bluecircle = CircleAsset(CELLDIAMETER/2, LineStyle(0, black), blue)
    adjacentdelta = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,-1), (1,1)]
    adjcentcoords = lambda pos, delta: [pos[0]+x[0], pos[1]+x[1]) for x in delta]
    alive = set()
    alivecells = []
    deadcells = []    
    
    def __init__(self, logicalpos):
        self.pos = logicalpos
        self.makenew()
        self.alive.add(self.pos)
        self.alivecells.append(self)
        self._setphysicalposition(logicalpos)

    def _setphysicalposition(self, pos):
        self.cell.position = (pos[0]*CELLDIAMETER, pos[1]*CELLDIAMETER)
        
    def makenew(self):
        if self.reds:
            self.cell = self.freereds.pop()
            self.cell.visible = True
        else:
            self.cell = Sprite(self.redcircle, (0,0))
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
            # move a blue cell to the actie list
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
        
    def neighbors(self):
        """
        Count living neighbors.
        """
        adjacentcounts = [1 if x in self.alive else 0 for 
            x in self.adjacentcoords(self.pos, self.adjacentdelta)]
        return sum(adjacentcounts)

    def openneighbors(self):
        """
        Get a list of open neighbor cells.
        """ 
        return filter(lambda x: x, [False if x in self.alive else x for 
            x in self.adjacentcoords(self.pos, self.adjacentdelta)])

    @classmethod
    def Initialize(cls):
        for c in cls.alive:
            c.visible = False
            
    @classmethod
    def NewCell(cls, pos):
        try:
            c = cls.deadcells.pop()
            c._setphysicalposition(pos)
            c.makenew()
            c.visible = True
        except IndexError:
            c = Cell(pos)

def step():
    print("step!")
    
Cell.NewCell(0,1)
Cell.NewCell(0,0)
Cell.NewCell(0,2)

myapp = App()
myapp.run()