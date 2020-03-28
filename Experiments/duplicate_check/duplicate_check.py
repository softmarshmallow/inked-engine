# coding=utf8
import re

from nltk import jaccard_distance, word_tokenize, ngrams
from datetime import datetime
import arrow

from bs4 import BeautifulSoup

set1 = {
    "provider": "11",
    "originUrl": None,
    "meta": {
        "source": "EBEST",
    },
    "content": "'집단감염 우려' 만민중앙교회 관련 6명 확진…지하 기도실 폐쇄(종합2보)\n교회 폐쇄하고 임시 선별진료소 설치…교인 200여명 검사 진행중\r\n\r\n    (서울=연합뉴스) 임화섭 김지헌 기자 = 서울 구로구 구로3동에 있는 '만민중앙\r\n교회'와 관련된 확진자가 잇따라 확인되고 있다고 복수의 방역당국 관계자들이 전했\r\n다.\r\n    방역당국은 조사 과정에서 동작구 목사 사택 인근에 있는 교인들 거주 빌라 지\r\n하에서 기도실을 발견하고 폐쇄 조치를 내렸다. 이 교회는 공식적으로 3월 6일부터 \r\n예배를 온라인으로 전환했다.\r\n    방역당국은 또 사택과 빌라 근처에 컨테이너로 설치된 사무실에 교인들이 드나\r\n든 사실도 확인하고 교회나 사택 운영과의 연관성을 조사하면서 접촉자를 파악 중이\r\n다.\r\n    동작구는 이 빌라에 사는 만민중앙교회 교인 17명의 명단을 교회 장로로부터 넘\r\n겨받아 검사를 실시했다. 이 중 15명은 음성으로 판정됐고 2명의 검사 결과는 아직 \r\n나오지 않았다.\r\n    구로구는 접촉자 240여명을 파악했으며, 이 중 교직자 33명은 26일 오후 구로구\r\n 선별진료소에서 검사를 받았다. 이 중 구로구 외 거주자 3명이 확진됐고 30명은 음\r\n성 판정을 받았다. 구로구는 27일 오후 구로3동 만민중앙교회 앞에 임시 선별진료소\r\n를 설치해 나머지 교인 200여명이 검사를 받도록 했으며, 오후 6시까지 198명을 검\r\n사했다.\r\n\n    다만 이 중에는 접촉자로 분류되지 않아 원래 대상자가 아니었는데 검사를 받은\r\n 인원도 포함됐을 수 있어 정확한 전수검사 진행상황은 즉각 파악되지 않고 있다.\r\n    구로구청은 27일 만민중앙교회를 일단 폐쇄했으며, 검사 결과에 따라 폐쇄 기간\r\n을 조정할 예정이다.\r\n    구로구청이 파악한 타구 거주 확진자 3명 중 2명은 동작구에 있는 만민중앙교회\r\n 사무실에서 금천구 6번 확진자와 함께 근무하는 직원이며 다른 1명은 교회 교직자\r\n다.\r\n    서울 자치구들과 방역당국의 발표 내용에 따르면 그동안 만민중앙교회 관련 감\r\n염으로 의심되는 환자가 최소 4명 공개됐다.\r\n    금천구 독산3동에 실거주하는 55세 남성(금천구 8번 확진자)은 27일 확진 통보\r\n를 받았다. 이 환자의 주민등록상 주소는 경기 광명시이지만 실거주지는 금천구 독\r\n산3동이고, 검사는 26일 구로구 선별진료소에서 받았다.\r\n    이 환자의 직장은 구로구 구로3동에 있는 만민중앙교회다.\r\n    이 환자는 금천구 6번 환자(독산1동 거주, 40세 남성, 25일 확진)의 직장 동료\r\n인 것으로 알려졌다.\r\n    방역당국은 금천구 6번 환자가 동선으로 보아 만민중앙교회와 관련이 있고 이 \r\n교회에서 일을 하고 있을 공산이 큰 것으로 보고 있다.\r\n    금천구 6번 환자는 아내인 7번 환자(독산1동 거주, 33세 여성, 26일 확진), 장\r\n모인 구로구 24번 환자(가리봉동 거주, 58세 여성, 26일 확진)와 접촉해 감염시킨 \r\n것으로 추정된다.\r\n    영등포구 대림3동에 사는 40대 남성(영등포구 21번 환자)은 27일 확진됐다. 그\r\n는 25일에 발열, 기침, 인후통 등 증상이 있었고 26일 구로구보건소에서 검사를 받\r\n았다. 이 환자는 만민중앙교회의 동작구 컨테이너 사무실에서 근무하는 사무직원이\r\n다.\r\n    이런 내용을 종합하면 지금까지 각 자치구에 파악된 만민중앙교회 관련 확진자\r\n는 가족 등 파생 감염을 합해 6명 이상인 것으로 추정된다.\r\n    방역당국은 금천구 7번 환자가 가산디지털단지 SK트윈타워 5층에 있는 직장 사\r\n무실에서 접촉한 동료 11명을 파악해 일단 자가격리 조치했다.\r\n    limhwasop@yna.co.kr, jk@yna.co.kr\r\n(끝)\n\n\r\n<a href=\"http://www.yonhapnews.co.kr/aboutus/4223030400.html\"><긴급속보 SMS 신청></a> <a href=\"http://yonhap.pumzine.com\"><포토 매거진></a> <a href=\"http://www.yonhapnews.co.kr/aboutus/4223030500.html\">< M-SPORTS ></a>\r\n<저작권자(c) 연합뉴스, 무단 전재-재배포 금지>",
    "time": "2020-03-27T22:00:44.000Z",
    "title": "'집단감염 우려' 만민중앙교회 관련 6명 확진…지하 기도실 폐쇄(종합2보)",
}
set2 = {
    "provider": "연합뉴스",
    "originUrl": "http://yna.kr/AKR20200327172652004?did=1195m",
    "meta": {
        "source": "NAVER",
    },
    "content": "<html><body><div class=\"_article_body_contents\" id=\"articleBodyContents\">\n\n\n\n\n\t\n\t교회 폐쇄하고 임시 선별진료소 설치…교인 200여명 검사 진행중<br/><br/>(서울=연합뉴스) 임화섭 김지헌 기자 = 서울 구로구 구로3동에 있는 '만민중앙교회'와 관련된 확진자가 잇따라 확인되고 있다고 복수의 방역당국 관계자들이 전했다.<br/><br/>    방역당국은 조사 과정에서 동작구 목사 사택 인근에 있는 교인들 거주 빌라 지하에서 기도실을 발견하고 폐쇄 조치를 내렸다. 이 교회는 공식적으로 3월 6일부터 예배를 온라인으로 전환했다.<br/><br/>    방역당국은 또 사택과 빌라 근처에 컨테이너로 설치된 사무실에 교인들이 드나든 사실도 확인하고 교회나 사택 운영과의 연관성을 조사하면서 접촉자를 파악 중이다.<br/><br/>    동작구는 이 빌라에 사는 만민중앙교회 교인 17명의 명단을 교회 장로로부터 넘겨받아 검사를 실시했다. 이 중 15명은 음성으로 판정됐고 2명의 검사 결과는 아직 나오지 않았다.<br/><br/>    구로구는 접촉자 240여명을 파악했으며, 이 중 교직자 33명은 26일 오후 구로구 선별진료소에서 검사를 받았다. 이 중 구로구 외 거주자 3명이 확진됐고 30명은 음성 판정을 받았다. 구로구는 27일 오후 구로3동 만민중앙교회 앞에 임시 선별진료소를 설치해 나머지 교인 200여명이 검사를 받도록 했으며, 오후 6시까지 198명을 검사했다.<br/><br/><span class=\"end_photo_org\"><img alt=\"\" src=\"https://imgnews.pstatic.net/image/001/2020/03/27/PCM20200316000103990_P4_20200327220113912.jpg?type=w647\"/><em class=\"img_desc\">만민중앙교회 관련 6명 확진… (PG)[장현경 제작] 사진합성·일러스트</em></span><br/><br/>    다만 이 중에는 접촉자로 분류되지 않아 원래 대상자가 아니었는데 검사를 받은 인원도 포함됐을 수 있어 정확한 전수검사 진행상황은 즉각 파악되지 않고 있다.<br/><br/>    구로구청은 27일 만민중앙교회를 일단 폐쇄했으며, 검사 결과에 따라 폐쇄 기간을 조정할 예정이다.<br/><br/>    구로구청이 파악한 타구 거주 확진자 3명 중 2명은 동작구에 있는 만민중앙교회 사무실에서 금천구 6번 확진자와 함께 근무하는 직원이며 다른 1명은 교회 교직자다.<br/><br/>    서울 자치구들과 방역당국의 발표 내용에 따르면 그동안 만민중앙교회 관련 감염으로 의심되는 환자가 최소 4명 공개됐다.<br/><br/>    금천구 독산3동에 실거주하는 55세 남성(금천구 8번 확진자)은 27일 확진 통보를 받았다. 이 환자의 주민등록상 주소는 경기 광명시이지만 실거주지는 금천구 독산3동이고, 검사는 26일 구로구 선별진료소에서 받았다.<br/><br/>    이 환자의 직장은 구로구 구로3동에 있는 만민중앙교회다.<br/><br/>    이 환자는 금천구 6번 환자(독산1동 거주, 40세 남성, 25일 확진)의 직장 동료인 것으로 알려졌다.<br/><br/>    방역당국은 금천구 6번 환자가 동선으로 보아 만민중앙교회와 관련이 있고 이 교회에서 일을 하고 있을 공산이 큰 것으로 보고 있다.<br/><br/>    금천구 6번 환자는 아내인 7번 환자(독산1동 거주, 33세 여성, 26일 확진), 장모인 구로구 24번 환자(가리봉동 거주, 58세 여성, 26일 확진)와 접촉해 감염시킨 것으로 추정된다.<br/><br/>    영등포구 대림3동에 사는 40대 남성(영등포구 21번 환자)은 27일 확진됐다. 그는 25일에 발열, 기침, 인후통 등 증상이 있었고 26일 구로구보건소에서 검사를 받았다. 이 환자는 만민중앙교회의 동작구 컨테이너 사무실에서 근무하는 사무직원이다.<br/><br/>    이런 내용을 종합하면 지금까지 각 자치구에 파악된 만민중앙교회 관련 확진자는 가족 등 파생 감염을 합해 6명 이상인 것으로 추정된다.<br/><br/>    방역당국은 금천구 7번 환자가 가산디지털단지 SK트윈타워 5층에 있는 직장 사무실에서 접촉한 동료 11명을 파악해 일단 자가격리 조치했다.<br/><br/>    limhwasop@yna.co.kr, jk@yna.co.kr<br/><br/><span><a href=\"https://media.naver.com/channel/promotion.nhn?oid=001\" target=\"_blank\">▶코로나19 속보는 네이버 연합뉴스에서 [구독 클릭]</a><br/><a href=\"https://www.yna.co.kr/theme-list/factcheck?input=1195s\" target=\"_blank\">▶[팩트체크]'코로나19' 사실은 이렇습니다</a><a href=\"https://www.yna.co.kr/board/jebo/index?input=offer_naver\" style=\"margin-left:10px;\" target=\"_blank\">▶제보하기</a></span><br/><br/>\n\n</div></body></html>",
    "time": "2020-03-27T22:00:00.000Z",
    "title": "'집단감염 우려' 만민중앙교회 관련 6명 확진…지하 기도실 폐쇄(종합2보)",
}

