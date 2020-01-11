from Ui import Ui

ui = Ui()
while(ui.getPathways(suffix = '-test')): pass
ui.makeXlsx(6, 25)
ui.save()