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
        # Window.alert(kop)
        outer = FlexTable(BorderWidth="1")

        # outer.setWidget(0, 0, Image("rembrandt/LaMarcheNocturne.jpg"))
        # outer.getFlexCellFormatter().setColSpan(0, 0, 2)
        # outer.getFlexCellFormatter().setHorizontalAlignment(0, 0, HasHorizontalAlignment.ALIGN_CENTER)
        #
        # outer.setHTML(1, 0, "Look to the right...<br>That's a nested table component ->")
        # outer.getCellFormatter().setColSpan(1, 1, 2)

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


        # h=FlexTable()
        # h.setWidget(0,0,outer)
        # h.setWidget(0,1,self.TheoremApplier)
        h=HorizontalPanel()
        h.add(self.image)
        h.add(self.TheoremApplier)

        RootPanel().add(button0)
        # RootPanel().add(outer)

        RootPanel().add(h)