wrong_set_example = {
    "provider": "매일경제",
    "originUrl": "http://news.mk.co.kr/newsRead.php?no=321470&year=2020",
    "meta": {
        "source": "NAVER",
    },
    "content": "<html><body><div class=\"_article_body_contents\" id=\"articleBodyContents\">\n\n\n\n\n<span class=\"end_photo_org\"><img alt=\"\" src=\"https://imgnews.pstatic.net/image/009/2020/03/27/0004545961_001_20200327220203155.jpg?type=w647\"/><em class=\"img_desc\">[사진출처 = 연합뉴스]</em></span> 토요일인 28일은 차고 건조한 공기가 유입되면서 일부 지역은 아침 최저기온이 영하로 내려가는 등 꽃샘추위가 오겠다. <br/><br/>특히 경기 동부와 강원 영서는 기온이 영하로 내려가는 곳이 있고 강원 산지 도로는 눈이 내리는 곳도 있어 농작물 냉해 피해나 교통안전에 유의해야 한다.<br/><br/>아침 최저 기온은 －2∼9도, 낮 최고기온은 9∼14도로 전날(8∼16도·9∼27도)과 비교해 기온이 크게 내려가 쌀쌀하겠다.<br/><br/>미세먼지 등급은 대기확산이 원활해 전국이 '좋음'∼'보통'으로 예상된다.<br/><br/>중부지방은 대체로 맑고 남부지방은 오전에 구름 많다가 오후부터 맑아지겠다. 제주도는 낮에 비가 조금 오겠다. 예상 강수량은 5㎜ 내외다.<br/><br/>[디지털뉴스국]<br/><br/><a href=\"https://media.naver.com/channel/promotion.nhn?oid=009\" target=\"_blank\">▶네이버 메인에서 '매일경제'를 받아보세요</a><br/><a href=\"https://member.mk.co.kr/newsletter/info.php?utm_source=naver&amp;utm_medium=promotion&amp;utm_campaign=mkdk\" target=\"_blank\">▶뉴스레터 '매콤달콤' 구독</a> <a href=\"https://www.mk.co.kr/?utm_source=naver&amp;utm_medium=promotion&amp;utm_campaign=mkmain\" target=\"_blank\">▶'매일경제' 바로가기</a><br/>[ⓒ 매일경제 &amp; mk.co.kr, 무단전재 및 재배포 금지]\n\t\n</div></body></html>",
    "time": "2020-03-27T22:02:00.000Z",
    "title": "맑고 쌀쌀한 토요일…경기동부·강원영서 아침 영하",
}


