from pyjamas import Window
from pyjamas.ui.CheckBox import CheckBox
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.ScrollPanel import ScrollPanel
from pyjamas.ui.VerticalPanel import VerticalPanel

from app.FormulaBuilder import latex_to_url
from pyjamas.ui.Image import Image


class FormulaListPanel(ScrollPanel):
    def __init__(self,onClick):
        ScrollPanel.__init__(self, Size=("630px", "500px"))
        self.checkbox_list = []
        self.hpanel_list = []
        self.image_list = []

        self.pok = VerticalPanel()
        self.add(self.pok)
        self.onclick=onClick

    def add_formula(self, f):
        h = HorizontalPanel()
        im = Image()
        im.setUrl(latex_to_url(f.to_latex()))
        c = CheckBox()
        h.add(c)
        h.add(im)
        self.pok.add(h)
        self.checkbox_list.append(c)
        self.hpanel_list.append(h)
        self.image_list.append(im)

    def set_checks_to_def(self,split_points):
        for i in range(len(self.checkbox_list)):
            self.checkbox_list[i].setChecked(False)
            if i in split_points:
                self.checkbox_list[i].setStyleAttribute('background-color','#FF0000')
            else:
                self.checkbox_list[i].setStyleAttribute('background-color', 'transparent')
        self.checkbox_list[-1].setChecked(True)

    def get_selected_indices(self):
        return [i for i, c in enumerate(self.checkbox_list) if c.isChecked()]

    def reload(self, formula_list,split_points):
        if len(formula_list)<len(self.hpanel_list):
            for h in self.hpanel_list[len(formula_list):]:
                self.pok.remove(h)
            self.hpanel_list=self.hpanel_list[:len(formula_list)]
            self.checkbox_list = self.checkbox_list[:len(formula_list)]
            self.image_list = self.image_list[:len(formula_list)]
        for f, im in zip(formula_list, self.image_list):
            im.setUrl(latex_to_url(f.to_latex()))
        x = formula_list[len(self.hpanel_list):]
        for f in x:
            self.add_formula(f)
        self.set_checks_to_def(split_points)

        for i in range(len(self.image_list)):
            self.image_list[i].clearClickListener()
            self.image_list[i].addClickListener(self.onclick(i))

