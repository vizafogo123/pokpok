from lion.Formula import Formula
from lion.NormalForm import NormalForm
from lion.Operation import base_operations, EQUALS, A
from lion.Theorem import Theorem, axioms, AX_EMPT


class ProofState:
    def __init__(self, theorems, operations=list(), cnf=None):
        self.operations = list(operations)
        self.theorems = list(theorems)
        if cnf:
            self.cnf = cnf.deepcopy()
        else:
            self.cnf = NormalForm([])

        for op in Theorem.list_of_ops(theorems):
            if op not in self.operations:
                self.operations.append(op)

    def add_theorem(self, theorem):
        self.theorems.append(theorem)
        for op in Theorem.list_of_ops([theorem]):
            if op not in self.operations:
                self.operations.append(op)

    def add_operation(self, op):
        self.operations.append(op)

    def deepcopy(self):
        return ProofState(self.theorems,self.operations,self.cnf)

    def add_literal_to_cnf(self,literal):
        self.cnf+=NormalForm([[literal]])


global_proof_state = ProofState(axioms, base_operations)


class ProofTreeItem:
    def __init__(self, proof_state, parent):
        self.proof_state = proof_state
        self.parent = parent
        self.children=[]
        self.is_closed=False

    @staticmethod
    def proof_root(formula):
        return ProofTreeItem(ProofState(global_proof_state.theorems+[Theorem(formula,'indirect')],cnf=None),parent=None)

    def split(self, literal):
        child1=ProofTreeItem(self.proof_state.deepcopy(),self)
        child1.proof_state.add_literal_to_cnf(literal)
        child2=ProofTreeItem(self.proof_state.deepcopy(),self)
        child2.proof_state.add_literal_to_cnf(literal.negate())
        self.children=[child1,child2]

    def close(self):
        self.is_closed=True
        if self.parent and len([x for x in self.parent.children if not x.is_closed])==0:
            self.parent.close()


if __name__ == '__main__':
    x=ProofTreeItem.proof_root(AX_EMPT.formula)
    x.split(Formula([EQUALS, A, A]))
    x.children[0].close()
    x.children[1].close()
    print(98)
