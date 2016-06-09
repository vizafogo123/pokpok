from pyjamas import Window
from pyjamas.ui.Button import Button
from pyjamas.ui.FlexTable import FlexTable
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.RootPanel import RootPanel

from app.FormulaBuilder import FormulaBuilder
from app.TheoremApplier import TheoremApplier
from app.Utils import fill_flextable_with_cnf
from lion.Formula import Formula
from lion.Operation import base_operations, FORALL, A, NOT, IN
from lion.ProofState import ProofState, ProofTreeItem


class Root():
    def __init__(self):
        self.cnf_table = FlexTable(BorderWidth="1")

    def start_proof(self):
        def after(formula):
            self.proof_root=ProofTreeItem.proof_root(formula=formula.negate())
            self.set_to_proof_tree_position(self.proof_root)

        # a = FormulaBuilder([op for op in base_operations if op.available], after, type='rel')
        # a.show()

        f=Formula([FORALL,A,NOT,IN,A,A])
        after(f)

    def split_proof(self):
        def after(formula):
            self.proof_tree_position.split(formula)
            self.set_to_proof_tree_position(self.proof_tree_position.children[0])

        a = FormulaBuilder([op for op in self.proof_tree_position.proof_state.operations if op.available], after, type='rel')
        a.show()

    def onReceivingCnf(self, cnf):
        self.proof_tree_position.proof_state.cnf += cnf
        self.refresh_cnf_table()
        if self.proof_tree_position.proof_state.cnf.is_degenerate():
            Window.alert("SADAT ABDEL")

    def refresh_cnf_table(self):
        fill_flextable_with_cnf(self.cnf_table, self.proof_tree_position.proof_state.cnf)

    def set_to_proof_tree_position(self,proof_tree_position):
        self.proof_tree_position = proof_tree_position
        self.TheoremApplier.set_defaults(self.proof_tree_position.proof_state)
        self.refresh_cnf_table()

    def start(self):
        button0 = Button("Begin", self.start_proof, StyleName='teststyle')
        button1 = Button("Split", self.split_proof, StyleName='teststyle')

        self.TheoremApplier = TheoremApplier(ProofState([]), self.onReceivingCnf)

        self.h = HorizontalPanel()
        self.h.setWidth("100%")
        self.h.add(self.cnf_table)
        self.h.add(self.TheoremApplier)
        self.h.setCellWidth(self.cnf_table, "50%")

        RootPanel().add(button0)
        RootPanel().add(button1)

        RootPanel().add(self.h)
