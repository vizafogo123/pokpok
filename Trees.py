import urllib

from pokpok.Formula import Formula
from pokpok.Operation import operations
from pyjamas.ui import HasAlignment
from pyjamas.ui.DialogBox import DialogBox
from pyjamas.ui.DialogWindow import DialogWindow
from pyjamas.ui.DockPanel import DockPanel
from pyjamas.ui.HTML import HTML
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Image import Image
from pyjamas.ui.Sink import Sink, SinkInfo
from pyjamas.ui.Tree import Tree
from pyjamas.ui.TreeItem import TreeItem
from pyjamas import Window
from pyjamas.ui.Button import Button

from sink.Popups import MyDialog, MyDialogWindow


def latex_to_url(latex):
    return 'http://latex.codecogs.com/gif.download?' + urllib.quote(latex)


class Trees(Sink):
    def __init__(self):
        self.ops = [{"op": op, "proto": Proto(op.name)} for op in operations if op.available]

        Sink.__init__(self)
        self.fProto = [
            Proto("Beethoven", [x["proto"] for x in self.ops])
        ]

        self.fTree = Tree()

        for i in range(len(self.fProto)):
            self.createItem(self.fProto[i])
            self.fTree.addItem(self.fProto[i].item)

        self.fTree.addTreeListener(self)

        self.panel = HorizontalPanel(VerticalAlignment=HasAlignment.ALIGN_TOP)
        self.panel.setSpacing(40)
        self.panel.add(self.fTree)

        self.f = Formula([])

        self.image1 = Image(latex_to_url(self.f.fill_with_placeholders().to_latex()))
        self.image2 = Image()
        self.panel.add(self.image1)
        self.panel.add(self.image2)

        self.initWidget(self.panel)

    def onTreeItemSelected(self, item):
        dlg = FormulaBuilder(operations)

        dlg.show()
        if item.children == []:
            if not self.f.is_closed():
                for op in [x["op"] for x in self.ops if item.userObject == x["proto"]]:
                    self.f.add_one_op(op)
                    self.image1.setUrl(latex_to_url(self.f.fill_with_placeholders().to_latex()))
            else:

                self.f = self.f.simplify()
                # self.image2.setUrl(latex_to_url(self.f.to_latex()))
                self.image2.setUrl(latex_to_url(self.f.to_cnf().to_latex()))

    def onTreeItemStateChanged(self, item):
        child = item.getChild(0)
        if hasattr(child, "isPendingItem"):
            item.removeItem(child)

            proto = item.getUserObject()
            for i in range(len(proto.children)):
                self.createItem(proto.children[i])
                index = self.getSortIndex(item, proto.children[i].text)
                # demonstrate insertItem.  addItem is easy.
                item.insertItem(proto.children[i].item, index)

    def getSortIndex(self, parent, text):
        nodes = parent.getChildCount()
        node = 0
        text = text.lower()

        while node < nodes:
            item = parent.getChild(node)
            if cmp(text, item.getText().lower()) < 0:
                break;
            else:
                node += 1

        return node

    def createItem(self, proto):
        proto.item = TreeItem(proto.text)
        proto.item.setUserObject(proto)
        if len(proto.children) > 0:
            proto.item.addItem(PendingItem())


class Proto:
    def __init__(self, text, children=None):
        self.children = []
        self.item = None
        self.text = text

        if children is not None:
            self.children = children


class PendingItem(TreeItem):
    def __init__(self):
        TreeItem.__init__(self, "Please wait...")

    def isPendingItem(self):
        return True


def init():
    text = "GWT has a built-in <code>Tree</code> widget. The tree is focusable and has keyboard support as well."
    return SinkInfo("Trees", text, Trees)


class FormulaBuilder(DialogWindow):
    def __init__(self, operations):
        DialogWindow.__init__(self, modal=True, close=True)

        left = 100
        top = 100

        self.ops_with_buttons = [{"op": op, "button": Button(op.name, self)} for op in operations if op.available]
        self.f = Formula([])
        dock = DockPanel()
        dock.setSpacing(20)

        for owb in self.ops_with_buttons:
            dock.add(owb['button'], DockPanel.NORTH)

        # dock.setCellHorizontalAlignment(closeButton, HasAlignment.ALIGN_RIGHT)
        dock.setWidth("300")

        self.image = Image(latex_to_url(self.f.fill_with_placeholders().to_latex()))
        dock.add(self.image, DockPanel.EAST)

        self.doneButton=Button("Done",self)
        dock.add(self.doneButton,DockPanel.SOUTH)

        self.setText("opkop")
        self.setPopupPosition(left, top)
        self.setStyleAttribute("background-color", "#ffffff")
        self.setStyleAttribute("color", "white")
        self.setStyleAttribute("border-width", "5px")
        self.setStyleAttribute("border-style", "solid")

        self.setWidget(dock)

    def onClick(self, sender):
        if sender==self.doneButton:
            self.hide()

        op=None
        for owb in self.ops_with_buttons:
            if owb['button'] == sender:
                self.setText(sender.getText())
                op=owb['op']

        if not self.f.is_closed():
            self.f.add_one_op(op)
            self.image.setUrl(latex_to_url(self.f.fill_with_placeholders().to_latex()))
