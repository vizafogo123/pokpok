from pyjamas import Window
from pyjamas.ui.VerticalPanel import VerticalPanel

from app.FormulaBuilder import latex_to_url, FormulaBuilder
from pyjamas.ui.Button import Button
from pyjamas.ui.Image import Image
from pyjamas.ui.ListBox import ListBox

from lion.Formula import Formula
from lion.NormalForm import NormalForm
from lion.Operation import operations, Operation


class TheoremApplier(VerticalPanel):
    def __init__(self,theorems):
        VerticalPanel.__init__(self)
        self.theorems = theorems

        self.button1 = Button("Select theorem", self.select_theorem, StyleName='teststyle')
        self.button2 = Button("Substitute variable", self.substitute_variable, StyleName='teststyle')
        self.button3 = Button("Add", self.add_to_cnf, StyleName='teststyle')

        self.combo_theorem = ListBox(VisibleItemCount=1)
        self.combo_variable = ListBox(VisibleItemCount=1)

        self.image_formula = Image()
        self.image_current_cnf = Image()
        self.image_cnf = Image()

        self.add(self.combo_theorem)
        self.add(self.button1)
        self.add(self.image_formula)
        self.add(self.combo_variable)
        self.add(self.button2)
        self.add(self.image_current_cnf)
        self.add(self.button3)
        self.add(self.image_cnf)

        self.set_defaults()

    def set_defaults(self):
        self.current_theorem = None
        self.current_vars = []
        self.cnf = NormalForm([])
        self.fill_combo_theorem()
        # self.fill_combo_variable()


    def fill_combo_variable(self):
        self.combo_variable.clear()
        for var in self.current_vars:
            self.combo_variable.addItem(var.name)

    def fill_combo_theorem(self):
        self.combo_theorem.clear()
        for theorem in self.theorems:
            self.combo_theorem.addItem(theorem.name)

    def select_theorem(self):
        self.current_theorem = self.theorems[self.combo_theorem.getSelectedIndex()]
        self.current_cnf = self.current_theorem.cnf.deepcopy()
        self.image_formula.setUrl(latex_to_url(self.current_theorem.formula.to_latex()))
        self.image_current_cnf.setUrl(latex_to_url(self.current_cnf.to_latex()))

        self.current_vars = self.current_cnf.get_vars()
        self.fill_combo_variable()

    def substitute_variable(self):
        var = self.current_vars[self.combo_variable.getSelectedIndex()]

        def after(formula):
            self.current_cnf = self.current_cnf.substitute(Formula([var]), formula)
            self.image_current_cnf.setUrl(latex_to_url(self.current_cnf.to_latex()))
            del self.current_vars[self.combo_variable.getSelectedIndex()]
            self.fill_combo_variable()

        a = FormulaBuilder([op for op in operations if op.available and op.type == Operation.EXPRESSION], after,
                           type='expr')
        a.show()

    def add_to_cnf(self):
        self.cnf += self.current_cnf
        self.image_cnf.setUrl(latex_to_url(self.cnf.to_latex()))
        if self.cnf.is_degenerate():
            Window.alert("SADAT ABDEL")

    def add_theorem(self,theorem):
        self.theorems.append(theorem)
        self.fill_combo_theorem()
