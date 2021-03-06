# coding=utf8
import re

from nltk import jaccard_distance
from datetime import datetime, timedelta

from data.api.content_db_connector import fetch_news_collection
from data.model.news import News, NewsMeta

from bs4 import BeautifulSoup


class DuplicateCheckResult:
    def __init__(self, is_duplicated: bool, reason="", news: News = None):
        self.is_duplicated: bool = is_duplicated
        self.reason: str = reason
        self.news: News = news

    def serialize(self):
        news_serialized = None
        if self.news is not None:
            news_serialized = self.news.serialize()
        return {
            "isDuplicated": self.is_duplicated,
            "reason": self.reason,
            "news": news_serialized
        }

    def __str__(self):
        return f"matched: {self.is_duplicated}\nreason: {self.reason}\nnews: {self.news}"


def diff_time_sec_abs(target: datetime, control: datetime):
    return abs((control - target).seconds)


def time_match(target: datetime, control: datetime) -> bool:
    if target > control:
        return False
    diff = diff_time_sec_abs(target, control)
    time_matches_range = diff < 3 * 60
    return time_matches_range


def title_match(title1, title2) -> bool:
    pass
    title_matches = title1 == title2
    return title_matches


def extract_usable_text(html):
    soup = BeautifulSoup(html, 'lxml')
    [s.extract() for s in soup('em')]  # read /rsc/README.md for more details
    [s.extract() for s in soup('a')]  # read /rsc/README.md for more details
    return soup.get_text()


def content_distance_check(html1, html2):
    txt1 = extract_usable_text(html1)
    txt2 = extract_usable_text(html2)
    txt1 = re.sub('\s+', ' ', txt1)
    txt2 = re.sub('\s+', ' ', txt2)
    # print(txt1)
    # print(txt2)
    distance = jaccard_distance(set(txt1), set(txt2))
    return distance


MAX_ACCEPTED_JACCARD_DISTANCE = 0.05


def content_match(html1, html2):
    distance = content_distance_check(html1, html2)
    # print(distance)
    return distance < MAX_ACCEPTED_JACCARD_DISTANCE


def check_duplicate(target: News, control: News) -> DuplicateCheckResult:
    """
    :param target: the new news to compare with existing news `control`
    :param control: the existing news to be compared with new news `target`
    :return:
    """
    # blocking same source
    source_matches = target.meta.source == control.meta.source
    if source_matches:
        return DuplicateCheckResult(is_duplicated=False,
                                    reason="news with same source, skipping process")

    # 0. check time diff
    time_matches = time_match(target.time, control.time)
    if not time_matches:
        return DuplicateCheckResult(is_duplicated=False,
                                    reason="time does not matches")

    # 1. check title match
    title_matches = title_match(target.title, control.title)
    if not title_matches:
        return DuplicateCheckResult(is_duplicated=False,
                                    reason="title does not matches")

    # 2. check content similarity with `jaccard_distance`
    content_matches = content_match(target.content, control.content)
    if not content_matches:
        return DuplicateCheckResult(is_duplicated=False,
                                    reason="content does not matches")

    return DuplicateCheckResult(is_duplicated=True,
                                reason="time, title, and content matched", news=control)


def check_duplicates(target: News, controls: [News]) -> DuplicateCheckResult:
    for c in controls:
        res = check_duplicate(target, c)
        if res.is_duplicated:
            return res
    return DuplicateCheckResult(is_duplicated=False,
                                reason="no duplicate news matched with control group",
                                news=None)


def check_duplicates_from_database(target: News, time_range_min=3) -> DuplicateCheckResult:
    newses = fetch_news_collection(time_from=target.time - timedelta(minutes=time_range_min), time_to=target.time + timedelta(minutes=time_range_min))
    print(len(newses))
    return check_duplicates(target, controls=newses)


