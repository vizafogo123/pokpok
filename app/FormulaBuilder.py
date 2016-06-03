from pyjamas.ui.DialogWindow import DialogWindow
from pyjamas.ui.Button import Button
from pyjamas.ui.DockPanel import DockPanel
from pyjamas.ui.HTML import HTML
from pyjamas.ui.Image import Image
from pyjamas.ui import HasAlignment

from app.Utils import latex_to_url
from lion.Formula import Formula


class FormulaBuilder(DialogWindow):
    def __init__(self, operations, after, type='rel'):
        DialogWindow.__init__(self, modal=True, close=True)
        self.formula = Formula([])
        self.after = after
        self.type = type

        left = 100
        top = 100

        self.ops_with_buttons = [{"op": op, "button": Button(op.name, self)} for op in operations if op.available]
        dock = DockPanel()
        dock.setSpacing(3)

        for owb in self.ops_with_buttons:
            dock.add(owb['button'], DockPanel.NORTH)

        dock.setWidth("300")

        self.image = Image(latex_to_url(self.formula.fill_with_placeholders().to_latex()))
        dock.add(self.image, DockPanel.EAST)
        dock.setCellHorizontalAlignment(self.image, HasAlignment.ALIGN_TOP)

        self.doneButton = Button("Done", self)
        self.doneButton.setEnabled(False)
        dock.add(self.doneButton, DockPanel.SOUTH)

        dock.add(HTML(""), DockPanel.CENTER)

        self.setText("opkop")
        self.setPopupPosition(left, top)
        self.setStyleAttribute("background-color", "#ffffff")
        self.setStyleAttribute("color", "blue")
        self.setStyleAttribute("border-width", "5px")
        self.setStyleAttribute("border-style", "solid")

        self.setWidget(dock)

    def onClick(self, sender):
        if sender == self.doneButton:
            self.hide()
            self.after(self.formula)

        op = None
        for owb in self.ops_with_buttons:
            if owb['button'] == sender:
                self.setText(sender.getText())
                op = owb['op']

        if not self.formula.is_closed():
            self.formula.add_one_op(op, self.type)
            self.image.setUrl(latex_to_url(self.formula.fill_with_placeholders().to_latex()))
            if self.formula.is_closed():
                self.doneButton.setEnabled(True)
