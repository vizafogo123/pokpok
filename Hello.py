
import pyjd # this is dummy in pyjs.

from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.Button import Button
from pyjamas.ui.Image import Image

from pokpok.Theorem import axioms
import urllib

def latex_to_url(latex):
    return 'http://latex.codecogs.com/gif.download?' + urllib.quote(latex)



def greet(fred):
    global text_area

    #Window.alert(text_area.getText())

    f=axioms[combo.getSelectedIndex()]
    image_formula.setUrl(latex_to_url(f.formula.to_latex()))
    image_cnf.setUrl(latex_to_url(f.cnf.to_latex()))

if __name__ == '__main__':
    pyjd.setup("public/Hello.html?fred=foo#me")
    b = Button("Click me", greet, StyleName='teststyle')

    combo = ListBox(VisibleItemCount=1)
    for ax in axioms:
        combo.addItem(ax.name)

    image_formula = Image()
    image_cnf = Image()
    RootPanel().add(combo)
    RootPanel().add(b)
    RootPanel().add(image_formula)
    RootPanel().add(image_cnf)

    # RootPanel().add(Image('http://latex.codecogs.com/gif.download?'+urllib.quote(Formula.AX_CHO.to_latex())))
    # RootPanel().add(base)
    pyjd.run()
