import codecs

import os
from konlpy.tag import Twitter
from datetime import datetime

# contentType:: (NewsTitle, NewsContent, Wiki)
def CreateUnpolishedCorpus(contentType:str = "Wiki")->str:
    print("CreateUnpolishedCorpus....")

    from Api.LocalJsonDatabaseService import GetLocalNewsData
    from Utils.HtmlLinkRemover import GetLinkLessContent

    outputFilePath = "Corpus/" + contentType + ".txt"
    f = open(outputFilePath, 'w')

    corpus = ""
    if contentType == "Wiki":
        pass
    if contentType == "NewsTitle" or contentType == "NewsContent":
        allNewsData = GetLocalNewsData(hasMaxValue=False)
        for newsData in allNewsData:
            if contentType == "NewsTitle":
                corpus += "\n" + newsData.newsTitle
            elif contentType == "NewsContent":
                corpus += "\n" + newsData.get_newsContent()

    f.write(corpus)
    f.close()

    return outputFilePath


def PolishCorpus(corpusFilePath:str, outputPath):
    print("PolishCorpus...")
    # Read Corpus file
    readFp = codecs.open(corpusFilePath, "r", encoding="utf-8")
    outputCorpusFile = outputPath
    writeFp = open(outputCorpusFile, "w", encoding="utf-8")


    # 형태소 분석 --- (※2)
    twitter = Twitter()
    i = 0
    # 텍스트를 한 줄씩 처리하기
    num_lines = sum(1 for line in open(corpusFilePath))
    startTime = datetime.now()
    while True:
        line = readFp.readline()
        if not line: break

        if i % 20000 == 0:
            percentage = i/num_lines * 100
            try: estimated = (num_lines/i) * (datetime.now() - startTime).seconds
            except ZeroDivisionError: estimated = 9999
            print("current - " + str(i), "...", round(percentage, 2), "% done", "...",  "remaining: ", round(estimated, 2))
        i += 1

        # 형태소 분석
        malist = twitter.pos(line, norm=True, stem=True)
        # 필요한 어구만 대상으로 하기
        r = []
        for word in malist:
            # 어미/조사/구두점 등은 대상에서 제외
            if not word[1] in ["Josa", "Eomi", "Punctuation"]:
                writeFp.write(word[0] + " ")
    writeFp.close()


if __name__ == "__main__":

    contentType = "NewsContent"
    rawCorpusPath = CreateUnpolishedCorpus(contentType=contentType)
    # rawCorpusPath = os.path.join(dirname, "Corpus/" + "NewsContent.txt")

    PolishCorpus(rawCorpusPath, "Corpus/" + contentType + ".corpus")
