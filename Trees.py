import urllib

from pokpok.Formula import Formula
from pokpok.Operation import operations
from pyjamas.ui import HasAlignment
from pyjamas.ui.DialogBox import DialogBox
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
        self.ops=[{"op":op,"proto":Proto(op.name)} for op in operations if op.available]

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
        self.image2=Image()
        self.panel.add(self.image1)
        self.panel.add(self.image2)

        self.initWidget(self.panel)



        # self.initWidget(self.fTree)

    def onTreeItemSelected(self, item):
         dlg = DialogBox(self.baseURL())
         left = 100
         top = 100

         closeButton = Button("Close", dlg)
         msg = HTML("<center>This is an example of a standard dialog box component.<br>  You can put pretty much anything you like into it,<br>such as the following IFRAME:</center>", True)

         dock = DockPanel()
         dock.setSpacing(4)

         dock.add(closeButton, DockPanel.SOUTH)
         dock.add(msg, DockPanel.NORTH)

         dock.setCellHorizontalAlignment(closeButton, HasAlignment.ALIGN_RIGHT)
         dock.setWidth("100%")


         dlg.setText("opkop")
         dlg.setPopupPosition(left, top)
         dlg.setStyleAttribute("background-color","#8a00b8")
         dlg.setStyleAttribute("color","white")
         dlg.setStyleAttribute("border-width","5px")
         dlg.setStyleAttribute("text-transform","uppercase")
         dlg.setStyleAttribute("border-style","solid")

         dlg.onClick=lambda x:dlg.hide()
         # dlg.setDefaults()
         dlg.setWidget(dock)

         # dlg.setElement("body",)

         dlg.show()
         if item.children == []:
            if not self.f.is_closed():
                for op in [x["op"] for x in self.ops if item.userObject==x["proto"]]:
                    self.f.add_one_op(op)
                    self.image1.setUrl(latex_to_url(self.f.fill_with_placeholders().to_latex()))
            else:

                self.f=self.f.simplify()
                #self.image2.setUrl(latex_to_url(self.f.to_latex()))
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
