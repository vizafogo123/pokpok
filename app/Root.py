from pyjamas import Window
from pyjamas.ui import HasHorizontalAlignment
from pyjamas.ui.Button import Button
from pyjamas.ui.DockPanel import DockPanel
from pyjamas.ui.FlexTable import FlexTable
from pyjamas.ui.Grid import Grid
from pyjamas.ui.HTML import HTML
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Image import Image
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.RootPanel import RootPanel

from app.FormulaBuilder import latex_to_url, FormulaBuilder
from app.TheoremApplier import TheoremApplier
from lion.Formula import Formula
from lion.NormalForm import NormalForm
from lion.Operation import Operation, operations
from lion.Theorem import axioms, Theorem, AX_REG, AX_CHO


class Root():
    def __init__(self):
        pass

    def jnbhu(self):
        def after(formula):
            self.TheoremApplier.add_theorem(Theorem(formula, 'ind'))

        a = FormulaBuilder([op for op in operations if op.available], after, type='rel')
        a.show()


    def start(self):

        kop=AX_CHO.cnf.get_latex_vectors()
        outer = FlexTable(BorderWidth="1")

        for i in range(len(kop)):
            for j in range(len(kop[i])):
                outer.setWidget(i, j, Image(latex_to_url(kop[i][j])))

        button0 = Button("Begin", self.jnbhu, StyleName='teststyle')

        self.image=Image()
        self.cnf=NormalForm([])

        def after(cnf):
            self.cnf+=cnf
            self.image.setUrl(latex_to_url(self.cnf.to_latex()))
            if self.cnf.is_degenerate():
                Window.alert("SADAT ABDEL")

        self.TheoremApplier=TheoremApplier(axioms,after)


        h=HorizontalPanel()
        h.setWidth("100%")
        h.add(self.image)
        h.add(self.TheoremApplier)
        h.setCellWidth(self.image,"50%")

        RootPanel().add(button0)
        # RootPanel().add(outer)

        RootPanel().add(h)

