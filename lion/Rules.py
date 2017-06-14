from pyjamas import Window

from app.FormulaBuilder import FormulaBuilder
from lion.Formula import Formula
from lion.Operation import FORALL, operations, Operation, EXISTS, AND, IF, OR
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


def gen_is_applicable(formulas):
    if len(formulas) <> 1:
        return False
    if len(formulas[0].body) == 0:
        return False
    return formulas[0].body[0] == FORALL


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
    if len(formulas) <> 1:
        return False
    if len(formulas[0].body) == 0:
        return False
    return formulas[0].body[0] == EXISTS


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
    if len(formulas) <> 1:
        return False
    if len(formulas[0].body) == 0:
        return False
    return formulas[0].body[0] == AND


def and_first_apply(formulas, after):
    after(Formula(formulas[0].body[1:formulas[0].start_of_child(0, 2)]))


and_first.is_applicable = and_first_is_applicable
and_first.apply = and_first_apply

and_second = Rule("and second")


def and_second_is_applicable(formulas):
    if len(formulas) <> 1:
        return False
    if len(formulas[0].body) == 0:
        return False
    return formulas[0].body[0] == AND


def and_second_apply(formulas, after):
    after(Formula(formulas[0].body[formulas[0].start_of_child(0, 2):]))


and_second.is_applicable = and_second_is_applicable
and_second.apply = and_second_apply

split = Rule("split")


def split_is_applicable(formulas):
    if len(formulas) <> 1:
        return False
    if len(formulas[0].body) == 0:
        return False
    return formulas[0].body[0] in [IF,OR]


def split_apply(formulas, after):
    if formulas[0].body[0]==IF:
        after(Formula(formulas[0].body[1:formulas[0].start_of_child(0, 2)]).negate(),type=ProofElement.SPLIT,
              second_formula=Formula(formulas[0].body[formulas[0].start_of_child(0, 2):]))
    else:
        after(Formula(formulas[0].body[1:formulas[0].start_of_child(0, 2)]),type=ProofElement.SPLIT,
              second_formula=Formula(formulas[0].body[formulas[0].start_of_child(0, 2):]))


split.is_applicable = split_is_applicable
split.apply = split_apply


Rules = [gen, exist, and_first, and_second,split]

