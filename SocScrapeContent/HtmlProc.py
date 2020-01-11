import bs4

class HtmlProc:
    @staticmethod
    def ulProc(soup):
        text = ''
        for li in soup.select('li'):
            text += '- ' + HtmlProc.allProc(li)
            text += '\n'
        return text
    @staticmethod
    def olProc(soup):
        text = ''
        num = 1
        for li in soup.select('li'):
            text += str(num) + '. ' + HtmlProc.allProc(li)
            text += '\n'
            num += 1
        return text
    @staticmethod
    def pProc(soup):
        text = ''
        for str in soup.children:
            text += HtmlProc.allProc(str)
        return text
    @staticmethod
    def allProc(soup):
        text = ''
        if (type(soup) is bs4.element.NavigableString):
            return text + soup
        else:
            for child in soup.children:
                if(type(child) is bs4.element.NavigableString):
                    text += child
                else:
                    if (child.name == 'ul'): text += HtmlProc.ulProc(child)
                    elif (child.name == 'ol'): text += HtmlProc.olProc(child)
                    else: text += HtmlProc.pProc(child)
        return text.strip()
