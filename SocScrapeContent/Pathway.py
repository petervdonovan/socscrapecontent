import bs4
from bs4 import BeautifulSoup
from HtmlProc import HtmlProc
import re

class Pathway:
    def __init__(self, text):
        self.soup = BeautifulSoup(text, "html.parser")
    def getPlainText(self, id):
        text = ''
        description = self.soup.find(id = id)
        for formattingElement in description.select('.interns-ellipsis, .interns-show-more'):
            formattingElement.decompose()
        for child in description:
            add = HtmlProc.allProc(child)
            if not text.endswith(' ') and not add.startswith(' '):
                text += ' '
            text += add
        return text.strip()
    def getQuotes(self, id):
        text = self.getPlainText(id)
        parts = re.split(r'"|\u201C|\u201D', text)
        for i in range(1, len(parts), 2):
            parts[i] = '"' + parts[i] + '"'
        ret = [None, None]
        ret[0] = ''.join(parts[0:3]).strip()
        ret[1] = ''.join(parts[3:]).strip()
        return ret
    def getUlToCol(self, ulId): #the year must be a number
        courses = []
        year = self.soup.find(id = ulId)
        list = year.ul
        for li in list:
            courses.append(HtmlProc.allProc(li))
        courses = [course for course in courses if course.strip()]
        return courses
    def getPathwayName(self):
        return self.getPlainText('sl-cms2-page-title__h1').replace('-test', '')
    def getEntranceCriteria(self):
        criteria = {}
        table = self.soup.find(id = 'entrance-criteria')
        tds = [''.join(td.stripped_strings).strip() for td in list(table.find_all('td'))]
        if not tds: return {}
        keys = tds[::2]
        values = tds[1::2]
        for i, key in enumerate(keys):
            criteria[key] = values[i]
        return criteria
    def getVideoLink(self):
        if self.soup.video: return '=HYPERLINK("' + self.soup.video.source['src'] + '")'
        return ''
    def getAll(self):
        spreadsheet = [[None] * 6 for _ in range(25)]
        pathwayName = self.getPathwayName()
        description = self.getPlainText('pathway-description')
        courses9 = self.getUlToCol('grade-9')
        courses10 = self.getUlToCol('grade-10')
        courses11 = self.getUlToCol('grade-11')
        courses12 = self.getUlToCol('grade-12')
        popularElectives = self.getUlToCol('popular-electives')
        studentQuotes = self.getQuotes('student-quotes')
        staffQuotes = self.getQuotes('staff-quotes')
        videoLink = self.getVideoLink()
        entranceCriteria = self.getEntranceCriteria()
        
        spreadsheet[1][0] = 'Grade 9'
        spreadsheet[1][1] = 'Grade 10'
        spreadsheet[1][2] = 'Grade 11'
        spreadsheet[1][3] = 'Grade 12'
        spreadsheet[1][5] = 'Program Description'
        spreadsheet[13][0] = 'Popular Elective Options'
        spreadsheet[13][2] = 'Link to 1-2 Minute Video'
        spreadsheet[13][5] = 'Two Student Quotes'
        spreadsheet[16][2] = 'Entrance Criteria'
        spreadsheet[16][5] = 'Two Staff Quotes'

        i = 0
        for key in entranceCriteria:
            spreadsheet[i + 17][2] = key
            spreadsheet[i + 17][3] = entranceCriteria[key]
            i += 1

        spreadsheet[2][5] = description
        spreadsheet[0][0] = pathwayName
        for i, course in enumerate(courses9):
            spreadsheet[i + 2][0] = course
        for i, course in enumerate(courses10):
            spreadsheet[i + 2][1] = course
        for i, course in enumerate(courses11):
            spreadsheet[i + 2][2] = course
        for i, course in enumerate(courses12):
            spreadsheet[i + 2][3] = course

        for i, elective in enumerate(popularElectives):
            if (i < 10):
                spreadsheet[i + 14][0] = elective
            else:
                spreadsheet[i - 10 + 14][1] = elective

        for i, quote in enumerate(studentQuotes):
            spreadsheet[i + 14][5] = quote
        for i, quote in enumerate(staffQuotes):
            spreadsheet[i + 17][5] = quote

        spreadsheet[14][2] = videoLink

        return spreadsheet