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


def latex_to_url(latex):
    return 'http://latex.codecogs.com/gif.download?' + urllib.quote(latex)


class FormulaBuilder(DialogWindow):
    def __init__(self, operations, after, type='rel'):
        DialogWindow.__init__(self, modal=True, close=True)
        self.formula = Formula([])
        self.after = after
        self.type = type

        self.set_styles()

        def op_button_click(op):
            def aio():
                self.add_op(op)
            return aio

        self.ops_with_buttons = [{"op": op, "button": Button(op.name,op_button_click(op))} for op in operations if op.available]

        for owb in self.ops_with_buttons:
            self.add_button(owb["button"])

        self.set_variables(1)

    def set_variables(self,no_of_vars,x=True):
        for i in range(no_of_vars):
            h = HorizontalPanel()
            h.add(Button("variable"))
            t=TextBox()
            t.setText("aoka")
            h.add(t)
            self.add_button(h)


    def set_styles(self):
        self.dock = DockPanel()
        self.dock.setSpacing(3)

        self.dock.setWidth("300")

        self.image = Image(latex_to_url(self.formula.fill_with_placeholders().to_latex()))
        self.dock.add(self.image, DockPanel.EAST)
        self.dock.setCellHorizontalAlignment(self.image, HasAlignment.ALIGN_TOP)

        self.doneButton = Button("Done", self)
        self.doneButton.setEnabled(False)
        self.dock.add(self.doneButton, DockPanel.SOUTH)

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

    def add_button(self,b):
        self.dock.add(b, DockPanel.NORTH)

    def add_op(self,op):
        if not self.formula.is_closed():
            self.formula.add_one_op(op, self.type)
            self.image.setUrl(latex_to_url(self.formula.fill_with_placeholders().to_latex()))
            if self.formula.is_closed():
                self.doneButton.setEnabled(True)



    def onClick(self, sender):
        if sender == self.doneButton:
            self.hide()
            self.after(self.formula)
