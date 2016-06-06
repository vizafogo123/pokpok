from pyjamas import Window
from pyjamas.ui.Button import Button
from pyjamas.ui.FlexTable import FlexTable
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.RootPanel import RootPanel

from app.FormulaBuilder import FormulaBuilder
from app.TheoremApplier import TheoremApplier
from app.Utils import fill_flextable_with_cnf
from lion.NormalForm import NormalForm
from lion.Operation import base_operations
from lion.ProofState import global_proof_state, ProofState
from lion.Theorem import Theorem


class Root():
    def __init__(self):
        self.cnf_table = FlexTable(BorderWidth="1")
    def jnbhu(self):
        def after(formula):
            self.TheoremApplier.add_theorem(Theorem(formula, 'ind'))

        a = FormulaBuilder([op for op in base_operations if op.available], after, type='rel')
        a.show()

    def onReceivingCnf(self, cnf):
        self.proof_state.cnf += cnf
        self.refresh_cnf_table()
        if self.proof_state.cnf.is_degenerate():
            Window.alert("SADAT ABDEL")

    def refresh_cnf_table(self):
        fill_flextable_with_cnf(self.cnf_table, self.proof_state.cnf)

    def start(self):
        button0 = Button("Begin", self.jnbhu, StyleName='teststyle')

        self.proof_state = ProofState(operations=global_proof_state.operations, theorems=global_proof_state.theorems,
                                      cnf=NormalForm([]))

        self.TheoremApplier = TheoremApplier(self.proof_state, self.onReceivingCnf)

        h = HorizontalPanel()
        h.setWidth("100%")
        h.add(self.cnf_table)
        h.add(self.TheoremApplier)
        h.setCellWidth(self.cnf_table, "50%")

        RootPanel().add(button0)

        RootPanel().add(h)
