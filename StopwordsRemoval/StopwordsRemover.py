from typing import List
import json

import ahocorasick

import os

from data.api import NewsDataService
from WordTokenizer.WordTokenizer import WordTokenizer

dir_path = os.path.dirname(os.path.realpath(__file__))


def FetchStopwords() -> List[str]:
    stopwords = []
    # stopwords list 1
    path = os.path.join(dir_path, "rcs/stopwords-ko.json")
    stopwords += json.loads(open(path).read())

    # stopwords list 2
    path = os.path.join(dir_path, "rcs/custom-stopwords-ko.json")
    stopwords += json.loads(open(path).read())

    # Remove duplicates
    # stopwords = list(set(stopwords))

    return stopwords


# FIXME 인풋으로 리스트가 아닌 raw 텍스트 받을것.
class StopwordsRemover:

    def __init__(self, txtArr: List[str] = None, rawTxt: str = None):
        self.txtArr = txtArr
        self.rawTxt = rawTxt

    def RemoveStopwords(self) -> List[str]:
        if self.txtArr is None:
            raise ReferenceError("no parameter setted")
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

    def RemoveStopwordsFromContent(self) -> str:
        if self.rawTxt is None:
            raise ReferenceError("no parameter setted")

        auto = ahocorasick.Automaton()
        for stopword in FetchStopwords():
            auto.add_word(stopword, stopword)
        auto.make_automaton()

        for found in auto.iter(self.rawTxt):
            print(found)
#             TODO Add remove logic


if __name__ == "__main__":
    # print(len(FetchStopwords()))

    ns = NewsDataService().FetchNewsData(10)
    for n in ns:
        content = n.get_news_content()
        tokens = WordTokenizer(content).Tokenize()
        swr = StopwordsRemover(tokens)
        print(content)
        print(tokens)
        print(swr.RemoveStopwords())
