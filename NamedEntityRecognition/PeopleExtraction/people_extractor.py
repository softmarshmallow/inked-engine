
from konlpy.tag import Mecab

from DataModels.models import PersonModel

mecab = Mecab()




people_dics = [
    "이건희",
    "이재용",
    "문제인",
    "안철수"
]



class PeopleExtractor:
    def __init__(self, txt):
        self.txt = txt

    def extract_peoples(self):
        extracted_peoples = []
        nouns = mecab.nouns(self.txt)
        for people in people_dics:
            if people in nouns:
                # FIXME
                person = PersonModel(id=None, name=people, relations=None)
                extracted_peoples.append(person)

        return extracted_peoples

