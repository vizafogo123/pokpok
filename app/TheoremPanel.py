from pyjamas import Window

from pyjamas.ui.ScrollPanel import ScrollPanel
from pyjamas.ui.VerticalPanel import VerticalPanel

from app.FormulaBuilder import latex_to_url
from pyjamas.ui.Image import Image

from lion.Formula import Formula
from lion.Operation import Operation
from lion.Proof import proof
from lion.Rules import request_formula
from lion.Theorem import axioms


class TheoremPanel(ScrollPanel):
    def __init__(self, after):
        ScrollPanel.__init__(self, Size=("630px", "500px"))
        self.after = after
        self.pok = VerticalPanel()
        self.add(self.pok)

        def onClick(theorem):
            def name(n):
                return "var" + str(n + 1)

            def print_scheme(n):
                return ["\\alpha", "\\beta", "\\gamma", "\\delta", "\\epsilon"][n]

            def poas(sender):
                if len(theorem.vars) == 1:
                    constants = [Operation("const" + str(i + 1), 0, print_scheme(i), name(i), Operation.EXPRESSION)
                                 for i in range(theorem.vars[0].no_of_args)]

                    def after1(f):
                        self.after(theorem.formula.substitute_definition(Formula([theorem.vars[0]] + constants), f),
                                   predecessors=[], rule_name="insert")
                    request_formula([op for op in proof.get_operations()] + constants,
                                    after1, type=('rel' if theorem.vars[0].type == Operation.RELATION else 'exp'))
                else:
                    self.after(theorem.formula, predecessors=[], rule_name="insert")

            return poas

        for ax in axioms:
            im = Image()
            im.addClickListener(onClick(ax))
            im.setUrl(latex_to_url(ax.formula.to_latex()))
            self.pok.add(im)
