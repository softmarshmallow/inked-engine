from typing import List
import json

from Api.NewsDataService import NewsDataService
from WordTokenizer.WordTokenizer import WordTokenizer


def FetchStopwords() -> List[str]:
    stopwords = []
    # stopwords list 1
    stopwords += json.loads(open("Stopwords/stopwords-ko.json").read())

    # stopwords list 2
    stopwords += open("Stopwords/ranks-stopwords-ko.txt").read().splitlines()

    # stopwords list 3
    stopwords += json.loads(open("Stopwords/custom-stopwords-ko.json").read())

    # Remove duplicates
    # stopwords = list(set(stopwords))

    return stopwords

# FIXME 인풋으로 리스트가 아닌 raw 텍스트 받을것.
class StopwordsRemover:

    def __init__(self, txtArr: List[str]):
        self.txtArr = txtArr

    def RemoveStopwords(self) -> List[str]:
        stopwords = FetchStopwords()
        targetTextArr = self.txtArr
        removalTextArr = stopwords

        # region method1
        # targetTextArr = set(self.txtArr)
        # removalTextArr = set(stopwords)
        # # Get new set with elements that are only in a but not in b
        # removedStopwordsTextArr = targetTextArr.difference(removalTextArr)
        # endregion

        # region method2
        removedStopwordsTextArr = [i for i in targetTextArr if i not in removalTextArr]
        # endregion

        return list(removedStopwordsTextArr)


if __name__ == "__main__":
    # print(len(FetchStopwords()))

    ns = NewsDataService().FetchNewsData(10)
    for n in ns:
        content = n.get_newsContent()
        tokens = WordTokenizer(content).Tokenize()
        swr = StopwordsRemover(tokens)
        print(content)
        print(tokens)
        print(swr.RemoveStopwords())
