from pyjamas.ui.CheckBox import CheckBox
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.VerticalPanel import VerticalPanel

from app.FormulaBuilder import latex_to_url
from pyjamas.ui.Image import Image


class FormulaListPanel(VerticalPanel):
    def __init__(self):
        VerticalPanel.__init__(self)
        self.checkbox_list = []
        self.hpanel_list = []
        self.image_list = []

    def add_formula(self, f):
        h = HorizontalPanel()
        im = Image()
        im.setUrl(latex_to_url(f.to_latex()))
        c = CheckBox()
        h.add(c)
        h.add(im)
        self.add(h)
        self.checkbox_list.append(c)
        self.hpanel_list.append(h)
        self.image_list.append(im)

    def get_selected_indices(self):
        return [i for i, c in enumerate(self.checkbox_list) if c.isChecked()]

    def reload(self, formula_list):
        for h in self.hpanel_list[len(formula_list):]:
            self.remove(h)
        for f, im in zip(formula_list, self.image_list):
            im.setUrl(latex_to_url(f.to_latex()))
        x = formula_list[len(self.hpanel_list):]
        for f in x:
            self.add_formula(f)
