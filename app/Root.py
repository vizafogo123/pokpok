from pyjamas import Window
from pyjamas.ui.Button import Button
from pyjamas.ui.Image import Image
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.RootPanel import RootPanel

from app.FormulaBuilder import latex_to_url, FormulaBuilder
from lion.Formula import Formula
from lion.Operation import operations
from lion.Theorem import axioms


class Root():
    def __init__(self):
        self.current_theorem=None
        self.current_vars=[]

    def fill_combo_variable(self):
        self.combo_variable.clear()
        for var in self.current_vars:
            self.combo_variable.addItem(var.name)


    def select_theorem(self):
        self.current_theorem=axioms[self.combo_theorem.getSelectedIndex()]
        self.current_cnf=self.current_theorem.cnf.deepcopy()
        self.image_formula.setUrl(latex_to_url(self.current_theorem.formula.to_latex()))
        self.image_cnf.setUrl(latex_to_url(self.current_cnf.to_latex()))

        self.current_vars=self.current_cnf.get_vars()
        self.fill_combo_variable()

    def substitute_variable(self):
        var=self.current_vars[self.combo_variable.getSelectedIndex()]
        def after(formula):
            self.current_cnf=self.current_cnf.substitute(Formula([var]),formula)
            self.image_cnf.setUrl(latex_to_url(self.current_cnf.to_latex()))
            del self.current_vars[self.combo_variable.getSelectedIndex()]
            self.fill_combo_variable()

        a=FormulaBuilder(operations,after,type='expr')
        a.show()

    def start(self):
        button1 = Button("Click me", self.select_theorem, StyleName='teststyle')
        button2 = Button("Shari hao", self.substitute_variable, StyleName='teststyle')

        self.combo_theorem = ListBox(VisibleItemCount=1)
        for ax in axioms:
            self.combo_theorem.addItem(ax.name)

        self.combo_variable = ListBox(VisibleItemCount=1)
        self.image_formula = Image()
        self.image_cnf = Image()
        RootPanel().add(self.combo_theorem)
        RootPanel().add(button1)
        RootPanel().add(self.image_formula)
        RootPanel().add(self.image_cnf)
        RootPanel().add(self.combo_variable)
        RootPanel().add(button2)

