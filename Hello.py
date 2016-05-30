
import pyjd # this is dummy in pyjs.
from pyjamas import Window

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

    f=axioms[combo_theorem.getSelectedIndex()]
    image_formula.setUrl(latex_to_url(f.formula.to_latex()))
    image_cnf.setUrl(latex_to_url(f.cnf.to_latex()))

    combo_variable.clear()
    for var in f.cnf.get_vars():
        combo_variable.addItem(var.name)

def sopa():
    pass


if __name__ == '__main__':
    pyjd.setup("public/Hello.html?fred=foo#me")
    button1 = Button("Click me", greet, StyleName='teststyle')
    button2 = Button("Shari hao", sopa, StyleName='teststyle')

    combo_theorem = ListBox(VisibleItemCount=1)
    for ax in axioms:
        combo_theorem.addItem(ax.name)

    combo_variable = ListBox(VisibleItemCount=1)
    image_formula = Image()
    image_cnf = Image()
    RootPanel().add(combo_theorem)
    RootPanel().add(button1)
    RootPanel().add(image_formula)
    RootPanel().add(image_cnf)
    RootPanel().add(combo_variable)
    RootPanel().add(button2)

    # RootPanel().add(Image('http://latex.codecogs.com/gif.download?'+urllib.quote(Formula.AX_CHO.to_latex())))
    # RootPanel().add(base)
    pyjd.run()
