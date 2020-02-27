from bs4 import BeautifulSoup


def GetLinkLessContent(target, html=True):
    soup = BeautifulSoup(target, 'lxml')
    [s.extract() for s in soup('a')]
    if html: # return as html format
        return str(soup)
    else: # remove html tags
        return soup.getText()
