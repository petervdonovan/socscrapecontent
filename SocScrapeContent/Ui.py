import requests
from Pathway import Pathway
from ClubsList import ClubsList
from XlsxMake import XlsxMake

class Ui:
    '''
    Class for getting all of the necessary data from the user (that cannot be found automatically)
    Calls other functions needed to make the workbooks.
    '''
    def __init__(self):
        '''
        Initialize with default data
        '''
        self.path = ''
        self.baseUrl = ''
        self.pathways = []
        self.clubs = []
        self.xlsxMake = None

    def getPath(self):
        '''
        Get path to where the newly created workbook from user (if path is not known already) 
        and return it
        '''
        if not self.path: self.path = input('File name: ')
        if not self.path.endswith('.xlsx'): self.path += '.xlsx'
        return self.path

    def getBaseUrl(self):
        '''
        Get the URL of the site from which information will be pulled (if URL is not known 
        already) and return it
        '''
        if not self.baseUrl: self.baseUrl = input('Base URL: ')
        if not self.baseUrl.endswith('/'): self.baseUrl += '/'
        return self.baseUrl

    def getPathways(self, suffix = ''):
        '''
        Use the URL and user-input pathway names to get a list of Pathway objects and return it
        '''
        self.getBaseUrl()
        response = input('Pathway name: ')
        if not response: return self.pathways
        site = requests.get(self.getBaseUrl() + response.replace(' ', '-') + suffix)
        if not site:
            print('No site was found for the specified pathway.')
            return self.getPathways(suffix=suffix)
        else:
            self.pathways.extend(Pathway(site.text).getAll())
            return self.getPathways(suffix=suffix)

    def getClubs(self, suffix = ''):
        '''
        Use the URL to return a ClubsList object.
        '''
        self.getBaseUrl()
        site = requests.get(self.getBaseUrl() + 'clubs' + suffix)
        self.clubs = ClubsList(site.text).getAll()
        return self.clubs

    def makeXlsx(self, sectionWidth, sectionHeight):
        '''
        Pass required pathways and clubs information to the XlsxMake object so that a workbook
        can be created.
        '''
        self.xlsxMake = XlsxMake(self.pathways, self.clubs)
        self.xlsxMake.make(sectionWidth, sectionHeight)

    def save(self):
        '''
        Save the XLSX workbook created by the XlsxMake object
        '''
        self.xlsxMake.save(self.getPath())