from datetime import datetime
from typing import List

from local.models import ExtractedInformation

time_regex_rules = []


def translate_time(content: str):
    translate_map = {
        # dddd
        "월요일": "Monday",
        "화요일": "Tuesday",
        "수요일": "Wednesday",
        "목요일": "Thursday",
        "토요일": "Saturday",
        "일요일": "Sunday",

    }

    for key in translate_map.keys():
        content = content.replace(key, translate_map[key])

    return content


def read_time_rule_dictionary():
    ...


class TimeExtractor:
    def __init__(self, content):
        self.content = content
        self.translated_content = translate_time(content)

    def extract_most_informative_times(self) -> List[ExtractedInformation]:
        # FIXME returns dummy data, need to update
        dummy = datetime(2018, 1, 10)
        extracted_time = ExtractedInformation(self.content, dummy, 0)
        return [extracted_time, extracted_time]

    def extract_time(self):
        ...


def test():
    from data.api import NewsDataService
    service = NewsDataService()
    l = service.FetchNewsData(1)
    content = l[0].get_news_content()
    e = TimeExtractor(content).extract_most_informative_times()
    print(e)


    # Load data
    # Loop data
    # Extract Time
    # Print Time
    ...


if __name__ == "__main__":
    test()
    translated = translate_time("월요일 9시에 회의일정.")
    print(translated)

