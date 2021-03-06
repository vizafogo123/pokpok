from pyjamas import Window
from pyjamas.ui.DialogWindow import DialogWindow
from pyjamas.ui.Button import Button
from pyjamas.ui.DockPanel import DockPanel
from pyjamas.ui.HTML import HTML
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Image import Image
from pyjamas.ui import HasAlignment

import urllib

from pyjamas.ui.TextBox import TextBox

from lion.Formula import Formula
from lion.Operation import Operation


def latex_to_url(latex):
    return 'http://latex.codecogs.com/gif.download?' + urllib.quote(latex)


class FormulaBuilder(DialogWindow):
    def __init__(self, operations, after, **kwargs):
        DialogWindow.__init__(self, modal=True, close=True)
        self.formula = Formula([])
        self.after = after
        if "type" in kwargs:
            self.type = kwargs["type"]
        else:
            self.type = 'rel'

        self.set_styles()

        def op_button_click(op):
            def aio():
                self.add_op(op)

            return aio

        self.ops_with_buttons = [{"op": op, "button": Button(op.name, op_button_click(op))} for op in operations]

        for owb in self.ops_with_buttons:
            self.add_button(owb["button"])

        self.var = list()
        self.is_clicked = list()
        self.textbox = list()

        self.set_variables((0 if self.type == 'exp' else 5))

    def set_variables(self, no_of_vars, x=True):
        def name(n):
            return "var" + str(n)

        def print_scheme(n):
            return ["\\alpha", "\\beta", "\\gamma", "\\delta", "\\epsilon"][n]

        def button_click(n):
            def sopa():
                if not self.is_clicked[n]:
                    v = Operation(name(n), 0, self.textbox[n].getText(), name(n), Operation.VARIABLE)
                    self.var[n] = v
                    self.textbox[n].setEnabled(False)
                    self.is_clicked[n] = True
                self.add_op(self.var[n])

            return sopa

        for i in range(no_of_vars):
            h = HorizontalPanel()
            b = Button("variable", button_click(i))
            h.add(b)
            self.is_clicked.append(False)
            self.var.append(None)
            t = TextBox()
            self.textbox.append(t)
            t.setText(print_scheme(i))
            h.add(t)
            self.add_button(h)

    def set_styles(self):
        self.dock = DockPanel()
        self.dock.setSpacing(3)

        self.dock.setWidth("300")

        self.image = Image(latex_to_url(self.formula.fill_with_placeholders().to_latex()))
        self.dock.add(self.image, DockPanel.EAST)
        self.dock.setCellHorizontalAlignment(self.image, HasAlignment.ALIGN_TOP)

        self.backspaceButton_add()
        self.doneButton_add()

        self.dock.add(HTML(""), DockPanel.CENTER)
        left = 100
        top = 100

        self.setText("opkop")
        self.setPopupPosition(left, top)
        self.setStyleAttribute("background-color", "#ffffff")
        self.setStyleAttribute("color", "blue")
        self.setStyleAttribute("border-width", "5px")
        self.setStyleAttribute("border-style", "solid")

        self.setWidget(self.dock)

    def doneButton_add(self):
        def doneButton_click():
            self.hide()
            self.after(self.formula)

        self.doneButton = Button("Done", doneButton_click)
        self.doneButton.setEnabled(False)
        self.dock.add(self.doneButton, DockPanel.SOUTH)

    def backspaceButton_add(self):
        def backspaceButton_click():
            self.formula = Formula(self.formula.body[:-1])
            self.refresh()

        self.backspaceButton = Button("Backspace", backspaceButton_click)
        self.backspaceButton.setEnabled(False)
        self.dock.add(self.backspaceButton, DockPanel.SOUTH)

    def refresh(self):
        self.image.setUrl(latex_to_url(self.formula.fill_with_placeholders().to_latex()))
        self.doneButton.setEnabled(self.formula.is_closed())
        self.backspaceButton.setEnabled(len(self.formula.body) >= 0)

    def add_button(self, b):
        self.dock.add(b, DockPanel.NORTH)

    def add_op(self, op):
        if not self.formula.is_closed():
            self.formula.add_one_op(op, self.type)
            self.refresh()
