from typing import List

def sent_tokenize(content: str, module='nltk') -> List[str]:

    if module == "nltk":
        from nltk import sent_tokenize
        return sent_tokenize(content)

    elif module == 'kkma':
        from konlpy.tag import Kkma
        kkma = Kkma()
        return kkma.sentences(content)