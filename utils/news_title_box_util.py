import re
from typing import Tuple, List

boxTypes = [
    ('[', ']'),
    ('<', '>'),
]


class NewsBoxData:
    """
    뉴스속 테그 정보를 담는 데이터이다.
    eg. [특징주] , [속보], <사진> 등...
    """
    def __init__(self, original, charSet, fullBoxContent, innerBoxContent, fullBoxSpan, innerBoxSpan):
        self.original: str = original
        self.charSet = charSet # ('[', ']')
        self.startChar = charSet[0]
        self.endChar = charSet[1]
        self.fullBoxContent = fullBoxContent # [특징주]
        self.innerBoxContent = innerBoxContent # 특징주
        self.fullBoxSpan = fullBoxSpan # (0, 4)
        self.innerBoxSpan = innerBoxSpan # (1, 3)

    def __str__(self):
        return self.innerBoxContent

    def __repr__(self):
        return self.__str__()


def extract_boxes(txt: str) -> [NewsBoxData]:
    """
    remove Title header
    eg. [fn★티비텔] ‘라이브’ 경찰 미화 논란에도 진정성 짙은 이야기 완성
    == > fn★티비텔
    """
    boxDataList = []

    for boxType in boxTypes:
        startChar = boxType[0]
        endChar = boxType[1]

        if startChar in txt and endChar in txt:
            regex = "\%s(.*?)\%s" % (startChar, endChar)
            try:
                re_result = re.search(regex, txt)
                fullBoxContent = re_result.group(0)
                innerBoxContent = re_result.group(1)
                fbsi = txt.index(fullBoxContent)
                fullBoxSpan = (fbsi, fbsi+len(fullBoxContent))

                ibsi = txt.index(innerBoxContent)
                innerBoxSpan = (ibsi, ibsi + len(innerBoxContent))

                boxData = NewsBoxData(original=txt, charSet=boxType, innerBoxContent=innerBoxContent, fullBoxContent=fullBoxContent, fullBoxSpan=fullBoxSpan, innerBoxSpan=innerBoxSpan)
                boxDataList.append(boxData)
            except AttributeError as e:
                print("Exception", e)
                print("Exception", txt)

    return boxDataList


def remove_box(txt: str)->(str, str):
    """
    remove Title header
    eg. [fn★티비텔] ‘라이브’ 경찰 미화 논란에도 진정성 짙은 이야기 완성
    == > ‘라이브’ 경찰 미화 논란에도 진정성 짙은 이야기 완성
    """

    filtered: str = txt
    boxes: List[NewsBoxData] = extract_boxes(txt)
    for box in boxes:
        filtered = filtered.replace(box.fullBoxContent, "")

    return filtered, boxes



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
        result = extract_boxes(testSample)
        print("testSample", testSample, result)
        # print("find box:: ", result)
        #
        # result = remove_box(testSample)
        # print("remove box:: ", result)
