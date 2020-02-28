import bs4
from bs4 import BeautifulSoup
from HtmlProc import HtmlProc
import re

class Club:
    '''
    Object representation of a Club at a school site. Stores information about the club.
    '''
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
        '''
        Return the information about the club as an array of the form in which it will be
        displayed in the spreadsheet.
        '''
        return [self.name, self.isTopClub, self.description, self.category, self.fieldTrips, self.scholarships, self.volunteerOpportunities, self.competitive]

class ClubsList(object):
    '''
    List of all clubs at a school site. Used to get information about clubs from a 
    soup of HTML and output it in a 2D array representation of a spreadsheet.
    '''
    def __init__(self, text):
        '''
        Store messy HTML as searchable soup.
        '''
        self.soup = BeautifulSoup(text, "html.parser")
    def getClubs(self, category, spreadsheet):
        '''
        '''
        # the id of the div containing all of the clubs of a certain category
        id = category.lower().replace(" ", "-") + "-clubs"
        # Each list item in this UL will correspond to 1 club.
        rawUl = self.soup.find(id=id)
        clubs = []
        # Iterate over the list items in the ul and store each as a Club.
        for li in [li for li in rawUl.contents if type(li) == bs4.element.Tag]:
            club = Club()
            club.category = category
            # if the club has field trips, scholarships, etc., its LI will contain a 
            # SPAN with the corresponding letter.
            club.fieldTrips = bool(li.select(".interns-f"))
            club.scholarships = bool(li.select(".interns-s"))
            club.volunteerOpportunities = bool(li.select(".interns-v"))
            club.competitive = bool(li.select(".interns-c"))
            # Everything in the LI with HTML tags stripped out is part of the club's name,
            # except for single letters in their own element, which are probably just 
            # FSVC icons in SPANs.
            for str in li.stripped_strings:
                if(len(str) > 1):
                    club.name += str
            clubs.append(club)
        # Put all the clubs found in the UL of the category in the 2D array 
        # representation of the spreadsheet.
        for club in clubs:
            spreadsheet.append(club.listify())
    def getProminentClubs(self, spreadsheet):
        '''
        Find all the clubs that appear in the Top Clubs section at the top of the SOC page.
        '''
        # Remove information from the soup that is raw, because it needs extra cooking.
        rawSection = self.soup.find(id="top-clubs")
        selectedRow = None # represents the row that is currently being added to in the "spreadsheet" (2D array)
        # Iterate over the DOM elements of the Top Clubs section.
        for element in rawSection.contents:
            # if the current element is a title (indicated by being bolded)
            if(type(element.find('strong')) == bs4.element.Tag or type(element.find('b')) == bs4.element.Tag):
                selectedRow = -1
                stopwords = ['and', 'the', 'la', 'el', 'club', 'f', 's', 'v', 'c']
                topClubTokens = self.relevantTokens(str(' '.join(element.strings)), stopwords)
                # Check for exact match in spreadsheet (2D list) so that 
                # info is correctly merged into the spreadsheet
                for (index, club) in enumerate(spreadsheet, 0):
                    clubTokens = self.relevantTokens(club[0], stopwords)
                    if(clubTokens == topClubTokens):
                        # The row corresponding to this Top Club has been found.
                        selectedRow = index
                        break
                # Try again to find a matching row where this club has already appeared, except with less strict matching conditions
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
        '''
        Simplify a piece of text and remove stopwords.
        '''
        return [token.lower() for token in text.split() if token.lower() not in stopwords]
    def getAll(self):
        '''
        Get the 2D array representation of the spreadsheet with information on all of the school's clubs.
        '''
        spreadsheet = [["Club Name", "Prominent club? (Choose up to 6 clubs to be placed in a Top Clubs category at the top of the clubs page)", "Description (1-2 sentences) for top clubs", "Category (Arts, Cultural, Volunteering & Advocacy, Social, STEM, or Other)", "Field Trips", "Scholarships", "Volunteer Opportunities", "Does the club participate in competitions?"]]
        self.getClubs("Arts", spreadsheet)
        self.getClubs("Cultural", spreadsheet)
        self.getClubs("Volunteering and Advocacy", spreadsheet)
        self.getClubs("Social", spreadsheet)
        self.getClubs("STEM", spreadsheet)
        self.getClubs("Other", spreadsheet)
        self.getProminentClubs(spreadsheet)
        return spreadsheet