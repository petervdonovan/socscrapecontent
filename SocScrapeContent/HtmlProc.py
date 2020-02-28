import bs4

class HtmlProc:
    '''
    Class used for namespacing static methods.
    These methods are needed to represent HTML elements in BeautifulSoup soup
    as plain text for people unfamiliar with HTML.
    '''
    @staticmethod
    def ulProc(soup):
        '''
        Get an ul as a series of bullet points marked with dashes.
        '''
        text = ''
        for li in soup.select('li'):
            text += '- ' + HtmlProc.allProc(li)
            text += '\n'
        return text
    @staticmethod
    def olProc(soup):
        '''
        Get an ol as a series of numbered lines.
        '''
        text = ''
        num = 1
        for li in soup.select('li'):
            text += str(num) + '. ' + HtmlProc.allProc(li)
            text += '\n'
            num += 1
        return text
    @staticmethod
    def pProc(soup):
        '''
        Get the text of a p with any HTML elements represented as simple text
        '''
        text = ''
        for str in soup.children:
            text += HtmlProc.allProc(str)
        return text
    @staticmethod
    def allProc(soup):
        '''
        Generalized method for getting HTML as simple text.
        '''
        text = ''
        # If something is a NavigableString, it contains no elements and should look
        # fine if it is shown directly
        if (type(soup) is bs4.element.NavigableString):
            return text + soup
        else:
            for child in soup.children:
                # child does not have children
                if(type(child) is bs4.element.NavigableString):
                    text += child
                else:
                    # process uls as uls and ols as ols.
                    if (child.name == 'ul'): text += HtmlProc.ulProc(child)
                    elif (child.name == 'ol'): text += HtmlProc.olProc(child)
                    else: text += HtmlProc.pProc(child)
        return text.strip()