def __test():
    set1 = {
        "__id": "5e7df8ec24aa9a00072724f9",
        "provider": "11",
        "__typename": "News",
        "originUrl": None,
        "id": "5e7df8ec24aa9a00072724f9",
        "meta": {
            "source": "EBEST",
            "__typename": "NewsMeta",
            "__id": "0",
            "__path": "News:5e7df8ec24aa9a00072724f9:meta=>NewsMeta:0"
        },
        "content": "남수단 한빛부대 11진 장병 에티오피아 전세기로 귀국길\n주바공항 이동…아디스아바바 공항 기착해 연료 넣고 출발\r\n전원 코로나19 검사 실시…'음성' 때도 2주간 자가 격리\r\n\r\n\n    (서울=연합뉴스) 김귀근 기자 = 아프리카 남수단에 파병된 한빛부대 11진 장병\r\n이 에티오피아 항공 전세기를 이용해 27일 귀국길에 올랐다.\r\n    국방부는 이날 한빛부대 11진 장병들이 전세기인 에티오피아 항공기를 이용해 \r\n저녁 9시50분(한국시간) 남수단을 출발해 내일 오전 11시10분께 인천공항에 도착할 \r\n예정이라고 밝혔다.\r\n    귀국하는 11진 장병은 200여명인 것으로 알려졌다.\r\n    국방부는 \"현 신종 코로나바이러스 감염증(코로나19) 상황으로 한빛부대 11, 12\r\n진 교대가 지연됨에 따라 11진 인원 중 주둔지 경계와 관리를 위한 필수 인원은 현\r\n지에 잔류하게 된다\"고 설명했다.\r\n    한빛부대원은 부대에서 주바 공항으로 이동해 에티오피아 항공기에 올랐다. 이 \r\n항공기는 에티오피아 수도 아디스아바바 공항에 잠시 기착해 연료를 넣은 후 인천공\r\n항으로 출발했다.\r\n    한빛부대 11진은 이달 초 12진과 임무를 교대할 예정이었지만, 남수단이 평화유\r\n지군 입국을 중지해달라고 요청하면서 교대를 하지 못했다.\r\n    국방부는 \"귀국하는 한빛부대 11진은 모두 코로나19 진단 검사를 받게 되며, 전\r\n원 음성으로 판별되더라도 2주간 자가 격리를 시행할 예정\"이라고 설명했다.\r\n    그러면서 \"인천공항 특별입국 절차에 따른 검역 과정에서 유증상자로 분류되는 \r\n경우 공항검사 시설에서 진단검사를 하고, 무증상자는 육군학생군사학교에서 예방적\r\n 차원의 군 자체 진단검사를 받게 된다\"고 전했다.\r\n    이 과정에서 확진자가 발생하면 전원 육군학생군사학교 내에 격리할 계획이다.\r\n    정부는 4·15 총선 전까지 12진이 출국해 11진이 모두 귀국할 수 있도록 남수단\r\n 등과 협의 중이다.\r\n    국방부는 \"한빛부대의 정상적 임무 수행을 위해 조속한 시일 내에 12진이 투입\r\n될 수 있도록 주둔국 및 유엔과의 협의 등 외교적 노력을 지속할 계획\"이라고 밝혔\r\n다.\r\n    이밖에 국방부는 \"현지에 남아 있는 한빛부대 임무 수행 여건 등을 고려해 복귀\r\n 및 잔류 인원수에 대해서는 보도를 자제해 주시기 바란다\"고 덧붙였다.\r\n    한빛부대는 유엔 평화유지군 소속으로 2013년부터 남수단에 파병됐다. 내전으로\r\n 황폐해진 남수단 지역의 도로, 비행장 등의 재건을 지원하고, 난민 보호와 식수·\r\n의료 등 인도적 지원을 하고 있다.\r\n    threek@yna.co.kr\r\n(끝)\n\n\r\n<a href=\"http://www.yonhapnews.co.kr/aboutus/4223030400.html\"><긴급속보 SMS 신청></a> <a href=\"http://yonhap.pumzine.com\"><포토 매거진></a> <a href=\"http://www.yonhapnews.co.kr/aboutus/4223030500.html\">< M-SPORTS ></a>\r\n<저작권자(c) 연합뉴스, 무단 전재-재배포 금지>",
        "time": "2020-03-27T22:00:23.000Z",
        "title": "남수단 한빛부대 11진 장병 에티오피아 전세기로 귀국길",
        "__path": "News:5e7df8ec24aa9a00072724f9"
    }
    set1 = News(**set1)

    set2 = {
        "__id": "5e7df92e24aa9a000727250b",
        "provider": "연합뉴스",
        "__typename": "News",
        "originUrl": "http://yna.kr/AKR20200327093000504?did=1195m",
        "id": "5e7df92e24aa9a000727250b",
        "meta": {
            "source": "NAVER",
            "__typename": "NewsMeta",
            "__id": "0",
            "__path": "News:5e7df92e24aa9a000727250b:meta=>NewsMeta:0"
        },
        "content": "<html><body><div class=\"_article_body_contents\" id=\"articleBodyContents\">\n\n\n\n\n\t\n\t주바공항 이동…아디스아바바 공항 기착해 연료 넣고 출발<br/><br/>전원 코로나19 검사 실시…'음성' 때도 2주간 자가 격리<br/><br/><span class=\"end_photo_org\"><img alt=\"\" src=\"https://imgnews.pstatic.net/image/001/2020/03/27/AKR20200327093000504_01_i_P4_20200327220112407.jpg?type=w647\"/><em class=\"img_desc\">윷놀이 즐기는 남수단 난민보호소 어린이들(서울=연합뉴스) 한빛부대는 남수단 난민보호소에 거주하는 어린이 200여 명과 UN 및 NGO 관계자를 초청, 한국의 대표명절인 추석을 소개하고 민속놀이 체험 등을 함께 했다고 밝혔다. 사진은 어린이들이 윷놀이를 즐기는 모습. 2019.9.12 [합동참모본부 제공. 재판매 및 DB금지]</em></span><br/><br/>    (서울=연합뉴스) 김귀근 기자 = 아프리카 남수단에 파병된 한빛부대 11진 장병이 에티오피아 항공 전세기를 이용해 27일 귀국길에 올랐다.<br/><br/>    국방부는 이날 한빛부대 11진 장병들이 전세기인 에티오피아 항공기를 이용해 저녁 9시50분(한국시간) 남수단을 출발해 내일 오전 11시10분께 인천공항에 도착할 예정이라고 밝혔다.<br/><br/>    귀국하는 11진 장병은 200여명인 것으로 알려졌다.<br/><br/>    국방부는 \"현 신종 코로나바이러스 감염증(코로나19) 상황으로 한빛부대 11, 12진 교대가 지연됨에 따라 11진 인원 중 주둔지 경계와 관리를 위한 필수 인원은 현지에 잔류하게 된다\"고 설명했다.<br/><br/>    한빛부대원은 부대에서 주바 공항으로 이동해 에티오피아 항공기에 올랐다. 이 항공기는 에티오피아 수도 아디스아바바 공항에 잠시 기착해 연료를 넣은 후 인천공항으로 출발했다.<br/><br/>    한빛부대 11진은 이달 초 12진과 임무를 교대할 예정이었지만, 남수단이 평화유지군 입국을 중지해달라고 요청하면서 교대를 하지 못했다.<br/><br/>    국방부는 \"귀국하는 한빛부대 11진은 모두 코로나19 진단 검사를 받게 되며, 전원 음성으로 판별되더라도 2주간 자가 격리를 시행할 예정\"이라고 설명했다.<br/><br/>    그러면서 \"인천공항 특별입국 절차에 따른 검역 과정에서 유증상자로 분류되는 경우 공항검사 시설에서 진단검사를 하고, 무증상자는 육군학생군사학교에서 예방적 차원의 군 자체 진단검사를 받게 된다\"고 전했다.<br/><br/>    이 과정에서 확진자가 발생하면 전원 육군학생군사학교 내에 격리할 계획이다.<br/><br/>    정부는 4·15 총선 전까지 12진이 출국해 11진이 모두 귀국할 수 있도록 남수단 등과 협의 중이다.<br/><br/>    국방부는 \"한빛부대의 정상적 임무 수행을 위해 조속한 시일 내에 12진이 투입될 수 있도록 주둔국 및 유엔과의 협의 등 외교적 노력을 지속할 계획\"이라고 밝혔다.<br/><br/>    이밖에 국방부는 \"현지에 남아 있는 한빛부대 임무 수행 여건 등을 고려해 복귀 및 잔류 인원수에 대해서는 보도를 자제해 주시기 바란다\"고 덧붙였다.<br/><br/>    한빛부대는 유엔 평화유지군 소속으로 2013년부터 남수단에 파병됐다. 내전으로 황폐해진 남수단 지역의 도로, 비행장 등의 재건을 지원하고, 난민 보호와 식수·의료 등 인도적 지원을 하고 있다.<br/><br/>    threek@yna.co.kr<br/><br/><span><a href=\"https://media.naver.com/channel/promotion.nhn?oid=001\" target=\"_blank\">▶코로나19 속보는 네이버 연합뉴스에서 [구독 클릭]</a><br/><a href=\"https://www.yna.co.kr/theme-list/factcheck?input=1195s\" target=\"_blank\">▶[팩트체크]'코로나19' 사실은 이렇습니다</a><a href=\"https://www.yna.co.kr/board/jebo/index?input=offer_naver\" style=\"margin-left:10px;\" target=\"_blank\">▶제보하기</a></span><br/><br/>\n\n</div></body></html>",
        "time": "2020-03-27T22:00:00.000Z",
        "title": "남수단 한빛부대 11진 장병 에티오피아 전세기로 귀국길",
        "__path": "News:5e7df92e24aa9a000727250b"
    }
    set2 = News(**set2)

    set3 = {
        "__id": "5e7dfcb724aa9a00072725ab",
        "provider": "MBC",
        "__typename": "News",
        "originUrl": "https://imnews.imbc.com/news/2020/politics/article/5681798_32626.html",
        "id": "5e7dfcb724aa9a00072725ab",
        "meta": {
            "source": "NAVER",
            "__typename": "NewsMeta",
            "__id": "0",
            "__path": "News:5e7dfcb724aa9a00072725ab:meta=>NewsMeta:0"
        },
        "content": "<html><body><div class=\"_article_body_contents\" id=\"articleBodyContents\">\n\n\n\n\n<span class=\"end_photo_org\"><img alt=\"\" src=\"https://imgnews.pstatic.net/image/214/2020/03/27/0001026431_001_20200327221612916.jpg?type=w647\"/></span>아프리카 남수단에 유엔 평화유지군 소속으로 파병된 한빛부대 11진 장병들이 귀국길에 올랐습니다.<br/><br/>국방부는 한빛부대 11진 장병들이 전세기인 에티오피아 항공기를 이용해 우리 시간 저녁 9시 50분 남수단을 출발했으며,내일 오전 11시 10분쯤 인천공항에 도착할 예정이라고 밝혔습니다.<br/><br/>국방부는 \"현 코로나19 상황으로 한빛부대 11,12진 교대가 지연됨에 따라 11진 인원 중 주둔지 경계와 관리를 위한 필수 인원은 현지에 잔류하게 된다\"고 설명했습니다.<br/><br/>국방부는 또 \"귀국하는 한빛부대 11진은 모두 코로나19 진단 검사를 받게 되며, 음성으로 판별되더라도 2주간 자가 격리를 시행할 예정\"이라고 밝혔습니다.<br/><br/>한빛부대 11진은 이달 초 12진과 임무를 교대할 예정이었지만 남수단이 평화유지군 입국을 중지해달라고 요청하면서 교대를 하지 못했습니다.<br/><br/>박선하 기자 (vividsun@mbc.co.kr)<br/><br/>[저작권자(c) MBC (https://imnews.imbc.com) 무단복제-재배포 금지]<br/><br/><a href=\"http://bit.ly/2rVONF0\" target=\"_blank\">▶ 네이버 홈에서 [MBC뉴스] 채널 구독하기</a><br/><br/><a href=\"https://imnews.imbc.com/original/mbig\" target=\"_blank\">▶ 새로움을 탐험하다. \"엠빅뉴스\"</a><br/><br/><a href=\"https://imnews.imbc.com/original/14f\" target=\"_blank\">▶ MBC 14층 사람들이 만든 뉴스 \"14F\"</a><br/><br/>Copyright(c) Since 1996, <a href=\"https://imnews.imbc.com\" target=\"_blank\">MBC</a>&amp;<a href=\"https://www.imbc.com/\" target=\"_blank\">iMBC</a> All rights reserved.\n\t\n</div></body></html>",
        "time": "2020-03-27T22:15:00.000Z",
        "title": "남수단 한빛부대 11진 장병 에티오피아 전세기로 귀국길",
        "__path": "News:5e7dfcb724aa9a00072725ab"
    }
    set3 = News(**set3)

    set4 = {
        "__id": "5e7dffb224aa9a0007272637",
        "provider": "SBS",
        "__typename": "News",
        "originUrl": "https://news.sbs.co.kr/news/endPage.do?news_id=N1005720710&plink=ORI&cooper=NAVER",
        "id": "5e7dffb224aa9a0007272637",
        "meta": {
            "source": "NAVER",
            "__typename": "NewsMeta",
            "__id": "0",
            "__path": "News:5e7dffb224aa9a0007272637:meta=>NewsMeta:0"
        },
        "content": "<html><body><div class=\"_article_body_contents\" id=\"articleBodyContents\">\n\n\n\n\n<span class=\"end_photo_org\"><img alt=\"\" src=\"https://imgnews.pstatic.net/image/055/2020/03/27/0000803881_001_20200327222907619.jpg?type=w647\"/></span><br/><div style=\"text-align: center;\"><span style=\"color:#808080\"><strong>▲ 윷놀이 즐기는 남수단 난민보호소 어린이들</strong></span></div><br/>아프리카 남수단에 파병된 한빛부대 11진 장병이 에티오피아 항공 전세기를 이용해 귀국길에 올랐습니다.<br/><br/>국방부는 한국 시간으로 오늘(27일) 밤 9시 50분쯤 한빛부대 11진이 남수단에서 출발해 내일 오전 11시 10분쯤 인천공항에 도착할 예정이라고 밝혔습니다.<br/><br/>국방부는 \"코로나19 상황으로 한빛부대 11, 12진 교대가 지연됨에 따라 11진 인원 중 주둔지 경계와 관리를 위한 필수 인원은 현지에 잔류하게 된다\"고 설명했습니다.<br/><br/>한빛부대 11진은 이달 초 12진과 임무를 교대할 예정이었지만, 남수단이 코로나19 확산 방지를 위해 평화유지군 입국을 중지해달라고 요청하면서 교대하지 못했습니다.<br/><br/>국방부는 \"귀국하는 한빛부대 11진은 모두 코로나19 진단 검사를 받게 되며, 전원 음성으로 판별되더라도 2주간 자가 격리를 시행할 예정\"이라고 설명했습니다.<br/><br/>인천공항 특별입국절차에 따른 검역 과정에서 유증상자로 분류되는 경우 공항 검사 시설에서 진단검사를 하고, 무증상자는 육군학생군사학교에서 예방적 차원의 군 자체 진단검사를 받게 됩니다.<br/><br/>이 과정에서 확진자가 발생하면 전원 육군학생군사학교에 격리 조치할 계획입니다.<br/><br/>국방부는 \"한빛부대의 정상적 임무 수행을 위해 조속한 시일 내에 12진이 투입될 수 있도록 주둔국과 유엔과의 협의 등 외교적 노력을 지속할 계획\"이라고 밝혔습니다.<br/><br/>한빛부대는 유엔 평화유지군 소속으로 2013년부터 남수단에 파병됐습니다.<br/><br/>내전으로 황폐해진 남수단 지역의 도로, 비행장 등의 재건을 지원하고, 난민 보호와 식수·의료 등 인도적 지원을 하고 있습니다.<br/><br/>(사진=합동참모본부 제공, 연합뉴스)<br/><br/>김학휘 기자(hwi@sbs.co.kr)<br/><br/><a href=\"https://news.sbs.co.kr/news/newsHotIssueList.do?tagId=10000051272&amp;plink=FOOT&amp;cooper=NAVER\">▶ 'n번방 · 박사방' 성착취 사건 파문</a><br/><a href=\"https://news.sbs.co.kr/news/newsHotIssueList.do?tagId=10000050973&amp;plink=FOOT&amp;cooper=NAVER\" target=\"_blank\">▶ 코로나19 속보 한눈에 보기</a><br/><a href=\"https://news.sbs.co.kr/news/newsPlusList.do?themeId=10000000257&amp;plink=FOOT&amp;cooper=NAVER\" target=\"_blank\">▶ VOTE KOREA 2020 온라인 갤러리</a><br/><br/>※ ⓒ SBS &amp; SBS Digital News Lab. : 무단복제 및 재배포 금지\n\t\n</div></body></html>",
        "time": "2020-03-27T22:28:00.000Z",
        "title": "남수단 한빛부대 11진 장병 에티오피아 전세기로 귀국길",
        "__path": "News:5e7dffb224aa9a0007272637"
    }
    set4 = News(**set4)

    sets = [set2, set3, set4]
    # res = check_duplicates(set1, sets)
    # print(set1.title)
    # print(res)

    # test db
    res = check_duplicates_from_database(target=set2)
    print(res)


if __name__ == "__main__":
    __test()
