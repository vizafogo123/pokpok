from pyjamas import Window
from pyjamas.ui.Button import Button
from pyjamas.ui.Image import Image
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.RootPanel import RootPanel

from app.FormulaBuilder import latex_to_url, FormulaBuilder
from lion.Formula import Formula
from lion.NormalForm import NormalForm
from lion.Operation import Operation, operations
from lion.Theorem import axioms, Theorem


class Root():
    def __init__(self):
        self.current_theorem=None
        self.current_vars=[]
        self.cnf=NormalForm([])
        self.theorems=axioms

    def fill_combo_variable(self):
        self.combo_variable.clear()
        for var in self.current_vars:
            self.combo_variable.addItem(var.name)

    def fill_combo_theorem(self):
        self.combo_theorem.clear()
        for theorem in self.theorems:
            self.combo_theorem.addItem(theorem.name)

    def select_theorem(self):
        self.current_theorem=self.theorems[self.combo_theorem.getSelectedIndex()]
        self.current_cnf=self.current_theorem.cnf.deepcopy()
        self.image_formula.setUrl(latex_to_url(self.current_theorem.formula.to_latex()))
        self.image_current_cnf.setUrl(latex_to_url(self.current_cnf.to_latex()))

        self.current_vars=self.current_cnf.get_vars()
        self.fill_combo_variable()

    def substitute_variable(self):
        var=self.current_vars[self.combo_variable.getSelectedIndex()]
        def after(formula):
            self.current_cnf=self.current_cnf.substitute(Formula([var]),formula)
            self.image_current_cnf.setUrl(latex_to_url(self.current_cnf.to_latex()))
            del self.current_vars[self.combo_variable.getSelectedIndex()]
            self.fill_combo_variable()

        a=FormulaBuilder([op for op in operations if op.available and op.type==Operation.EXPRESSION],after,type='expr')
        a.show()

    def add_to_cnf(self):
        self.cnf+=self.current_cnf
        self.image_cnf.setUrl(latex_to_url(self.cnf.to_latex()))
        if self.cnf.is_degenerate():
            Window.alert("SADAT ABDEL")

    def begin(self):
        def after(formula):
            self.theorems.append(Theorem(formula,'ind'))
            self.fill_combo_theorem()

        a=FormulaBuilder([op for op in operations if op.available],after,type='rel')
        a.show()


    def start(self):
        self.button0 = Button("Begin", self.begin, StyleName='teststyle')
        self.button1 = Button("Select theorem", self.select_theorem, StyleName='teststyle')
        self.button2 = Button("Substitute variable", self.substitute_variable, StyleName='teststyle')
        self.button3 = Button("Add", self.add_to_cnf, StyleName='teststyle')

        self.combo_theorem = ListBox(VisibleItemCount=1)
        self.fill_combo_theorem()

        self.combo_variable = ListBox(VisibleItemCount=1)
        self.image_formula = Image()
        self.image_current_cnf = Image()
        self.image_cnf = Image()

        RootPanel().add(self.button0)
        RootPanel().add(self.combo_theorem)
        RootPanel().add(self.button1)
        RootPanel().add(self.image_formula)
        RootPanel().add(self.combo_variable)
        RootPanel().add(self.button2)
        RootPanel().add(self.image_current_cnf)
        RootPanel().add(self.button3)
        RootPanel().add(self.image_cnf)

