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
        # self.image=Image()
        self.cnf=NormalForm([])
        self.cnf_table = FlexTable(BorderWidth="1")

    def jnbhu(self):
        def after(formula):
            self.TheoremApplier.add_theorem(Theorem(formula, 'ind'))

        a = FormulaBuilder([op for op in operations if op.available], after, type='rel')
        a.show()

    def onReceivingCnf(self,cnf):
        self.cnf += cnf
        # self.image.setUrl(latex_to_url(self.cnf.to_latex()))
        self.refresh_cnf_table()
        if self.cnf.is_degenerate():
            Window.alert("SADAT ABDEL")

    def refresh_cnf_table(self):
        self.cnf_table.clear()
        latex_vectors = self.cnf.get_latex_vectors()
        for i in range(len(latex_vectors)):
            for j in range(len(latex_vectors[i])):
                self.cnf_table.setWidget(i, j, Image(latex_to_url(latex_vectors[i][j])))

    def start(self):

        button0 = Button("Begin", self.jnbhu, StyleName='teststyle')

        self.TheoremApplier=TheoremApplier(axioms,self.onReceivingCnf)

        h=HorizontalPanel()
        h.setWidth("100%")
        h.add(self.cnf_table)
        h.add(self.TheoremApplier)
        h.setCellWidth(self.cnf_table,"50%")

        RootPanel().add(button0)
        # RootPanel().add(self.cnf_table)

        RootPanel().add(h)

