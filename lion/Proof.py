from lion.Formula import Formula
from lion.Operation import A, B, C


class ProofElement:
    NORMAL = 0
    SPLIT = 1
    CONTRA = -1

    def __init__(self, formula, **kwargs):
        self.formula = formula
        self.type = self.NORMAL
        if "type" in kwargs:
            self.type = kwargs["type"]

        if "second_formula" in kwargs:
            self.second_formula = kwargs["second_formula"]


class Proof:
    def __init__(self):
        self.body = []

    def add(self, formula, **kwargs):
        self.body.append(ProofElement(formula.deepcopy(), **kwargs))

    def get_formula_list(self):
        depths = [sum([x.type for x in self.body[:i + 1]]) for i in range(len(self.body))] # TODO:sajp
        min_depths = [min(depths[i:]) for i in range(len(self.body))]
        return [(pe.formula if pe.type == ProofElement.NORMAL or d <= m else pe.second_formula)
                for pe, d,m in zip(self.body, depths,min_depths)
                if pe.type <> ProofElement.CONTRA and (d <= m+pe.type)]


proof = Proof()

if __name__ == "__main__":
    f = Formula([A])
    proof.add(f)
    proof.add(f, second_formula=Formula([B]), type=ProofElement.SPLIT, skao=123)
    proof.add(f, second_formula=Formula([C]), type=ProofElement.SPLIT, skao=123)
    proof.add(f)
    proof.add(Formula([]), type=ProofElement.CONTRA)
    proof.add(f, second_formula=Formula([B]), type=ProofElement.SPLIT, skao=123)
    proof.add(f)
    proof.add(Formula([]), type=ProofElement.CONTRA)
    print([x.dump() for x in proof.get_formula_list()])
