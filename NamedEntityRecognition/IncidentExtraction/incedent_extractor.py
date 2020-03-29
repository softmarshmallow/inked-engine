from konlpy.tag import Mecab

from data.local.models import IncidentModel

mecab = Mecab()

incident_list = ["계약", "수주", "공급", "인수합병", "M&A"]


class IncidentExtractor:
    def __init__(self, txt: str):
        self.txt: str = txt

    def extract_incidents(self) -> [IncidentModel]:
        contain_incidents = []
        nouns = mecab.nouns(self.txt)
        for incident in incident_list:
            if incident in nouns:
                incident = IncidentModel(
                    name=incident,
                    type=incident,
                    relation=None
                )
                contain_incidents.append(incident)

        return contain_incidents


def extract_incidents(content:str):
    ...

