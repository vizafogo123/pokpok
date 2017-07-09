from pyjamas import Window
from pyjamas.ui.Button import Button
from pyjamas.ui.DialogWindow import DialogWindow
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.Image import Image
from pyjamas.ui.Label import Label
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.RadioButton import RadioButton
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.VerticalPanel import VerticalPanel

from app.FormulaBuilder import latex_to_url
from app.io import IO
from lion.Theorem import Theorem


class SaveDialog(DialogWindow):
    def __init__(self, theorem, **kwargs):
        DialogWindow.__init__(self, modal=True, close=True)
        self.theorem=theorem
        v = VerticalPanel()
        v.setWidth(300)
        # v.setHeight(500)
        self.setText("save")
        self.setPopupPosition(100, 100)
        self.setStyleAttribute("background-color", "#ffffff")
        self.setStyleAttribute("color", "red")
        self.setStyleAttribute("border-width", "5px")
        self.setStyleAttribute("border-style", "solid")
        self.im=Image()
        self.im.setUrl(latex_to_url(self.theorem.formula.to_latex()))
        v.add(self.im)
        h=HorizontalPanel()
        self.radio=RadioButton("group1", "Existing folder:")
        h.add(self.radio)
        self.list = ListBox()
        self.list.setVisibleItemCount(1)
        for f in Theorem.get_all_folders():
            self.list.addItem(f)

        h.add(self.list)
        v.add(h)
        h=HorizontalPanel()
        h.add(RadioButton("group1", "New folder:"))
        self.radio.setChecked(True)
        self.textbox=TextBox()
        h.add(self.textbox)
        v.add(h)
        v.add(Button("Done",self.done_click))
        self.add(v)

    def get_folder_name(self):
        if self.radio.getChecked():
            return self.list.getItemText(self.list.getSelectedIndex())
        else:
            return self.textbox.getText()

    def done_click(self):
        self.theorem.folder=self.get_folder_name()
        Theorem.theorems.append(self.theorem)
        IO.save()
        self.hide()
