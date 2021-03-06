from app.FormulaBuilder import FormulaBuilder
from lion.Formula import Formula
from lion.Operation import FORALL, Operation, EXISTS, AND, IF, OR, EQUI
from lion.Proof import ProofElement, proof


def request_formula(operations, after, type):
    if type=='exp':
        FormulaBuilder([o for o in operations if o.type==Operation.EXPRESSION], after, type=type).show()
    else:
        FormulaBuilder(operations, after, type=type).show()


class Rule:
    def __init__(self, name):
        self.name = name

    def is_applicable(self, formulas):
        pass

    def apply(self, formulas, after):
        pass


gen = Rule("gen")


def check_number(formulas, n):
    if len(formulas) <> n:
        return False
    for f in formulas:
        if len(f.body) == 0:
            return False
    return True


def gen_is_applicable(formulas):
    return check_number(formulas, 1) and formulas[0].body[0] == FORALL


def gen_apply(formulas, after):
    def after1(formula):
        f = formulas[0]
        f = Formula(f.body[2:]).substitute(Formula([f.body[1]]), formula)
        after(f, rule_name=gen.name, additional_info=formula)

    request_formula([op for op in proof.get_operations() if op.type == Operation.EXPRESSION], after1, type='exp')


gen.is_applicable = gen_is_applicable
gen.apply = gen_apply

exist = Rule("exist")


def exist_is_applicable(formulas):
    return check_number(formulas, 1) and formulas[0].body[0] == EXISTS


def exist_apply(formulas, after):
    const = Operation.get_new_expression(proof.get_operations(), 0)
    f = formulas[0]
    f = Formula(f.body[2:]).substitute(Formula([f.body[1]]), Formula([const]))
    after(f, rule_name=exist.name, additional_info=const)


exist.is_applicable = exist_is_applicable
exist.apply = exist_apply

and_first = Rule("and first")


def and_first_is_applicable(formulas):
    return check_number(formulas, 1) and formulas[0].body[0] == AND


def and_first_apply(formulas, after):
    after(Formula(formulas[0].body[1:formulas[0].start_of_child(0, 2)]), rule_name=and_first.name)


and_first.is_applicable = and_first_is_applicable
and_first.apply = and_first_apply

and_second = Rule("and second")


def and_second_is_applicable(formulas):
    return check_number(formulas, 1) and formulas[0].body[0] == AND


def and_second_apply(formulas, after):
    after(Formula(formulas[0].body[formulas[0].start_of_child(0, 2):]), rule_name=and_second.name)


and_second.is_applicable = and_second_is_applicable
and_second.apply = and_second_apply

split = Rule("split")


def split_is_applicable(formulas):
    return check_number(formulas, 1) and formulas[0].body[0] in [IF, OR]


def split_apply(formulas, after):
    if formulas[0].body[0] == IF:
        after(Formula(formulas[0].body[1:formulas[0].start_of_child(0, 2)]).negation(), type=ProofElement.SPLIT,
              second_formula=Formula(formulas[0].body[formulas[0].start_of_child(0, 2):]).simplify(),
              rule_name=split.name)
    else:
        after(Formula(formulas[0].body[1:formulas[0].start_of_child(0, 2)]), type=ProofElement.SPLIT,
              second_formula=Formula(formulas[0].body[formulas[0].start_of_child(0, 2):]).simplify(),
              rule_name=split.name)


split.is_applicable = split_is_applicable
split.apply = split_apply

contra = Rule("contradiction")


def contra_is_applicable(formulas):
    return check_number(formulas, 2) and formulas[0].is_negation_of(formulas[1])


def contra_apply(formulas, after):
    after(Formula([]), type=ProofElement.CONTRA, rule_name=contra.name)


contra.is_applicable = contra_is_applicable
contra.apply = contra_apply

assumption = Rule("assumption")


def assumption_is_applicable(formulas):
    return True


def assumption_apply(formulas, after):
    def after1(formula):
        after(formula, type=ProofElement.SPLIT, second_formula=formula.negation().simplify(), predecessors=[],
              rule_name=assumption.name)
        # TODO:spoapok

    request_formula(proof.get_operations(), after1, type='rel')


assumption.is_applicable = assumption_is_applicable
assumption.apply = assumption_apply

deduction = Rule("deduction")


def deduction_is_applicable(formulas):
    if not check_number(formulas, 2):
        return False
    if len(formulas[0].body) > len(formulas[1].body):
        a = formulas[1]
        b = formulas[0]
    else:
        a = formulas[0]
        b = formulas[1]
    if b.body[0] not in [EQUI, OR, IF]:
        return False
    k = b.start_of_child(0, 2)
    if b.body[0] == EQUI:
        return a == Formula(b.body[1:k]) or \
               a.is_negation_of(Formula(b.body[1:k])) or \
               a == Formula(b.body[k:]) or \
               a.is_negation_of(Formula(b.body[k:]))
    if b.body[0] == OR:
        return a.is_negation_of(Formula(b.body[1:k])) or \
               a.is_negation_of(Formula(b.body[k:]))
    if b.body[0] == IF:
        return a == Formula(b.body[1:k]) or \
               a.is_negation_of(Formula(b.body[k:]))


def deduction_apply(formulas, after):
    if len(formulas[0].body) > len(formulas[1].body):
        a = formulas[1]
        b = formulas[0]
    else:
        a = formulas[0]
        b = formulas[1]
    k = b.start_of_child(0, 2)
    if b.body[0] == EQUI:
        if a == Formula(b.body[1:k]):
            f = Formula(b.body[k:])
        if a.is_negation_of(Formula(b.body[1:k])):
            f = Formula(b.body[k:]).negation()
        if a == Formula(b.body[k:]):
            f = Formula(b.body[1:k])
        if a.is_negation_of(Formula(b.body[k:])):
            f = Formula(b.body[1:k]).negation()
    if b.body[0] == OR:
        if a.is_negation_of(Formula(b.body[1:k])):
            f = Formula(b.body[k:])
        if a.is_negation_of(Formula(b.body[k:])):
            f = Formula(b.body[1:k])
    if b.body[0] == IF:
        if a == Formula(b.body[1:k]):
            f = Formula(b.body[k:])
        if a.is_negation_of(Formula(b.body[k:])):
            f = Formula(b.body[1:k]).negation()
    after(f, rule_name=deduction.name)


deduction.is_applicable = deduction_is_applicable
deduction.apply = deduction_apply

Rules = [gen, exist, and_first, and_second, split, contra, assumption, deduction]

if __name__ == '__main__':
    A = Operation("var1", 0, "a", "a", Operation.VARIABLE)
    B = Operation("var2", 0, "b", "b", Operation.VARIABLE)
    fa = Formula([OR, A, B])
    g = Formula([B])


    def pok(p):
        print(p.dump())


    print(deduction_is_applicable([fa, g]))
    if deduction_is_applicable([fa, g]):
        deduction.apply([fa, g], pok)
