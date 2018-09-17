from ggame import CircleAsset, Color, LineStyle, Sprite
from ggame import App

red = Color(0xff0000, 1.0)
blue = Color(0xff0000, 1.0)
black = Color(0,1.0)

redcircle = CircleAsset(5, LineStyle(0, black), red)

Sprite(redcircle, (100,100))

myapp = App()
myapp.run()