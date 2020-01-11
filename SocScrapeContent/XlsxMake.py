from openpyxl import Workbook
from openpyxl.styles import Border, Side, Font

class XlsxMake:
    def __init__(self, data):
        self.data = data
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = 'Pathways'
        self.fill()

    def fill(self):
        for row in self.data:
            self.ws.append(row)

    def save(self, filename):
        try:
            self.wb.save(filename = 'sheets/' + filename)
        except:
            print('Unable to save. Is the file you intend to write to already open in another program?')
            input('Press enter when you have closed the file.')
            self.save(filename)

    def format(self, sectionWidth, sectionHeight):
        #self.ws.delete_rows(sectionHeight, 1)
        for topRow in range(1, len(self.data), sectionHeight):
            #borders
            thin = Side(border_style="thin", color="000000")
            thick = Side(border_style="thick", color="000000")
            none = Side(border_style=None, color='FF000000')
            #if topRow >= sectionHeight: topRow -= 1 #Compensate for the first section being 1 shorter than the rest
            for row in range(topRow, topRow + sectionHeight):
                for col in range(1, sectionWidth + 1):
                    size = 12
                    bold = False
                    cell = self.ws.cell(row, col)
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
                    cell = self.ws.cell(row, col)
                    if (cell.value and (row - topRow < 2 or not self.ws.cell(row - 1, col).value)):
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
                    self.ws.merge_cells(start_row = topRow, start_column = 1, end_row = topRow, end_column = sectionWidth)