def diff_time_sec_abs(first: datetime, second: datetime):
    return abs((first - second).seconds)


def time_match(time1, time2) -> bool:
    diff = diff_time_sec_abs(time1, time2)
    time_matches_range = diff < 3 * 60
    return time_matches_range


def title_match(title1, title2) -> bool:
    pass
    title_matches = title1 == title2
    return title_matches


def extract_usable_text(html):
    soup = BeautifulSoup(html, 'lxml')
    [s.extract() for s in soup('em')] # read /rsc/README.md for more details
    [s.extract() for s in soup('a')] # read /rsc/README.md for more details
    return soup.get_text()


def content_distance_check(html1, html2):
    txt1 = extract_usable_text(html1)
    txt2 = extract_usable_text(html2)
    txt1 = re.sub('\s+',' ',txt1)
    txt2 = re.sub('\s+',' ',txt2)
    print(txt1)
    print(txt2)
    distance = jaccard_distance(set(txt1), set(txt2))
    return distance


MAX_ACCEPTED_JACCARD_DISTANCE = 0.05


def content_match(html1, html2):
    distance = content_distance_check(html1, html2)
    print(distance)
    return distance < MAX_ACCEPTED_JACCARD_DISTANCE


def check_duplicate(set1, set2) -> (bool, str):
    # 0. check time diff
    # time_matches = time_match(arrow.get(set1["time"]).datetime, arrow.get(set2["time"]).datetime)
    # if not time_matches:
    #     return False, "time does not matches"

    # 1. check title match
    title_matches = title_match(set1["title"], set2["title"])
    if not title_matches:
        return False, "title does not matches"

    # 2. check content similarity with `jaccard_distance`
    content_matches = content_match(set1["content"], set2["content"])
    if not content_matches:
        return False, "content does not matches"

    return True, "time, title, and content matched"


