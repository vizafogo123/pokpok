
import pyjd # this is dummy in pyjs.
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.Button import Button
from pyjamas.ui.HTML import HTML
from pyjamas.ui.Label import Label
from pyjamas import Window
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui.Anchor import Anchor
from pyjamas.ui.Image import Image

from pokpok import Formula
import urllib




def greet(fred):
    global text_area
    fred.setText("No, really click me!")

    #Window.alert(text_area.getText())
    a3 = Image('http://latex.codecogs.com/gif.download?'+urllib.quote(text_area.getText()))
    RootPanel().add(a3)


if __name__ == '__main__':
    pyjd.setup("public/Hello.html?fred=foo#me")
    b = Button("Click me", greet, StyleName='teststyle')

    text_area = TextArea()
    text_area.setCharacterWidth(80)
    text_area.setVisibleLines(8)

    a3 = Image()
    RootPanel().add(a3)

    RootPanel().add(b)
    # RootPanel().add(h)
    # RootPanel().add(l)
    RootPanel().add(text_area)

    RootPanel().add(Image('http://latex.codecogs.com/gif.download?'+urllib.quote(Formula.AX_CHO.to_latex())))
    # RootPanel().add(base)
    pyjd.run()
