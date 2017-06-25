from pyjamas import Window

from pyjamas.ui.CheckBox import CheckBox
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.ScrollPanel import ScrollPanel
from pyjamas.ui.SimplePanel import SimplePanel
from pyjamas.ui.VerticalPanel import VerticalPanel

from app.FormulaBuilder import latex_to_url
from pyjamas.ui.Image import Image

from lion.Theorem import axioms

class TheoremPanel(ScrollPanel):
    def __init__(self,after):
        ScrollPanel.__init__(self,Size=("630px", "500px"))
        # self.setAlwaysShowScrollBars(True)
        self.after=after
        self.pok=VerticalPanel()
        self.add(self.pok)

        def onClick(x):
            def poas(sender):
                self.after(x)
            return poas

        for ax in axioms:
            im = Image()
            im.addClickListener(onClick(ax.formula))
            im.setUrl(latex_to_url(ax.formula.to_latex()))
            self.pok.add(im)

