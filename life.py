from ggame import CircleAsset, Color, LineStyle, Sprite
from ggame import App

red = Color(0xff0000, 1.0)
blue = Color(0x0000ff, 1.0)
black = Color(0,1.0)

CELLDIAMETER = 10
redcircle = CircleAsset(CELLDIAMETER/2, LineStyle(0, black), red)
bluecircle = CircleAsset(CELLDIAMETER/2, LineStyle(0, black), blue)

deadcells = []
livecells = {}
neighborsof = {}
killlist = []
birthlist = []

pfroml = lambda p: (p[0]*CELLDIAMETER, p[1]*CELLDIAMETER)
lfromp = lambda p: (p[0]//CELLDIAMETER, p[1]//CELLDIAMETER)
adjacentdelta = [(-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1)]
adjacentcoords = lambda pos, delta: [(pos[0]+x[0], pos[1]+x[1]) for x in delta]

def GetAdjacent(coords):
    # build a list of adjacentcoordinates
    try:
        neighbors = neighborsof[coords]
    except:
        # build a list of adjacent coordinates
        neighbors = adjacentcoords(coords, adjacentdelta)
        neighborsof[coords] = neighbors
    return neighbors
        

def NewCellAt(coords):
    if not coords in livecells:
        try:
            newcell = deadcells.pop()
        except:
            newcell = (Sprite(redcircle,(0,0)), Sprite(bluecircle,(0,0)))
        livecells[coords] = newcell
        newcell[0].visible = True
        newcell[1].visible = False
        newcell[0].position = newcell[1].position = pfroml(coords)

# return number of live neighbors and list of empty neighbors
def ScanCell(coords):
    neighbors = GetAdjacent(coords)
    count = 0
    empties = []
    for n in neighbors:
        if n in livecells:
            count = count + 1
        else:
            empties.append(n)
    return count, empties


def step():
    global killlist
    global birthlist

    if not running:
        return
    allempties = set()
    # scan living cells
    for p, val in livecells.items():
        # change reds to blue
        if val[0].visible:
            val[0].visible = False
            val[1].visible = True
        n, empties = ScanCell(p)
        if n > 3 or n < 2:
            killlist.append(p)
        allempties.update(empties)
    # scan all neighboring empty cells to find newbies
    for p in allempties:
        n, empties = ScanCell(p)
        if n == 3:
            birthlist.append(p)
    # process deaths
    for p in killlist:
        c = livecells.pop(p)
        c[0].visible = c[1].visible = False
        deadcells.append(c)
    # process births
    for p in birthlist:
        NewCellAt(p)
    
    # clean up
    killlist = []
    birthlist = []
        

def MakeAGlider(pos):
    deltas = [(0,0), (1,1), (2,1), (2,0), (2,-1)]
    for p in deltas:
        NewCellAt((pos[0]+p[0],pos[1]+p[1]))

for i in range(5):
    MakeAGlider((i*6, i*2))

mousedown = None
running = True

def MouseDown(event):
    global mousedown
    mousedown = True
    pos = lfromp((event.x, event.y))
    NewCellAt(pos)

def MouseUp(event):
    global mousedown
    mousedown = False

def MouseMove(event):
    if mousedown:
        pos = lfromp((event.x, event.y))
        NewCellAt(pos)
        
def Spacebar(event):
    print("space")
    if running:
        running = False
    else:
        running = True

App.listenMouseEvent('mousedown', MouseDown)
App.listenMouseEvent('mouseup', MouseUp)
App.listenMouseEvent('mousemove', MouseMove)
App.listenKeyEvent('keypress', 'space', Spacebar)

myapp = App()
myapp.run(step)