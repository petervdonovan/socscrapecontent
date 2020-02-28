import bs4
from bs4 import BeautifulSoup
from HtmlProc import HtmlProc
import re

class Pathway:
    '''
    Object representation of a Pathway at a school site.
    '''
    def __init__(self, text):
        '''
        Store HTML pulled from online as an object that can be navigated more easily than a string
        '''
        self.soup = BeautifulSoup(text, "html.parser")

    def getPlainText(self, id):
        '''
        Return string form of a DOM element of given ID, with UI elements removed
        '''
        text = ''
        description = self.soup.find(id = id)
        # Remove UI elements that do not contain information about the pathway
        for formattingElement in description.select('.interns-ellipsis, .interns-show-more'):
            formattingElement.decompose()
        # make sure that anything that would be run together as a result of removing UI elements
        # is separated by a space
        for child in description:
            add = HtmlProc.allProc(child)
            if not text.endswith(' ') and not add.startswith(' '):
                text += ' '
            text += add
        # remove starting and ending whitespace
        return text.strip()
    def getQuotes(self, id):
        '''
        Return string form for 2 quotes in an area with a certain ID, with any 
        special formatting removed
        '''
        # Get the text from the soup.
        text = self.getPlainText(id)
        # Separate out the quotations.
        parts = re.split(r'"|\u201C|\u201D', text)
        # Re-join the quotations with only straight quotation marks
        for i in range(1, len(parts), 2):
            parts[i] = '"' + parts[i] + '"'
        ret = [None, None]
        # The first quote is empty string + quote + text that follows the quote
        ret[0] = ''.join(parts[0:3]).strip()
        # The second quote is what remains
        ret[1] = ''.join(parts[3:]).strip()
        return ret
    def getUlToCol(self, ulId): #the year must be a number
        '''
        Process an unordered list and return it as an array
        '''
        courses = []
        # Get the ul from the soup using the id
        year = self.soup.find(id = ulId)
        list = year.ul
        # Append all non-empty list items to the array
        for li in list:
            courses.append(HtmlProc.allProc(li))
        courses = [course for course in courses if course.strip()]
        return courses
    def getPathwayName(self):
        '''
        The pathway name is the title of the page, based on SchoolLoop's special title
        ID system. If it is labeled for testing, ignore that label.
        '''
        return self.getPlainText('sl-cms2-page-title__h1').replace('-test', '')
    def getEntranceCriteria(self):
        '''
        Return the entrance criteria as a dictionary, where the name of the criterion
        is a key and the value of the criterion is the value
        '''
        criteria = {}
        # Get the table out of the soup
        table = self.soup.find(id = 'entrance-criteria')
        # Get string (without starting and ending whitespace) of the contents of each td.
        tds = [''.join(td.stripped_strings).strip() for td in list(table.find_all('td'))]
        # This means there is not table containing entrance criteria
        if not tds: return {}
        # Every even-numbered td is on the left of the table, so it is a criterion.
        keys = tds[::2]
        # Values are the odd-numbered tds.
        values = tds[1::2]
        # Fill in the dictionary
        for i, key in enumerate(keys):
            criteria[key] = values[i]
        return criteria
    def getVideoLink(self):
        '''
        Get a link to video if a source for the video is found, formatted as a 
        hyperlink in a spreadsheet.
        '''
        if self.soup.video: return '=HYPERLINK("' + self.soup.video.source['src'] + '")'
        return ''
    def getAll(self):
        # start out with an empty 2d array (representing this pathway's section in the spreadsheet)
        spreadsheet = [[None] * 6 for _ in range(25)]
        # Fill in with data about the pathway
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
        
        # Fill in the labels for the data (for the user to read only)
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

        # Create table of entrance criteria
        i = 0
        for key in entranceCriteria:
            spreadsheet[i + 17][2] = key
            spreadsheet[i + 17][3] = entranceCriteria[key]
            i += 1
        # Create lists of courses for each year
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
        
        # Create list of electives (in the 2D array)
        for i, elective in enumerate(popularElectives):
            if (i < 10):
                spreadsheet[i + 14][0] = elective
            else:
                spreadsheet[i - 10 + 14][1] = elective

        for i, quote in enumerate(studentQuotes):
            spreadsheet[i + 14][5] = quote
        for i, quote in enumerate(staffQuotes):
            spreadsheet[i + 17][5] = quote
        # Put the video link in the "cell" where it belongs
        spreadsheet[14][2] = videoLink

        return spreadsheet