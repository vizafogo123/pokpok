class ProofElement:
    def __init__(self, formula):
        self.formula = formula


class Proof:
    def __init__(self):
        self.body = []

    def add(self, formula):
        self.body.append(ProofElement(formula.deepcopy()))

    def get_formula_list(self):
        return [x.formula for x in self.body]


proof = Proof()
