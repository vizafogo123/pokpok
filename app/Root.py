from pyjamas import Window
from pyjamas.ui.Button import Button
from pyjamas.ui.FlexTable import FlexTable
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Image import Image
from pyjamas.ui.RootPanel import RootPanel

from app.FormulaBuilder import latex_to_url, FormulaBuilder
from app.FormulaList import FormulaList
from lion.Formula import Formula
from lion.NormalForm import NormalForm
from lion.Operation import operations, FORALL
from lion.Theorem import AX_CHO, AX_EXT


class Root():
    def __init__(self):
        pass

    def button0_click(self):
        if self.fo.body[0] not in [FORALL]:
            Window.alert("daj!")
            return

        def after(formula):
            self.fo = Formula(self.fo.body[2:]).substitute(Formula([self.fo.body[1]]), formula)
            self.image.setUrl(latex_to_url(self.fo.to_latex()))

        a = FormulaBuilder([op for op in operations if op.available], after, type='exp')
        a.show()

    def button1_click(self):
        self.FormulaList.add_fomula(self.fo)
        self.list.append(self.fo.deepcopy())

    def button2_click(self):
        if len(self.FormulaList.get_selected_indices())<>1:
            Window.alert("lari!")
            return
        self.f=self.list[self.FormulaList.get_selected_indices()[0]]
        if self.f.body[0] not in [FORALL]:
            Window.alert("daj!")
            return

        def after(formula):
            self.f = Formula(self.f.body[2:]).substitute(Formula([self.f.body[1]]), formula)
            self.FormulaList.add_fomula(self.f)
            self.list.append(self.f.deepcopy())

        a = FormulaBuilder([op for op in operations if op.available], after, type='exp')
        a.show()


    def start(self):

        kop = AX_CHO.cnf.get_latex_vectors()
        outer = FlexTable(BorderWidth="1")

        for i in range(len(kop)):
            for j in range(len(kop[i])):
                outer.setWidget(i, j, Image(latex_to_url(kop[i][j])))

        button0 = Button("Begin", self.button0_click, StyleName='teststyle')
        button1 = Button("Topsa", self.button1_click, StyleName='teststyle')
        button2 = Button("gen", self.button2_click, StyleName='teststyle')

        self.image = Image()
        self.cnf = NormalForm([])

        def after(cnf):
            self.cnf += cnf
            self.image.setUrl(latex_to_url(self.cnf.to_latex()))
            if self.cnf.is_degenerate():
                Window.alert("SADAT ABDEL")

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
