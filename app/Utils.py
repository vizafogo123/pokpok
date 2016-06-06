import urllib

from pyjamas.ui.Image import Image

def latex_to_url(latex):
    return 'http://latex.codecogs.com/gif.download?' + urllib.quote(latex)

def fill_flextable_with_cnf(flextable, cnf):
    k=flextable.getRowCount()
    for i in range(k):
        flextable.removeRow(0)
    latex_vectors = cnf.get_latex_vectors()
    for i in range(len(latex_vectors)):
        for j in range(len(latex_vectors[i])):
            flextable.setWidget(i, j, Image(latex_to_url(latex_vectors[i][j])))
