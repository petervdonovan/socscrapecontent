import requests
from Pathway import Pathway
from ClubsList import ClubsList
from XlsxMake import XlsxMake

class Ui:
    def __init__(self):
        self.path = ''
        self.baseUrl = ''
        self.pathways = []
        self.clubs = []
        self.xlsxMake = None

    def getPath(self):
        if not self.path: self.path = input('File name: ')
        if not self.path.endswith('.xlsx'): self.path += '.xlsx'
        return self.path

    def getBaseUrl(self):
        if not self.baseUrl: self.baseUrl = input('Base URL: ')
        if not self.baseUrl.endswith('/'): self.baseUrl += '/'
        return self.baseUrl

    def getPathways(self, suffix = ''):
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
        self.getBaseUrl()
        site = requests.get(self.getBaseUrl() + 'clubs' + suffix)
        self.clubs = ClubsList(site.text).getAll()
        return self.clubs

    def makeXlsx(self, sectionWidth, sectionHeight):        
        self.xlsxMake = XlsxMake(self.pathways, self.clubs)
        self.xlsxMake.make(sectionWidth, sectionHeight)

    def save(self):
        self.xlsxMake.save(self.getPath())