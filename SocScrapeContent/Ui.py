import requests
from Pathway import Pathway
from XlsxMake import XlsxMake

class Ui:
    def __init__(self):
        self.path = ''
        self.baseUrl = ''
        self.pathways = []
        self.xlsxMake = None
        self.pathways = []

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
        if not response: return
        site = requests.get(self.getBaseUrl() + response.replace(' ', '-') + suffix)
        if not site:
            print('No site was found for the specified pathway.')
            return 1
        else:
            self.pathways.extend(Pathway(site.text).getAll())
        return self.pathways

    def makeXlsx(self, sectionWidth, sectionHeight):        
        self.xlsxMake = XlsxMake(self.pathways)
        self.xlsxMake.format(sectionWidth, sectionHeight)

    def save(self):
        self.xlsxMake.save(self.getPath())