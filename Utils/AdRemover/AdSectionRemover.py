"""뉴스 안의 광고 영역을 제거합니다."""
import re
from typing import List

from bs4 import BeautifulSoup
from Api.LocalJsonDatabaseService import GetLocalNewsData
import pprint


class AdSectionRemover:
    def __init__(self, newsContent: str):
        self.newsContent = newsContent


suspiciousChars = ['▶', '♠', '☞', '※', ]
uniqueString = " _ESCAPE_REPLACEMENT_ "  # need space 앞뒤로 공백 있어야함.


def RemoveLinks(content: str) -> str:
    bs = BeautifulSoup(content, 'lxml')
    [s.extract() for s in bs('a')]
    # Remove Links

    return str(bs)


# TODO
def RemoveSuspiciousLine(content: str):

    # print("▶" in content)
    # m = re.match(r"(?<=▶)(.*\\w)(?=\\n)", content)
    # # print(m)
    # if m is not None:
    #     print("REGEX", m.group(1))

    return content



def GetAdLessContent(content: str) -> str:
    content = content.replace("\r", uniqueString)
    # content = content.replace("\n", "")
    content = RemoveLinks(content)
    content = RemoveSuspiciousLine(content)
    content = content.replace(uniqueString, "\r")
    return content


if __name__ == "__main__":

    samplesCount = 2000
    sampleNewsDataList = GetLocalNewsData(max=samplesCount, hasMaxValue=True)

    for sample in sampleNewsDataList:
        # print("Title : ", sample.newsTitle)
        # print("\n")
        # print("RawContent : ", sample.newsContent)
        bs = BeautifulSoup(sample.newsContent, "lxml")
        parsedText = bs.get_text()
        oneLineText = sample.newsContent.replace("\n", ' ')
        # print("BuiltText:", parsedText)
        # print("OneLineText", oneLineText)
        print("\n\nADS")
        RemoveLinks(oneLineText)
        print("=========\n\n\n")

    # print(sampleNewsData.newsContent)
#
#
# <a href="http://www.x1.co.kr/ad/?seq=2097&link=H" target="_blank">●[긴급] 3月 - 1등 주도주는 &#039;바로 이종목&#039; / 모멘텀 성장성 갖춘 종_ESCAPE_REPLACEMENT_
# 목 1선 바로확인</a>
#
#
# <a href="http://www.x1.co.kr/ad/?seq=2097&amp;link=H" target="_blank">●[긴급] 3月 - 1등 주도주는 '바로 이종목' / 모멘텀 성장성 갖춘 종_ESCAPE_REPLACEMENT_
# 목 1선 바로확인</a>
