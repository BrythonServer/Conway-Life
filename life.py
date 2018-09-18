from ggame import CircleAsset, Color, LineStyle, Sprite
from ggame import App

red = Color(0xff0000, 1.0)
blue = Color(0xff0000, 1.0)
black = Color(0,1.0)

CELLDIAMETER = 10


class Cell(Sprite):
    freereds = []
    freeblues = []
    reds = []
    blues = []
    redcircle = CircleAsset(CELLDIAMETER/2, LineStyle(0, black), red)
    bluecircle = CircleAsset(CELLDIAMETER/2, LineStule(0, black), blue)
    
    def __init__(self, logicalpos):
        super().__init__(self.getred(), 
            (logicalpos[0]*CELLDIAMETER, logicalpos[1]*CELLDIAMETER))
            
    def getred(self):
        if freereds

Sprite(redcircle, (100,100))

myapp = App()
myapp.run()