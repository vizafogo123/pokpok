from pyjamas import Window
from pyjamas.ui.Button import Button
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Image import Image
from pyjamas.ui.RootPanel import RootPanel

from app.FormulaBuilder import latex_to_url, FormulaBuilder
from app.FormulaListPanel import FormulaListPanel
from lion.Formula import Formula
from lion.Operation import operations, A
from lion.Proof import proof
from lion.Rules import gen, Rules
from lion.Theorem import AX_EXT


class Root():
    def __init__(self):
        pass

    def button0_click(self):
        def after(formula):
            self.fo = formula
            self.image.setUrl(latex_to_url(self.fo.to_latex()))

        FormulaBuilder([op for op in operations if op.available], after, type='rel').show()

    def button1_click(self):
        self.add_formula(self.fo)

    def selected_formulas(self):
        return [x for i, x in enumerate(proof.get_formula_list()) if i in self.FormulaListPanel.get_selected_indices()]

    def button_rule_click(self, rule):
        def pok():
            if not rule.is_applicable(self.selected_formulas()):
                Window.alert(rule.name)
                return
            rule.apply(self.selected_formulas(), self.add_formula)

        return pok

    def add_formula(self, formula, **kwargs):
        proof.add(formula)
        self.FormulaListPanel.reload(proof.get_formula_list())

    def start(self):

        button0 = Button("Begin", self.button0_click, StyleName='teststyle')
        button1 = Button("Topsa", self.button1_click, StyleName='teststyle')

        for r in Rules:
            RootPanel().add(Button(r.name, self.button_rule_click(r), StyleName='teststyle'))

        self.image = Image()
        self.FormulaListPanel = FormulaListPanel()
        self.fo = AX_EXT.formula

        h = HorizontalPanel()
        h.setWidth("100%")
        h.add(self.image)
        h.add(self.FormulaListPanel)
        h.setCellWidth(self.image, "50%")

        self.image.setUrl(latex_to_url(self.fo.to_latex()))

        RootPanel().add(button0)
        RootPanel().add(button1)
        # RootPanel().add(button2)
        RootPanel().add(self.image)
        # RootPanel().add(outer)

        RootPanel().add(h)
