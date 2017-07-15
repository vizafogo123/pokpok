from pyjamas import Window

from lion.Formula import Formula
from lion.Operation import Operation, AND, EXISTS, OR, IF, FORALL
from lion.Theorem import Theorem


class ProofElement:
    NORMAL = 0
    SPLIT = 1
    CONTRA = -1

    def __init__(self, formula, **kwargs):
        self.formula = formula
        self.predecessors = kwargs["predecessors"]
        self.rule_name = kwargs["rule_name"]
        self.additional_info = (None if "additional_info" not in kwargs else kwargs["additional_info"])
        self.hidden = (False if "hidden" not in kwargs else kwargs["hidden"])
        self.second_formula = (None if "second_formula" not in kwargs else kwargs["second_formula"])
        self.type = (self.NORMAL if "type" not in kwargs else kwargs["type"])

    def to_json(self):
        res = {
            "formula": self.formula.to_json(),
            "rule_name": self.rule_name,
            "predecessors": self.predecessors
        }
        if self.additional_info is not None:
            res["additional_info"] = self.additional_info.to_json()
        if self.second_formula is not None:
            res["second_formula"] = self.second_formula.to_json()
        return res


class Proof:
    def __init__(self):
        self.body = []

    def add(self, formula, **kwargs):
        f = formula.simplify()
        self.body.append(
            ProofElement(f, **kwargs))

    def active_list(self):
        if len(self.body)==0:
            return []
        depths=[self.body[0].type]
        for i in range(len(self.body)-1):
            depths.append(depths[i]+self.body[i+1].type)

        min_depths = [depths[-1]]
        for i in reversed(range(len(self.body)-1)):
            min_depths=[min(min_depths[0],depths[i])]+min_depths

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
        l = [proof.list_index_to_proof_index(i) for i in index_list if i not in self.split_points()]
        for i in l:
            proof.body[i].hidden = True

    def unhide_all(self):
        for pe in proof.body:
            pe.hidden = False

    def get_operations(self):
        res = Operation.get_globals()
        for f in self.get_formula_list():
            for op in f.body:
                if op.type <> Operation.VARIABLE and op not in res:
                    res.append(op)
        return res

    def get_local_ops(self):
        res = list()
        for f in self.get_formula_list():
            for op in f.body:
                if op.type <> Operation.VARIABLE and op not in Operation.get_globals() and op not in res:
                    res.append(op)
        return res

    def apply_rule(self, rule, selected_indices, after):
        selected_formulas = [x for i, x in enumerate(proof.get_formula_list()) if i in selected_indices]
        selected_indices = [self.list_index_to_proof_index(n) for n in selected_indices]
        if not rule.is_applicable(selected_formulas):
            Window.alert(rule.name+selected_formulas[0].dump())
            return

        def after1(formula, **kwargs):
            if not "predecessors" in kwargs:
                kwargs["predecessors"] = selected_indices
            self.add(formula, **kwargs)
            after()

        rule.apply(selected_formulas, after1)

    def to_json(self):
        return {"proof": [pe.to_json() for pe in proof.body],
                "local_ops": ""  # "[op.to_json() for op in self.get_local_ops()]
                }

    def get_theorem_to_save(self, selected_indices):
        if len(selected_indices) != 1 or sum(pe.type for pe in self.body) != 0:
            Window.alert("kop")
            return None
        f = [x for i, x in enumerate(proof.get_formula_list()) if i in selected_indices][0]
        return Theorem(f, Theorem.get_new_id(), "")

    def split_points(self):
        x = [i for i, x in enumerate(self.active_list()) if x == 1 and proof.body[i].type == ProofElement.SPLIT]
        return [n for n in range(len(self.get_formula_list())) if self.list_index_to_proof_index(n) in x]

    def take_recommended_action(self, n, rules, after):
        def pok():
            pass

        k = self.get_formula_list()
        if k[n].body[0] == AND:
            self.apply_rule(rules["and_first"], [n], pok)
            self.apply_rule(rules["and_second"], [n], pok)
            self.hide_formulas([n])
            after()
        elif k[n].body[0] in [OR, IF]:
            self.apply_rule(rules["split"], [n], after)
        elif k[n].body[0] == EXISTS:
            self.apply_rule(rules["exists"], [n], pok)
            self.hide_formulas([n])
            after()
        elif k[n].body[0] == FORALL:
            self.apply_rule(rules["gen"], [n], after)
        else:
            return


proof = Proof()

if __name__ == "__main__":
    A = Operation("var1", 0, "a", "a", Operation.VARIABLE)
    B = Operation("var2", 0, "b", "b", Operation.VARIABLE)
    C = Operation("var3", 0, "c", "c", Operation.VARIABLE)
    f = Formula([A])
    for i in range(1):
        proof.add(f, predecessors=[1, 2], rule_name="opj")
        proof.add(f, second_formula=Formula([B]), type=ProofElement.SPLIT, skao=123, predecessors=[1, 2], rule_name="opj")
        proof.add(f, second_formula=Formula([C]), type=ProofElement.SPLIT, skao=123, predecessors=[1, 2], rule_name="opj")
        proof.add(f, predecessors=[1, 2], rule_name="opj")
        proof.add(Formula([]), type=ProofElement.CONTRA, predecessors=[1, 2], rule_name="opj")
        proof.add(f, second_formula=Formula([B]), type=ProofElement.SPLIT, skao=123, predecessors=[1, 2], rule_name="opj")
        proof.add(f, predecessors=[1, 2], rule_name="opj")
        proof.add(f, second_formula=Formula([C]), type=ProofElement.SPLIT, skao=123, predecessors=[1, 2],
                  rule_name="opj")
        proof.add(f, predecessors=[1, 2], rule_name="opj")
        proof.add(Formula([]), type=ProofElement.CONTRA, predecessors=[1, 2], rule_name="opj")

    # print([x.dump() for x in proof.get_formula_list()])
    # print([proof.body[proof.list_index_to_proof_index(i)].formula.dump() for i in range(4)])
    # print([proof.list_index_to_proof_index(i) for i in range(4)])
    # t=time.time()
    # print t
    print(proof.active_list())
    # print time.time()-t
