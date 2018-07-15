from typing import List
from konlpy.tag import Twitter


class WordTokenizer:
    def __init__(self, txt):
        self.txt = txt

    def Tokenize(self, remove:List[str]=None) -> List[str]:
        result = []
        if remove is None:
            remove = ["Josa", "Eomi", "Punctuation"]

        # 형태소 분석
        twitter = Twitter()
        malist = twitter.pos(self.txt, norm=True, stem=True)
        # 필요한 어구만 대상으로 하기
        for word in malist:
            # 어미/조사/구두점 등은 대상에서 제외
            if not word[1] in remove:
                result.append(word[0])

        return result
