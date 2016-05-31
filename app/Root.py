from pyjamas.ui.Button import Button
from pyjamas.ui.Image import Image
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.RootPanel import RootPanel

from app.FormulaBuilder import latex_to_url, FormulaBuilder
from lion.Operation import operations
from lion.Theorem import axioms


class Root():
    def select_theorem(self):
        f=axioms[self.combo_theorem.getSelectedIndex()]
        self.image_formula.setUrl(latex_to_url(f.formula.to_latex()))
        self.image_cnf.setUrl(latex_to_url(f.cnf.to_latex()))

        self.combo_variable.clear()
        for var in f.cnf.get_vars():
            self.combo_variable.addItem(var.name)

    def substitute_variable(self):
        a=FormulaBuilder(operations,lambda x:0)
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

