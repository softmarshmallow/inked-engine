
from konlpy.tag import Mecab

from NamedEntityRecognition.AnnieHelper.annie_helper import extract_named_entity_dictionary
from data.local.models import PersonModel

mecab = Mecab()




people_dics = extract_named_entity_dictionary(NE_type="PS")


class PeopleExtractor:
    def __init__(self, txt):
        self.txt = txt

    def extract_peoples(self):
        extracted_peoples = []
        nouns = mecab.nouns(self.txt)
        for people in people_dics.keys():
            if people in nouns and len(people) >= 2:
                person = PersonModel(id=None, name=people, relations=None)
                extracted_peoples.append(person)
                # print(people)

        return extracted_peoples

