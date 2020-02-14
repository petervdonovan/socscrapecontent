import bs4
from bs4 import BeautifulSoup
from HtmlProc import HtmlProc
import re

class Club:
    def __init__(self):
        self.name = ""
        self.isTopClub = False
        self.description = ''
        self.category = ''
        self.fieldTrips = False
        self.scholarships = False
        self.volunteerOpportunities = False
        self.competitive = False
    def listify(self):
        return [self.name, self.isTopClub, self.description, self.category, self.fieldTrips, self.scholarships, self.volunteerOpportunities, self.competitive]

class ClubsList(object):
    def __init__(self, text):
        self.soup = BeautifulSoup(text, "html.parser")
    def getClubs(self, category, spreadsheet):
        id = category.lower().replace(" ", "-") + "-clubs"
        rawUl = self.soup.find(id=id)
        clubs = []
        for li in [li for li in rawUl.contents if type(li) == bs4.element.Tag]:
            club = Club()
            club.category = category
            club.fieldTrips = bool(li.select(".interns-f"))
            club.scholarships = bool(li.select(".interns-s"))
            club.volunteerOpportunities = bool(li.select(".interns-v"))
            club.competitive = bool(li.select(".interns-c"))
            
            for str in li.stripped_strings:
                if(len(str) > 1):
                    club.name += str
            clubs.append(club)
        for club in clubs:
            spreadsheet.append(club.listify())
    def getProminentClubs(self, spreadsheet):
        rawSection = self.soup.find(id="top-clubs")
        selectedRow = None
        for element in rawSection.contents:
            if(type(element.find('strong')) == bs4.element.Tag or type(element.find('b')) == bs4.element.Tag):
                selectedRow = -1
                stopwords = ['and', 'the', 'la', 'el', 'club', 'f', 's', 'v', 'c']
                topClubTokens = self.relevantTokens(str(' '.join(element.strings)), stopwords)
                #Check for exact match in spreadsheet (2D list) so that 
                #info is correctly merged into the spreadsheet
                for (index, club) in enumerate(spreadsheet, 0):
                    clubTokens = self.relevantTokens(club[0], stopwords)
                    if(clubTokens == topClubTokens):
                        selectedRow = index
                        break
                for (index, club) in enumerate(spreadsheet, 0):
                    clubTokens = self.relevantTokens(club[0], stopwords)
                    if( set(clubTokens).issubset(set(topClubTokens)) or set(topClubTokens).issubset(set(clubTokens)) ):
                        selectedRow = index
                        break
                #If merge with existing row is impossible, create new row
                if(selectedRow == -1):
                    spreadsheet.append(Club().listify())
                    spreadsheet[selectedRow][0] = ' '.join([string for string in element.stripped_strings])
                spreadsheet[selectedRow][1] = True;
            elif(selectedRow != None): spreadsheet[selectedRow][2] += HtmlProc.allProc(element)
            #clean up all row 2 entries
            for row in spreadsheet:
                row[2] = row[2].strip()
    @staticmethod
    def relevantTokens(text, stopwords):
        return [token.lower() for token in text.split() if token.lower() not in stopwords]
    def getAll(self):
        spreadsheet = [["Club Name", "Prominent club? (Choose up to 6 clubs to be placed in a Top Clubs category at the top of the clubs page)", "Description (1-2 sentences) for top clubs", "Category (Arts, Cultural, Volunteering & Advocacy, Social, STEM, or Other)", "Field Trips", "Scholarships", "Volunteer Opportunities", "Does the club participate in competitions?"]]
        self.getClubs("Arts", spreadsheet)
        self.getClubs("Cultural", spreadsheet)
        self.getClubs("Volunteering and Advocacy", spreadsheet)
        self.getClubs("Social", spreadsheet)
        self.getClubs("STEM", spreadsheet)
        self.getClubs("Other", spreadsheet)
        self.getProminentClubs(spreadsheet)
        return spreadsheet