from pyjamas import Window
from pyjamas.ui.Button import Button
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Image import Image
from pyjamas.ui.RootPanel import RootPanel

from app.FormulaBuilder import latex_to_url
from app.FormulaList import FormulaList
from app.Rules import gen
from lion.Theorem import AX_EXT


class Root():
    def __init__(self):
        pass

    def button0_click(self):
        pass

    def button1_click(self):
        self.add_formula(self.fo)

    def selected_formulas(self):
        return [x for i,x in enumerate(self.list) if i in self.FormulaList.get_selected_indices()]

    def button2_click(self):
        if not gen.is_applicable(self.selected_formulas()):
            Window.alert(self.selected_formulas())
            return
        gen.apply(self.selected_formulas(), self.add_formula)

    def add_formula(self, formula):
        self.FormulaList.add_formula(formula)
        self.list.append(formula.deepcopy())

    def start(self):

        button0 = Button("Begin", self.button0_click, StyleName='teststyle')
        button1 = Button("Topsa", self.button1_click, StyleName='teststyle')
        button2 = Button("gen", self.button2_click, StyleName='teststyle')

        self.image = Image()
        self.FormulaList = FormulaList()
        self.fo = AX_EXT.formula
        self.list=[]

        h=HorizontalPanel()
        h.setWidth("100%")
        h.add(self.image)
        h.add(self.FormulaList)
        h.setCellWidth(self.image,"50%")

        self.image.setUrl(latex_to_url(self.fo.to_latex()))

        RootPanel().add(button0)
        RootPanel().add(button1)
        RootPanel().add(button2)
        RootPanel().add(self.image)
        # RootPanel().add(outer)

        RootPanel().add(h)
