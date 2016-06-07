from lion.Operation import Operation
from pyjamas import Window
from pyjamas.ui.DialogWindow import DialogWindow
from pyjamas.ui.Button import Button
from pyjamas.ui.DockPanel import DockPanel
from pyjamas.ui.HTML import HTML
from pyjamas.ui.Image import Image
from pyjamas.ui import HasAlignment
from pyjamas.ui.Tree import Tree
from pyjamas.ui.TreeItem import TreeItem

from app.Utils import latex_to_url
from lion.Formula import Formula
from lion.ProofState import global_proof_state


class FormulaBuilder(DialogWindow):
    def __init__(self, operations, after, type='rel'):
        DialogWindow.__init__(self, modal=True, close=True)
        self.formula = Formula([])
        self.after = after
        self.type = type
        self.operations = operations

        left = 100
        top = 100
        self.ops_to_treeitems = {op: TreeItem(op.name) for op in self.operations if op.available}
        self.construct_tree()

        self.dock = DockPanel()
        self.dock.setSpacing(3)

        self.dock.add(self.tree, DockPanel.WEST)

        self.dock.setWidth("300")

        self.image = Image(latex_to_url(self.formula.fill_with_placeholders().to_latex()))
        self.dock.add(self.image, DockPanel.EAST)
        self.dock.setCellHorizontalAlignment(self.image, HasAlignment.ALIGN_TOP)

        self.doneButton = Button("Done", self)
        self.doneButton.setEnabled(False)
        self.dock.add(self.doneButton, DockPanel.SOUTH)

        self.dock.add(HTML(""), DockPanel.CENTER)

        self.setText("opkop")
        self.setPopupPosition(left, top)
        self.setStyleAttribute("background-color", "#ffffff")
        self.setStyleAttribute("color", "blue")
        self.setStyleAttribute("border-width", "5px")
        self.setStyleAttribute("border-style", "solid")

        self.setWidget(self.dock)

    def construct_tree(self):
        self.tree = Tree()
        x1 = TreeItem('Global')
        x2 = TreeItem('Quantors')
        x3 = TreeItem('Logical')
        x4 = TreeItem('Relations')
        x5 = TreeItem('Expressions')
        x6 = TreeItem('Variables')
        self.tree.addItem(x1)
        x1.addItem(x2)
        x1.addItem(x3)
        x1.addItem(x4)
        x1.addItem(x5)
        x1.addItem(x6)

        oaij = {Operation.QUANTOR: x2,
                Operation.LOGICAL: x3,
                Operation.RELATION: x4,
                Operation.EXPRESSION: x5,
                Operation.VARIABLE: x6}

        y1 = TreeItem('Local')
        y4 = TreeItem('Relations')
        y5 = TreeItem('Expressions')
        y6 = TreeItem('Variables')
        self.tree.addItem(y1)
        y1.addItem(y4)
        y1.addItem(y5)
        y1.addItem(y6)

        rferf = {Operation.RELATION: y4,
                Operation.EXPRESSION: y5,
                Operation.VARIABLE: y6}

        for op in self.operations:
            (oaij if op in global_proof_state.operations else rferf)[op.type].addItem(self.ops_to_treeitems[op])

        self.tree.addTreeListener(self)

    def onTreeItemSelected(self, item):
        for op in self.operations:
            if item == self.ops_to_treeitems[op]:
                self.op_selected(op)

    def onClick(self, sender):
        if sender == self.doneButton:
            self.hide()
            self.after(self.formula)

    def op_selected(self, op):
        if not self.formula.is_closed():
            self.formula.add_one_op(op, self.type)
            self.image.setUrl(latex_to_url(self.formula.fill_with_placeholders().to_latex()))
            if self.formula.is_closed():
                self.doneButton.setEnabled(True)
