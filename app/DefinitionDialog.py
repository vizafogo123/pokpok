from pyjamas import Window
from pyjamas.ui.Button import Button
from pyjamas.ui.DialogWindow import DialogWindow
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Image import Image
from pyjamas.ui.Label import Label
from pyjamas.ui.RadioButton import RadioButton
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.VerticalPanel import VerticalPanel

from app.FormulaBuilder import latex_to_url
from app.io import IO
from lion.Operation import Operation
from lion.Theorem import Theorem


class DefinitionDialog(DialogWindow):
    def __init__(self, **kwargs):
        DialogWindow.__init__(self, modal=True, close=True)
        v = VerticalPanel()
        v.setWidth(300)
        # v.setHeight(500)
        self.setText("definition")
        self.setPopupPosition(100, 100)
        self.setStyleAttribute("background-color", "#ffffff")
        self.setStyleAttribute("color", "#9847a2")
        self.setStyleAttribute("border-width", "5px")
        self.setStyleAttribute("border-style", "solid")
        h = HorizontalPanel()
        self.textbox_name = TextBox()
        h.add(Label("name"))
        h.add(self.textbox_name)
        v.add(h)
        h = HorizontalPanel()
        self.textbox_scheme = TextBox()
        h.add(Label("print scheme"))
        h.add(self.textbox_scheme)
        v.add(h)
        self.add(v)
        self.theorems = list()
        self.radios = list()
        for t in Theorem.theorems:
            if t.formula.is_in_unique_form():
                self.theorems.append(t)
                self.radios.append(RadioButton("group1", ""))
                h = HorizontalPanel()
                h.add(self.radios[-1])
                im = Image()
                im.setUrl(latex_to_url(t.formula.to_latex()))
                h.add(im)
                v.add(h)
        v.add(Button("Done", self.done_click))

    def done_click(self):
        for i in range(len(self.radios)):
            if self.radios[i].getChecked():
                op = Operation(Operation.get_new_id(), self.theorems[i].formula.get_no_of_args_for_unique_form(),
                               self.textbox_scheme.getText(), self.textbox_name.getText(), Operation.EXPRESSION)
                Operation.global_operations.append(op)
                Theorem.theorems.append(Theorem(self.theorems[i].formula.get_def_theorem(op),18,"iojo",[]))

        IO.save()
        self.hide()
