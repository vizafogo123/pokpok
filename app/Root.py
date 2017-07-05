from pyjamas import Window
from pyjamas.ui import HasAlignment
from pyjamas.ui.Button import Button
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.RootPanel import RootPanel

from app.FormulaBuilder import FormulaBuilder
from app.FormulaListPanel import FormulaListPanel
from app.TheoremPanel import TheoremPanel
from app.io import get_request, put_request
from lion.Operation import global_operations
from lion.Proof import proof
from lion.Rules import Rules
from lion.Theorem import axioms


class Root():
    def __init__(self):
        pass

    def button_test_click(self):
        def after(formula):
            self.add_formula(formula, predecessors=[], rule_name="dojdojdoj")

        FormulaBuilder(proof.get_operations(), after, type='rel').show()

    def selected_formulas(self):
        return [x for i, x in enumerate(proof.get_formula_list()) if i in self.FormulaListPanel.get_selected_indices()]

    def button_rule_click(self, rule):
        def pok():
            if not rule.is_applicable(self.selected_formulas()):
                Window.alert("opkop")
                return
            rule.apply(self.selected_formulas(), self.add_formula)

        return pok

    def add_formula(self, formula, **kwargs):
        if not "predecessors" in kwargs:
            kwargs["predecessors"] = self.FormulaListPanel.get_selected_indices()
        proof.add(formula, **kwargs)
        self.FormulaListPanel.reload(proof.get_formula_list())

    def hide_formulas(self):
        proof.hide_formulas(self.FormulaListPanel.get_selected_indices())
        self.FormulaListPanel.reload(proof.get_formula_list())

    def unhide_all(self):
        Window.alert([p.rule_name for p in proof.body])
        proof.unhide_all()
        self.FormulaListPanel.reload(proof.get_formula_list())

    def start(self):
        button_test = Button("dojdojdoj", self.button_test_click)
        button_hide = Button("hide", self.hide_formulas)
        button_unhide = Button("unhide all", self.unhide_all)

        for r in Rules:
            RootPanel().add(Button(r.name, self.button_rule_click(r), StyleName='teststyle'))
        RootPanel().add(button_test)
        RootPanel().add(button_hide)
        RootPanel().add(button_unhide)

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
        h.setCellWidth(self.FormulaListPanel, "50%")
        h.setCellWidth(self.TheoremPanel, "50%")
        RootPanel().add(h)
        # put_request({"operations":[o.to_json() for o in global_operations],"theorems":[ax.to_json() for ax in axioms]})

        def sakop(poj):
            Window.alert(poj["theorems"][8])

        # get_request(sakop)