def __test():
    set1 = {
        "provider": "11",
        "originUrl": None,
        "meta": {
            "source": "EBEST",
        },
        "content": "이탈리아도 말라리아·에이즈 치료제 사용 승인\n    \r\n\n    \r\n    (로마=연합뉴스) 전성훈 특파원 = 이탈리아 당국이 신종 코로나바이러스 감염증\r\n(코로나19) 환자에 대한 말라리아 및 에이즈 치료제 투약을 승인했다.\r\n    27일(현지시간) 현지 언론에 따르면 이탈리아 당국은 말라리아 치료제인 클로로\r\n퀸과 클로로퀸 계열 유사 약물인 하이드록시클로로퀸을 코로나19 환자 치료에 사용\r\n하도록 허가했다.\r\n    미국 식품의약국(FDA)의 승인을 받은 에이즈 치료제 성분인 로피나비르와 리토\r\n나비르 사용도 가능해졌다.\r\n    코로나19 환자에 해당 치료제를 사용할 경우 전액 의료보험 혜택이 적용된다.\r\n    26일 기준 이탈리아의 코로나19 누적 확진자 수는 8만539명, 누적 사망자 수는 \r\n8천165명이다. \r\n    누적 사망자 규모는 세계 최대이며, 누적 확진자도 현재의 증가 추이라면 미국(\r\n8만5천162명)과 중국(8만1천340명)을 넘어 세계 최대를 기록할 가능성이 크다. \r\n    lucho@yna.co.kr\r\n(끝)\n\n\r\n<a href=\"http://www.yonhapnews.co.kr/aboutus/4223030400.html\"><긴급속보 SMS 신청></a> <a href=\"http://yonhap.pumzine.com\"><포토 매거진></a> <a href=\"http://www.yonhapnews.co.kr/aboutus/4223030500.html\">< M-SPORTS ></a>\r\n<저작권자(c) 연합뉴스, 무단 전재-재배포 금지>",
        "time": "2020-03-27T22:26:36.000Z",
        "title": "이탈리아도 말라리아·에이즈 치료제 사용 승인",
    }
    set2 = {
               "provider": "연합뉴스",
               "originUrl": "http://yna.kr/AKR20200327191900109?did=1195m",
               "meta": {
                   "source": "NAVER",
               },
               "content": "<html><body><div class=\"_article_body_contents\" id=\"articleBodyContents\">\n\n\n\n\n<span class=\"end_photo_org\"><img alt=\"\" src=\"https://imgnews.pstatic.net/image/001/2020/03/27/PYH2020022723170034000_P4_20200327222710845.jpg?type=w647\"/><em class=\"img_desc\">\"코로나19 치료 효과\" 클로로퀸 생산 재개한 중국 제약사(난퉁 EPA=연합뉴스) 중국 장쑤성 난퉁에 있는 한 제약회사가 15년만에 말라리아 약제인 클로로퀸 포스페이트 생산을 재개한 가운데 직원들이 27일 해당 약품을 포장하고 있다. 중국 언론에 따르면 클로로퀸은 신종 코로나바이러스 감염증(코로나19)을 치료하는 데 어느 정도 효능을 보인 것으로 알려졌다. jsmoon@yna.co.kr</em></span><br/><br/>(로마=연합뉴스) 전성훈 특파원 = 이탈리아 당국이 신종 코로나바이러스 감염증(코로나19) 환자에 대한 말라리아 및 에이즈 치료제 투약을 승인했다.<br/><br/>    27일(현지시간) 현지 언론에 따르면 이탈리아 당국은 말라리아 치료제인 클로로퀸과 클로로퀸 계열 유사 약물인 하이드록시클로로퀸을 코로나19 환자 치료에 사용하도록 허가했다.<br/><br/>    미국 식품의약국(FDA)의 승인을 받은 에이즈 치료제 성분인 로피나비르와 리토나비르 사용도 가능해졌다.<br/><br/>    코로나19 환자에 해당 치료제를 사용할 경우 전액 의료보험 혜택이 적용된다.<br/><br/>    26일 기준 이탈리아의 코로나19 누적 확진자 수는 8만539명, 누적 사망자 수는 8천165명이다. <br/><br/>    누적 사망자 규모는 세계 최대이며, 누적 확진자도 현재의 증가 추이라면 미국(8만5천162명)과 중국(8만1천340명)을 넘어 세계 최대를 기록할 가능성이 크다. <br/><br/>    lucho@yna.co.kr<br/><br/><span><a href=\"https://media.naver.com/channel/promotion.nhn?oid=001\" target=\"_blank\">▶코로나19 속보는 네이버 연합뉴스에서 [구독 클릭]</a><br/><a href=\"https://www.yna.co.kr/theme-list/factcheck?input=1195s\" target=\"_blank\">▶[팩트체크]'코로나19' 사실은 이렇습니다</a><a href=\"https://www.yna.co.kr/board/jebo/index?input=offer_naver\" style=\"margin-left:10px;\" target=\"_blank\">▶제보하기</a></span><br/><br/>\n\n</div></body></html>",
               "time": "2020-03-27T22:26:00.000Z",
               "title": "이탈리아도 말라리아·에이즈 치료제 사용 승인",
           }
    set3 = {
        "provider": "SBS",
        "originUrl": "https://news.sbs.co.kr/news/endPage.do?news_id=N1005720713&plink=ORI&cooper=NAVER",
        "meta": {
            "source": "NAVER",
        },
        "content": "<html><body><div class=\"_article_body_contents\" id=\"articleBodyContents\">\n\n\n\n\n<span class=\"end_photo_org\"><img alt=\"\" src=\"https://imgnews.pstatic.net/image/055/2020/03/27/0000803884_001_20200327224207483.jpg?type=w647\"/></span><br/>이탈리아 당국이 코로나19 환자에 대한 말라리아 및 에이즈 치료제 투약을 승인했습니다.<br/><br/>이탈리아 당국은 말라리아 치료제인 클로로퀸과 클로로퀸 계열 유사 약물인 하이드록시클로로퀸을 코로나19 환자 치료에 사용하도록 허가했습니다.<br/><br/>미국 식품의약국 FDA의 승인을 받은 에이즈 치료제 성분인 로피나비르와 리토나비르 사용도 가능해졌습니다.<br/><br/>코로나19 환자에 해당 치료제를 사용할 경우 전액 의료보험 혜택이 적용됩니다.<br/><br/>현지시간으로 어제 기준 이탈리아의 코로나19 누적 확진자 수는 8만 539명, 누적 사망자 수는 8천165명입니다.<br/><br/>누적 사망자 규모는 세계 최대이며, 누적 확진자도 현재의 증가 추이라면 미국과 중국을 넘어 세계 최대를 기록할 가능성이 큽니다.<br/><br/><span class=\"end_photo_org\"><img alt=\"\" src=\"https://imgnews.pstatic.net/image/055/2020/03/27/0000803884_002_20200327224207515.jpg?type=w647\"/></span><br/><br/>안서현 기자(ash@sbs.co.kr)<br/><br/><a href=\"https://news.sbs.co.kr/news/newsHotIssueList.do?tagId=10000051272&amp;plink=FOOT&amp;cooper=NAVER\">▶ 'n번방 · 박사방' 성착취 사건 파문</a><br/><a href=\"https://news.sbs.co.kr/news/newsHotIssueList.do?tagId=10000050973&amp;plink=FOOT&amp;cooper=NAVER\" target=\"_blank\">▶ 코로나19 속보 한눈에 보기</a><br/><a href=\"https://news.sbs.co.kr/news/newsPlusList.do?themeId=10000000257&amp;plink=FOOT&amp;cooper=NAVER\" target=\"_blank\">▶ VOTE KOREA 2020 온라인 갤러리</a><br/><br/>※ ⓒ SBS &amp; SBS Digital News Lab. : 무단복제 및 재배포 금지\n\t\n</div></body></html>",
        "time": "2020-03-27T22:41:00.000Z",
        "title": "이탈리아도 말라리아·에이즈 치료제 사용 승인",
    }

    is_duplicate_1_2 = check_duplicate(set1, set2)
    print(is_duplicate_1_2)

    is_duplicate_1_3 = check_duplicate(set1, set3)
    print(is_duplicate_1_3)

    is_duplicate_2_3 = check_duplicate(set2, set3)
    print(is_duplicate_2_3)


if __name__ == "__main__":
    # check_duplicate(set1, set2)
    __test()
