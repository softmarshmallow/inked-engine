import re
from typing import Tuple

boxTypes = [
    ('[', ']'),
    ('<', '>'),
]

# TODO Rename
def RemoveTitleBox(title:str)->(str, str):
    '''
    remove Title header
    eg. [fn★티비텔] ‘라이브’ 경찰 미화 논란에도 진정성 짙은 이야기 완성
    == > ‘라이브’ 경찰 미화 논란에도 진정성 짙은 이야기 완성
    '''

    filtered: str = title
    boxContent: str = None
    for boxType in boxTypes:
        startChar = boxType[0]
        endChar = boxType[1]
        if title[0] == startChar:
            regex = "\%s(.*?)\%s" % (startChar, endChar)
            try:
                boxContent = re.search(regex, title).group(1)
                filtered = filtered.replace(startChar, "").replace(endChar, "").replace(boxContent, '')
            except AttributeError as e:
                print("Exception", e)
                print("Exception", title)
            return filtered, boxContent

    return filtered, boxContent


if __name__ == "__main__":

    # TEST
    testList = [
        "[인사] 한국감정원",
        "[fn★티비텔] ‘라이브’ 경찰 미화 논란에도 진정성 짙은 이야기 완성",
        "[연합뉴스 이 시각 헤드라인] - 20:00",
        "[연합시론] 이 전 대통령 구속 여부, 법과 원칙 따르면 된다",
        "<부고>김진호 전 GSK 회장 장인상",
        "부정적 성격, 심장병 사망 위험 2배 ↑ <연구>",
        "크로아티아 국립공원서 한국인 관광객 숨져…실족 추정"
    ]

    for testSample in testList:
        result = RemoveTitleBox(testSample)
        # print("testSample", testSample, result)
        print(result)
