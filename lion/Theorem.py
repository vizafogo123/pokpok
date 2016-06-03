from lion.Formula import Formula
from lion.Operation import EXISTS, IN, EMPTY, FORALL, B, IF, C, EQUI, EQUALS, AND, D, PHI1, PHI2, F, E, G, OR, H, \
    operations, Operation
from lion.Operation import NOT, A


class Theorem:
    def __init__(self, formula, name):
        self.formula = formula
        self.cnf = self.formula.simplify().to_cnf()
        self.name = name
        self.rename_constructed_ops()

    def rename_constructed_ops(self):
        for op in self.cnf.list_of_ops():
            if op.is_constructed_op:
                op.name += " in " + self.name
                op.print_scheme = op.print_scheme[:1] + "_{{" + self.name + "}} " + op.print_scheme[1:]

    @staticmethod
    def list_of_ops(theorems):
        res = operations
        for theorem in theorems:
            for op in theorem.cnf.list_of_ops():
                if op not in res:
                    res.append(op)
        return res

    def is_theorem_scheme(self):
        return len(self.cnf.get_function_schemes()) > 0


AX_EMPT = Theorem(Formula([NOT, EXISTS, A, IN, A, EMPTY]), 'ax-empt')
AX_EXT = Theorem(Formula([FORALL, A, FORALL, B, EQUI, FORALL, C, EQUI, IN, C, A, IN, C, B, EQUALS, A, B]), 'ax-ext')
AX_REG = Theorem(Formula(
    [FORALL, A, IF, NOT, EQUALS, A, EMPTY, EXISTS, B, AND, IN, B, A, NOT, EXISTS, C, AND, IN, C, B, IN, C, A]),
    'ax-reg')
AX_UNI = Theorem(Formula([FORALL, A, EXISTS, B, FORALL, C, FORALL, D, IF, AND, IN, D, C, IN, C, A, IN, D, B]),
                 'ax-uni')
AX_SPEC = Theorem(Formula([FORALL, A, EXISTS, B, FORALL, C, EQUI, IN, C, B, AND, IN, C, A, PHI1, C]), 'ax-spec')
AX_REP = Theorem(Formula(
    [FORALL, A, IF, FORALL, B, IF, IN, B, A, EXISTS, C, PHI2, B, C, EXISTS, D, FORALL, E, IF, IN, E, A, EXISTS, F,
     AND, IN, F, D, PHI2, E, F]), 'ax-rep')
AX_INF = Theorem(Formula(
    [EXISTS, A, AND, IN, EMPTY, A, FORALL, B, IF, IN, B, A, EXISTS, C, AND, IN, C, A, FORALL, D, EQUI, IN, D, C, OR,
     EQUALS, D, B, IN, D, B]), 'ax-inf')
AX_CHO = Theorem(Formula(
    [FORALL, A, IF, AND, NOT, IN, EMPTY, A, FORALL, B, IF, IN, B, A, FORALL, C, IF, IN, C, A, NOT, EXISTS, D, AND,
     IN, D, B, IN, D, C, EXISTS, E, FORALL, F, IF, IN, F, A, EXISTS, G, AND, AND, IN, G, E, IN, G, F, FORALL, H, IF,
     AND, IN, H, E, IN, H, F, EQUALS, H, G]), 'ax-cho')
AX_POW = Theorem(Formula([FORALL, A, EXISTS, B, FORALL, C, IF, FORALL, D, IF, IN, D, C, IN, D, A, IN, C, B]), 'ax-pow')

axioms = [AX_EMPT, AX_EXT, AX_REG, AX_UNI, AX_SPEC, AX_REP, AX_POW, AX_INF, AX_CHO]

if __name__ == '__main__':
    print(len(Theorem.list_of_ops(axioms)))
    print([op.type for op in Theorem.list_of_ops(axioms)])
    print(AX_REP.is_theorem_scheme())
    print(AX_INF.cnf.to_latex())
