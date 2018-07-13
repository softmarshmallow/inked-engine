from konlpy.tag import Kkma, Twitter
from konlpy.utils import pprint
import nltk
from Api import FirebaseService as firService
from Api import LocalJsonDatabaseService as localService
from Utils.HtmlLinkRemover import GetLinkLessContent

# Font Settings
from matplotlib import font_manager, rc

fontFrame = "/Library/Fonts/AppleGothic.ttf"
fontName = font_manager.FontProperties(fontFrame).get_name()
rc('font', family=fontFrame)
#

kkma = Kkma()
posTagger = Twitter()

newsDataList = localService.GetLocalNewsData(max=10, hasMaxValue=True)
newsDataList = newsDataList[:1]

for newsData in newsDataList:

    linkLessContent = GetLinkLessContent(newsData.newsContent)
    print(linkLessContent)

    nouns = kkma.nouns(linkLessContent)
    freq = nltk.FreqDist(nouns)

    for key, val in freq.items():
        # print(str(key) + ':' + str(val))
        pass

    freq.plot(20, cumulative=False)
