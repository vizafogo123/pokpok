from pyjamas import Window
from pyjamas.ui import HasHorizontalAlignment
from pyjamas.ui.Button import Button
from pyjamas.ui.FlexTable import FlexTable
from pyjamas.ui.Grid import Grid
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
        RootPanel().add(button0)
        RootPanel().add(outer)

        self.TheoremApplier=TheoremApplier(axioms)
        RootPanel().add(self.TheoremApplier)

