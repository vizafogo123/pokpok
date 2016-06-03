from pyjamas import Window
from pyjamas.ui.VerticalPanel import VerticalPanel

from app.FormulaBuilder import latex_to_url, FormulaBuilder
from pyjamas.ui.Button import Button
from pyjamas.ui.Image import Image
from pyjamas.ui.ListBox import ListBox

from lion.Formula import Formula
from lion.NormalForm import NormalForm
from lion.Operation import operations, Operation
from lion.Theorem import Theorem


class TheoremApplier(VerticalPanel):
    def __init__(self, theorems, after):
        VerticalPanel.__init__(self)
        self.theorems = list(theorems)
        self.after = after

        self.button1 = Button("Select theorem", self.select_theorem, StyleName='teststyle')
        self.button2 = Button("Substitute variable", self.substitute_button_click, StyleName='teststyle')
        self.button3 = Button("Add", self.add_button_click, StyleName='teststyle')

        self.combo_theorem = ListBox(VisibleItemCount=1)
        self.combo_variable = ListBox(VisibleItemCount=1)

        self.image_formula = Image()
        self.image_current_cnf = Image()
        self.image_cnf = Image()
        self.current_formula=None

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

    def fill_image_current_cnf(self):
        self.image_current_cnf.setUrl(latex_to_url(self.current_cnf.to_latex()))

    def fill_image_formula(self):
        self.image_formula.setUrl(latex_to_url(self.current_theorem.formula.to_latex()))


    def refresh_controls(self):
        self.fill_combo_variable()
        # self.fill_combo_theorem()
        self.fill_image_formula()
        self.fill_image_current_cnf()
        self.button3.setEnabled(len(self.current_vars) == 0)
        self.button2.setText(
            "Substitute variable" if not self.current_theorem.is_theorem_scheme() else "Substitute relation scheme")

    def select_theorem(self):
        self.current_theorem = self.theorems[self.combo_theorem.getSelectedIndex()]
        self.current_cnf = self.current_theorem.cnf.deepcopy()
        self.current_formula=self.current_theorem.formula.simplify()

        self.current_vars = (self.current_cnf.get_vars() if not self.current_theorem.is_theorem_scheme()
                                 else self.current_cnf.get_function_schemes())
        self.refresh_controls()


    def substitute_button_click(self):
        op = self.current_vars[self.combo_variable.getSelectedIndex()]
        if op.type==Operation.VARIABLE:
            self.substitute_variable(op)
        else:
            self.substitute_function_scheme(op)

        self.refresh_controls()

    def substitute_variable(self,var):
        def after(formula):
            self.current_cnf = self.current_cnf.substitute(Formula([var]), formula)
            del self.current_vars[self.combo_variable.getSelectedIndex()]
            self.refresh_controls()

        a = FormulaBuilder(
            [op for op in Theorem.list_of_ops(self.theorems) if op.available and op.type == Operation.EXPRESSION], after,
            type='expr')
        a.show()

    def substitute_function_scheme(self,fun):
        vars=[]
        for _ in range(fun.no_of_args):
            vars.append(Operation.get_new_variable(vars))

        def after(formula): #TODO: 1
            self.current_formula=self.current_formula.substitute_definition(Formula([fun]+vars), formula).simplify()
            self.current_cnf = self.current_formula.to_cnf()
            del self.current_vars[self.combo_variable.getSelectedIndex()]
            self.refresh_controls()

        a = FormulaBuilder(
            vars+[op for op in Theorem.list_of_ops(self.theorems) if op.available], after,
            type='rel')
        a.show()

    def add_theorem(self, theorem):
        self.theorems.append(theorem)
        self.fill_combo_theorem()

    def add_button_click(self):
        if not self.current_theorem.is_theorem_scheme():
            self.after(self.current_cnf)
        else:
            self.add_theorem(Theorem(self.current_formula,"oihjio"))
