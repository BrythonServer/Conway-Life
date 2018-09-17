from ggame import CircleAsset, Color, LineStyle, Sprite
from ggame import App

redcircle = CircleAsset(5, LineStyle(0,0), Color(0xff0000, 1))

Sprite(redcircle, (100,100))

myapp = App()
myapp.run()