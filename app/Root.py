from pyjamas import Window
from pyjamas.ui.Button import Button
from pyjamas.ui.FlexTable import FlexTable
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.RootPanel import RootPanel

from app.FormulaBuilder import FormulaBuilder
from app.TheoremApplier import TheoremApplier
from app.Utils import fill_flextable_with_cnf
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
        fill_flextable_with_cnf(self.cnf_table, self.cnf)

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

