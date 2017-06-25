from pyjamas import Window
from pyjamas.ui import HasAlignment
from pyjamas.ui.Button import Button
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.RootPanel import RootPanel

from app.FormulaBuilder import FormulaBuilder
from app.FormulaListPanel import FormulaListPanel
from app.TheoremPanel import TheoremPanel
from lion.Operation import operations
from lion.Proof import proof
from lion.Rules import Rules


class Root():
    def __init__(self):
        pass

    def button_test_click(self):
        def after(formula):
            self.add_formula(formula)

        FormulaBuilder([op for op in operations if op.available], after, type='rel').show()

    def selected_formulas(self):
        return [x for i, x in enumerate(proof.get_formula_list()) if i in self.FormulaListPanel.get_selected_indices()]

    def button_rule_click(self, rule):
        def pok():
            if not rule.is_applicable(self.selected_formulas()):
                Window.alert(self.FormulaListPanel.get_selected_indices())
                return
            rule.apply(self.selected_formulas(), self.add_formula)

        return pok

    def add_formula(self, formula, **kwargs):
        proof.add(formula,**kwargs)
        self.FormulaListPanel.reload(proof.get_formula_list())

    def sakop(self,poj):
        Window.alert(poj.formula.dump())

    def start(self):
        button_test = Button("dojdojdoj", self.button_test_click)

        for r in Rules:
            RootPanel().add(Button(r.name, self.button_rule_click(r), StyleName='teststyle'))
        RootPanel().add(button_test)

        self.FormulaListPanel = FormulaListPanel()
        self.TheoremPanel = TheoremPanel(self.add_formula)

        h = HorizontalPanel(BorderWidth=1,
                                HorizontalAlignment=HasAlignment.ALIGN_LEFT,
                                VerticalAlignment=HasAlignment.ALIGN_TOP,
                                Width="100%",
                                Height="200px")
        h.setStyleAttribute("background", "yellow")
        h.add(self.FormulaListPanel)
        h.add(self.TheoremPanel)
        h.setCellWidth(self.FormulaListPanel,"50%")
        h.setCellWidth(self.TheoremPanel,"50%")
        RootPanel().add(h)

        # panel = HorizontalPanel(BorderWidth=1,
        #                         HorizontalAlignment=HasAlignment.ALIGN_CENTER,
        #                         VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
        #                         Width="100%",
        #                         Height="200px")
        #
        # part1 = Label("Part 1")
        # part2 = Label("Part 2")
        # part3 = Label("Part 3")
        # part4 = Label("Part 4")
        #
        # panel.add(part1)
        # panel.add(part2)
        # panel.add(part3)
        # panel.add(part4)
        #
        # panel.setCellWidth(part1, "10%")
        # panel.setCellWidth(part2, "70%")
        # panel.setCellWidth(part3, "10%")
        # panel.setCellWidth(part4, "10%")
        #
        # panel.setCellVerticalAlignment(part3, HasAlignment.ALIGN_BOTTOM)
        #
        # RootPanel().add(panel)
