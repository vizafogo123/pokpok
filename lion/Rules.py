from app.FormulaBuilder import FormulaBuilder
from lion.Formula import Formula
from lion.Operation import FORALL, operations, Operation, EXISTS, AND, IF, OR, EQUI, A, B, NOT
from lion.Proof import ProofElement


def request_formula(operations, after, type):
    FormulaBuilder(operations, after, type).show()


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
        after(f)

    request_formula([op for op in operations if op.available and op.type == Operation.EXPRESSION], after1, type='exp')


gen.is_applicable = gen_is_applicable
gen.apply = gen_apply

exist = Rule("exist")


def exist_is_applicable(formulas):
    return check_number(formulas, 1) and formulas[0].body[0] == EXISTS


def exist_apply(formulas, after):
    const = Operation.get_new_expression(operations, 0)
    operations.append(const)
    f = formulas[0]
    f = Formula(f.body[2:]).substitute(Formula([f.body[1]]), Formula([const]))
    after(f)


exist.is_applicable = exist_is_applicable
exist.apply = exist_apply

and_first = Rule("and first")


def and_first_is_applicable(formulas):
    return check_number(formulas, 1) and formulas[0].body[0] == AND


def and_first_apply(formulas, after):
    after(Formula(formulas[0].body[1:formulas[0].start_of_child(0, 2)]))


and_first.is_applicable = and_first_is_applicable
and_first.apply = and_first_apply

and_second = Rule("and second")


def and_second_is_applicable(formulas):
    return check_number(formulas, 1) and formulas[0].body[0] == AND


def and_second_apply(formulas, after):
    after(Formula(formulas[0].body[formulas[0].start_of_child(0, 2):]))


and_second.is_applicable = and_second_is_applicable
and_second.apply = and_second_apply

split = Rule("split")


def split_is_applicable(formulas):
    return check_number(formulas, 1) and formulas[0].body[0] in [IF, OR]


def split_apply(formulas, after):
    if formulas[0].body[0] == IF:
        after(Formula(formulas[0].body[1:formulas[0].start_of_child(0, 2)]).negation(), type=ProofElement.SPLIT,
              second_formula=Formula(formulas[0].body[formulas[0].start_of_child(0, 2):]))
    else:
        after(Formula(formulas[0].body[1:formulas[0].start_of_child(0, 2)]), type=ProofElement.SPLIT,
              second_formula=Formula(formulas[0].body[formulas[0].start_of_child(0, 2):]))


split.is_applicable = split_is_applicable
split.apply = split_apply

contra = Rule("contradiction")


def contra_is_applicable(formulas):
    return check_number(formulas, 2) and formulas[0].is_negation_of(formulas[1])


def contra_apply(formulas, after):
    after(Formula([]), type=ProofElement.CONTRA)


contra.is_applicable = contra_is_applicable
contra.apply = contra_apply

assumption = Rule("assumption")


def assumption_is_applicable(formulas):
    return True


def assumption_apply(formulas, after):
    def after1(formula):
        after(formula, type=ProofElement.SPLIT, second_formula=formula.negation())
        # TODO:spoapok

    request_formula([op for op in operations if op.available], after1, type='rel')


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
    after(f)


deduction.is_applicable = deduction_is_applicable
deduction.apply = deduction_apply

Rules = [gen, exist, and_first, and_second, split, contra, assumption, deduction]

if __name__ == '__main__':
    fa = Formula([OR, A, B])
    g = Formula([B])


    def pok(p):
        print(p.dump())


    print(deduction_is_applicable([fa, g]))
    if deduction_is_applicable([fa, g]):
        deduction.apply([fa, g], pok)
