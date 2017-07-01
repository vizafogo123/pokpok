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

        if "hidden" in kwargs:
            self.hidden = kwargs["hidden"]
        else:
            self.hidden = False

        self.predecessors=kwargs["predecessors"]
        self.rule_name=kwargs["rule_name"]
        if "additional_info" in kwargs:
            self.additional_info=kwargs["additional_info"]

class Proof:
    def __init__(self):
        self.body = []

    def add(self, formula, **kwargs):
        # Window.alert([self.list_index_to_proof_index(n) for n in kwargs["predecessors"]])
        f = formula.simplify()
        kwargs["predecessors"]=[self.list_index_to_proof_index(n) for n in kwargs["predecessors"]]
        self.body.append(
            ProofElement(f, **kwargs))

    def active_list(self):
        depths = [sum([x.type for x in self.body[:i + 1]]) for i in range(len(self.body))]  # TODO:sajp
        min_depths = [min(depths[i:]) for i in range(len(self.body))]
        return [(0 if not ((not pe.hidden) and pe.type <> ProofElement.CONTRA and (d <= m + pe.type)) else
                 (1 if pe.type == ProofElement.NORMAL or d <= m else 2))
                for pe, d, m in zip(self.body, depths, min_depths)]

    def get_formula_list(self):
        return [(pe.formula if a == 1 else pe.second_formula) for pe, a in zip(self.body, self.active_list()) if a <> 0]

    def list_index_to_proof_index(self, n):
        k = 0
        a = self.active_list()
        for i in range(len(self.body)):
            if a[i] <> 0:
                if k == n:
                    return i
                else:
                    k += 1
        return ""

    def hide_formulas(self, index_list):
        l = [proof.list_index_to_proof_index(i) for i in index_list]
        for i in l:
            proof.body[i].hidden = True

    def unhide_all(self):
        for pe in proof.body:
            pe.hidden = False


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
    print([proof.body[proof.list_index_to_proof_index(i)].formula.dump() for i in range(4)])
    print([proof.list_index_to_proof_index(i) for i in range(4)])
    print(proof.active_list())
