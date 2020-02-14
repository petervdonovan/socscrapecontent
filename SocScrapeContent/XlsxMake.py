from openpyxl import Workbook
from openpyxl.styles import Border, Side, Font, PatternFill

class XlsxMake:
    def __init__(self, pathwaysData, clubsData):
        self.pathwaysData = pathwaysData
        self.clubsData = clubsData
        self.wb = Workbook()
        self.pathwaysWs = self.wb.active
        self.pathwaysWs.title = 'Pathways'
        self.clubsWs = self.wb.create_sheet('Clubs')
        self.athleticsWs = self.wb.create_sheet('Athletics')

    def fill(self):
        for row in self.pathwaysData:
            self.pathwaysWs.append(row)
        for row in self.clubsData:
            self.clubsWs.append(row)
    def save(self, filename):
        try:
            self.wb.save(filename = 'sheets/' + filename)
        except:
            print('Unable to save. Is the file you intend to write to already open in another program?')
            input('Press enter when you have closed the file.')
            self.save(filename)

    def make(self, sectionWidth, sectionHeight):
        self.fill()
        self.formatPathwayWs(sectionWidth, sectionHeight)
        self.formatClubsWs()
        self.formatAthleticsWs()

    def formatPathwayWs(self, sectionWidth, sectionHeight):
        for topRow in range(1, len(self.pathwaysData), sectionHeight):
            #borders
            thin = Side(border_style="thin", color="000000")
            thick = Side(border_style="thick", color="000000")
            none = Side(border_style=None, color='FF000000')
            for row in range(topRow, topRow + sectionHeight):
                for col in range(1, sectionWidth + 1):
                    size = 12
                    bold = False
                    cell = self.pathwaysWs.cell(row, col)
                    if (cell.value):
                        left = right = top = bottom = thin
                    else:
                        left = right = top = bottom = none
                    if col == 0:
                        left = thick
                    if col == sectionWidth:
                        right = thick
                    if row == topRow:
                        top = thick
                    if row == topRow + sectionHeight - 1:
                        bottom = thick

                    #Style headers
                    cell = self.pathwaysWs.cell(row, col)
                    if (cell.value and (row - topRow < 2 or not self.pathwaysWs.cell(row - 1, col).value)):
                        bold = True
                    #handle exceptions on which headers should be bold
                    if (row - topRow == 16 and col == 6): bold = True
                    if (row - topRow == 17 and col == 4): bold = False

                    #Style top row
                    if row == topRow and col == 1:
                        left = top = right = left = thick
                        size = 18
                    cell.border = Border(left = left, right = right, top = top, bottom = bottom)
                    cell.font = Font(size = size, bold = bold)
                    self.pathwaysWs.merge_cells(start_row = topRow, start_column = 1, end_row = topRow, end_column = sectionWidth)
    def formatClubsWs(self):
        thin = Side(border_style="thin", color="666666")
        thick = Side(border_style="thick", color="000000")
        maxCol = 8;
        for row in self.clubsWs.iter_rows(min_row=1, max_row=10000, min_col=1, max_col=maxCol):
            color = '000000'
            cells = [cell for cell in row]
            if not cells[0].value:
                break;
            category = cells[3].value.lower()
            if(category == 'arts'):
                color = 'ff8888'
            elif(category == 'cultural'):
                color = '88ff88'
            elif(category == 'volunteering and advocacy'):
                color = '8888ff'
            elif(category == 'social'):
                color = '88ffff'
            elif(category == 'stem'):
                color = 'ff88ff'
            elif(category == 'other'):
                color = 'ffff88'
            for cell in cells:
                cell.fill = PatternFill("solid", fgColor=color)
                left = right = top = bottom = thin
                if (cell.column == maxCol):
                    right = thick
                if(color == '000000'):
                    cell.font = Font(color="ffffff")
                cell.border = Border(left = left, right = right, top = top, bottom = bottom)
    def formatAthleticsWs(self):
        head = ["Sport", "Gender (Boys, Girls, Coed)", "CIF -- years gone to playoffs (since 2000)", "Moore League -- years won (since 2000)", "Other tournaments/awards"]
        col = 1
        for item in head:
            cell = self.athleticsWs.cell(1, col)
            cell.value = item
            cell.fill = PatternFill("solid", fgColor='000000')
            cell.font = Font(color="ffffff")
            col += 1