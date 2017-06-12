from lion.Formula import Formula
from lion.Operation import EXISTS, IN, EMPTY, FORALL, B, IF, C, EQUI, EQUALS, AND, D, PHI1, PHI2, F, E, G, OR, H, \
    operations
from lion.Operation import NOT, A


class Theorem:
    def __init__(self,formula,name):
        self.formula=formula
        self.name=name

    @staticmethod
    def list_of_ops(theorems):
        res=[]
        for theorem in theorems:
            for op in theorem.cnf.list_of_ops():
                if op not in res:
                    res.append(op)
        return res

AX_EMPT = Theorem(Formula([NOT, EXISTS, A, IN, A, EMPTY]),'ax_empt')
AX_EXT = Theorem(Formula([FORALL, A, FORALL, B, IF, FORALL, C, EQUI, IN, C, A, IN, C, B, EQUALS, A, B]),'ax_ext')
AX_REG = Theorem(Formula(
        [FORALL, A, IF, NOT, EQUALS, A, EMPTY, EXISTS, B, AND, IN, B, A, NOT, EXISTS, C, AND, IN, C, B, IN, C, A]),'ax_reg')
AX_UNI = Theorem(Formula([FORALL, A, EXISTS, B, FORALL, C, FORALL, D, IF, AND, IN, D, C, IN, C, A, IN, D, B]),'ax_uni')
AX_SPEC = Theorem(Formula([FORALL, A, EXISTS, B, FORALL, C, EQUI, IN, C, B, AND, IN, C, A, PHI1, C]),'ax_spec')
AX_REP = Theorem(Formula(
        [FORALL, A, IF, FORALL, B, IF, IN, B, A, EXISTS, C, PHI2, B, C, EXISTS, D, FORALL, E, IF, IN, E, A, EXISTS, F,
         AND, IN, F, D, PHI2, E, F]),'ax_rep')
AX_INF = Theorem(Formula(
        [EXISTS, A, AND, IN, EMPTY, A, FORALL, B, IF, IN, B, A, EXISTS, C, AND, IN, C, A, FORALL, D, EQUI, IN, D, C, OR,
         EQUALS, D, B, IN, D, B]),'ax_inf')
AX_CHO = Theorem(Formula(
        [FORALL, A, IF, AND, NOT, IN, EMPTY, A, FORALL, B, IF, IN, B, A, FORALL, C, IF, IN, C, A, NOT, EXISTS, D, AND,
         IN, D, B, IN, D, C, EXISTS, E, FORALL, F, IF, IN, F, A, EXISTS, G, AND, AND, IN, G, E, IN, G, F, FORALL, H, IF,
         AND, IN, H, E, IN, H, F, EQUALS, H, G]),'ax_cho')

axioms=[AX_EMPT,AX_EXT,AX_REG,AX_UNI,AX_SPEC,AX_REP,AX_INF,AX_CHO]

if __name__=='__main__':
    print(len(Theorem.list_of_ops(axioms)))
    print([op.type for op in Theorem.list_of_ops(axioms)])
