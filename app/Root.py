from pyjamas import Window
from pyjamas.ui import HasAlignment
from pyjamas.ui.Button import Button
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Label import Label
from pyjamas.ui.RootPanel import RootPanel

from app.FormulaBuilder import FormulaBuilder
from app.FormulaListPanel import FormulaListPanel
from app.SaveDialog import SaveDialog
from app.TheoremPanel import TheoremPanel
from app.io import IO
from lion.Operation import Operation
from lion.Proof import proof
from lion.Rules import Rules
from lion.Theorem import Theorem


class Root():
    def __init__(self):
        pass

    def button_test_click(self):
        def after(formula):
            self.add_formula(formula, predecessors=[], rule_name="dojdojdoj")

        FormulaBuilder(proof.get_operations(), after, type='rel').show()

    def button_rule_click(self, rule):
        def res():
            proof.apply_rule(rule,self.FormulaListPanel.get_selected_indices(),self.refresh)
        return res

    def refresh(self):
        self.FormulaListPanel.reload(proof.get_formula_list())

    def add_formula(self, formula, **kwargs):
        if not "predecessors" in kwargs:
            kwargs["predecessors"] = self.FormulaListPanel.get_selected_indices()
        proof.add(formula, **kwargs)
        self.refresh()

    def hide_formulas(self):
        proof.hide_formulas(self.FormulaListPanel.get_selected_indices())
        self.FormulaListPanel.reload(proof.get_formula_list())

    def unhide_all(self):
        Window.alert([p.rule_name for p in proof.body])
        proof.unhide_all()
        self.FormulaListPanel.reload(proof.get_formula_list())

    def download_data(self, after):
        def after1(json):
            Operation.global_operations = [Operation.from_dict(op) for op in json["operations"]]
            Theorem.theorems = [Theorem.from_dict(th) for th in json["theorems"]]
            self.label_done.setText("done")
            after()
            # put_request({"operations": [o.to_json() for o in Operation.global_operations],
            #              "theorems": [ax.to_json() for ax in Theorem.axioms]})

        IO.get_request(after1)

    def button_save(self):
        t=proof.get_theorem_to_save(self.FormulaListPanel.get_selected_indices())
        if t is not None:
            SaveDialog(t).show()
        # IO.put_request(proof.to_json(),file_name="http://api.myjson.com/bins/16lyhr")

    def setup_before_data(self):
        self.button_test = Button("dojdojdoj", self.button_test_click)
        self.button_hide = Button("hide", self.hide_formulas)
        self.button_unhide = Button("unhide all", self.unhide_all)
        self.button_save = Button("save", self.button_save)
        self.label_done = Label("loading")

        self.FormulaListPanel = FormulaListPanel()

        for r in Rules:
            RootPanel().add(Button(r.name, self.button_rule_click(r), StyleName='teststyle'))
        RootPanel().add(self.button_test)
        RootPanel().add(self.button_hide)
        RootPanel().add(self.button_unhide)
        RootPanel().add(self.button_save)
        RootPanel().add(self.label_done)



    def setup_after_data(self):
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

    def start(self):
        self.setup_before_data()
        self.download_data(self.setup_after_data)
