from lion.Operation import base_operations
from lion.Theorem import Theorem, axioms


class ProofState:
    def __init__(self, operations, theorems, cnf=None):
        self.operations = list(operations)
        self.theorems = list(theorems)
        if cnf:
            self.cnf=cnf.deepcopy()
        else:
            self.cnf=None

        for op in Theorem.list_of_ops(theorems):
            if op not in self.operations:
                self.operations.append(op)

    def add_theorem(self,theorem):
        self.theorems.append(theorem)
        for op in Theorem.list_of_ops([theorem]):
            if op not in self.operations:
                self.operations.append(op)

    def add_operation(self,op):
        self.operations.append(op)


global_proof_state = ProofState(base_operations, axioms)

if __name__=='__main__':
    for op in global_proof_state.operations:
        print(op.name)
