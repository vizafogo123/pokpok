from lion.Formula import Formula
from lion.Operation import Operation


class Theorem:
    axioms = []

    def __init__(self, formula, name, operations=list()):
        self.formula = formula
        self.name = name
        self.operations = operations

    def to_json(self):
        return {"name": self.name, "formula": self.formula.to_json(),
                "spec_ops": [op.to_json() for op in self.operations],
                "var_print_schemes": self.get_var_print_schemes()}

    def get_var_print_schemes(self):
        res = dict()
        for op in self.formula.body:
            if op.type == Operation.VARIABLE and op.id not in res:
                res[op.id] = op.print_scheme
        return res

    @staticmethod
    def from_dict(dic):
        vars = [Operation(k, 0, dic["var_print_schemes"][k], k, Operation.VARIABLE) for k in dic["var_print_schemes"]]
        spec_ops = [Operation.from_dict(k) for k in dic["spec_ops"]]
        return Theorem(Formula.from_list(dic["formula"],Operation.get_globals() + vars + spec_ops),
                       dic["name"], operations=spec_ops)

# PHI1 = Operation("op1", 1, "\phi \left( {} \\right)", "phi1", Operation.RELATION)
# PHI2 = Operation("op1", 2, "\phi \left( {} , {} \\right)", "phi2", Operation.RELATION)
# PHI3 = Operation("op1", 2, "\kappa \left( {} , {} \\right)", "kappa", Operation.EXPRESSION)

# AX_EMPT = Theorem(Formula([NOT, EXISTS, A, IN, A, EMPTY]), 'ax_empt')
# AX_EXT = Theorem(Formula([FORALL, A, FORALL, B, IF, FORALL, C, EQUI, IN, C, A, IN, C, B, EQUALS, A, B]), 'ax_ext')
# AX_REG = Theorem(Formula(
#     [FORALL, A, IF, NOT, EQUALS, A, EMPTY, EXISTS, B, AND, IN, B, A, NOT, EXISTS, C, AND, IN, C, B, IN, C, A]),
#     'ax_reg')
# AX_UNI = Theorem(Formula([FORALL, A, EXISTS, B, FORALL, C, FORALL, D, IF, AND, IN, D, C, IN, C, A, IN, D, B]), 'ax_uni')
# AX_SPEC = Theorem(Formula([FORALL, A, EXISTS, B, FORALL, C, EQUI, IN, C, B, AND, IN, C, A, PHI1, C]), 'ax_spec',
#                   operations=[PHI1])
# AX_REP = Theorem(Formula(
#     [FORALL, A, IF, FORALL, B, IF, IN, B, A, EXISTS, C, PHI2, B, C, EXISTS, D, FORALL, E, IF, IN, E, A, EXISTS, F,
#      AND, IN, F, D, PHI2, E, F]), 'ax_rep', operations=[PHI2])
# AX_INF = Theorem(Formula(
#     [EXISTS, A, AND, IN, EMPTY, A, FORALL, B, IF, IN, B, A, EXISTS, C, AND, IN, C, A, FORALL, D, EQUI, IN, D, C, OR,
#      EQUALS, D, B, IN, D, B]), 'ax_inf')
# AX_CHO = Theorem(Formula(
#     [FORALL, A, IF, AND, NOT, IN, EMPTY, A, FORALL, B, IF, IN, B, A, FORALL, C, IF, IN, C, A, NOT, EXISTS, D, AND,
#      IN, D, B, IN, D, C, EXISTS, E, FORALL, F, IF, IN, F, A, UNIQUE, G, AND, IN, G, E, IN, G, F]), 'ax_cho')
#
# AX_DAJDAJ = Theorem(Formula([FORALL, A, FORALL, B, EQUALS, PHI3, A, B, PHI3, B, A]), 'ax_dajdaj', [PHI3])

# axioms = [AX_EMPT, AX_EXT, AX_REG, AX_UNI, AX_SPEC, AX_REP, AX_INF, AX_CHO, AX_DAJDAJ]


if __name__ == '__main__':
    asok = {"name": "ax_rep",
            "formula": [1, "var1", 4, 1, "var2", 4, 11, "var2", "var1", 2, "var3", "op1", "var2", "var3", 2, "var4", 1,
                        "var5", 4, 11, "var5", "var1", 2, "var6", 7, 11, "var6", "var4", "op1", "var5", "var6"],
            "spec_ops": [{"id": "op1", "name": "phi2", "valence": 2, "type": 3,
                          "print_scheme": "\\phi \\left( {} , {} \\right) "}],
            "var_print_schemes": {"var1": "a ", "var2": "b ", "var3": "c ", "var4": "d ", "var5": "e ", "var6": "f "}}
    print(Theorem.from_dict(asok).formula.to_latex())
    # for k in asok["var_print_schemes"]:
    #     print(k,asok["var_print_schemes"][k])
