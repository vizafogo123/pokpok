from pyjamas.ui.CheckBox import CheckBox
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.VerticalPanel import VerticalPanel

from app.FormulaBuilder import latex_to_url
from pyjamas.ui.Image import Image


class FormulaList(VerticalPanel):
    def __init__(self):
        VerticalPanel.__init__(self)
        self.checkbox_list=[]

    def add_fomula(self,f):
        h=HorizontalPanel()
        im=Image()
        im.setUrl(latex_to_url(f.to_latex()))
        c=CheckBox()
        h.add(c)
        h.add(im)
        self.add(h)
        self.checkbox_list+=[c]

    def get_selected_indices(self):
        return [i for i, c in enumerate(self.checkbox_list) if c.isChecked()]
