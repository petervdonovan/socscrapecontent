from Ui import Ui

# Create user interface
ui = Ui()
# Ask user the names of the pathways. To get pathway info, it also
# has to ask the base URL of the website
ui.getPathways()
# Pull club information from the website (does not require user input)
ui.getClubs()
# create and save the spreadsheet
ui.makeXlsx(6, 25)
ui.save()