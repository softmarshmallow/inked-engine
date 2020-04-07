import ahocorasick
from typing import List
from data.api.company_data_api import get_company_by_name, fetch_all_company_list
from data.local.models import ExtractedInformation


def find_companies_in_content(content: str, allow_overlap: bool = True) -> List[ExtractedInformation]:
    """
    Finds company in news, but with Aho corasic method
    allowOverlap = True // 삼성전자, 대성, 삼성전자, 삼성전자 || False // 삼성전자, 대성
    """
    companies: List[ExtractedInformation] = []

    auto = ahocorasick.Automaton()
    for comp in fetch_all_company_list():
        auto.add_word(comp.compName, comp.compName)
    auto.make_automaton()

    for found in auto.iter(content):
        filtered_compName = found[1]
        end_span = found[0]
        start_span = end_span - (len(filtered_compName) - 1)
        span = (start_span, end_span)
        company = get_company_by_name(filtered_compName)
        ei = ExtractedInformation(original=content, information=company, span=span)
        companies.append(ei)
        # print(found)

    if not allow_overlap:
        no_overlap_comps = []
        [no_overlap_comps.append(v) for v in companies if v not in no_overlap_comps]
        return no_overlap_comps

    return companies


class CompanyExtractor:
    def __init__(self, txt):
        self.txt = txt

    def extract_companies(self):
        return find_companies_in_content(content=self.txt)


def test_findall_company_in_text():
    txt = """한편 이날 승 부사장의 강연에는 800여명 넘는 참석자들이 몰렸다. LG전자와 SK하이닉스 등 국내 IT기업 관계자들도 승 부사장의 강연을 듣기위해 참석하는 진풍경이 벌어졌다. 과학기술정보통신부 관계자도 찾아 승 부사장에게 강연을 요청하기도 했다. 
미국 하버드대를 졸업한 승 부사장은 인공신경망 분야 세계적 석학으로 삼성전자는 지난 6월 그를 부사장으로 영입했다. 미국 대학의 교수직을 겸임하면서 삼성전자 부사장급 직책을 맡는 파격적인 대우다. 삼성의 미래 성장동력이 될 AI 핵심 인재들을 키우겠다는 강력한 의지였다. 승 부사장은 미국 벨연구소 재직 당시  뇌 신경활동을 모방한 컴퓨터 프로그램을 공동 개발한 뒤 네이처에 발표하면서 학계의 스타로 떠올랐다.
포럼은 AI에 대한 높은 관심을 반영한듯 대히트를 기록했다. 전날 삼성 서초사옥에서 열린 포럼 참가자까지 합치면 1500명의 학계, 업계 관계자들이 삼성 AI 포럼에 참석했다. 전날 포럼에는 얀 르쿤 뉴욕대 교수 외에도 요수아 벤지오 캐나다 몬트리올대 교수, 조엘 피노 맥길대 교수, 애런 쿠르빌 몬트리올대 교수, 양은호 카이스트 교수 등도 강연자로 나섰다. 르쿤 교수와 요수아 벤지오 교수는 딥러닝 분야의 세계적인 대가로 꼽힌다. 이날은 언어·추론과 시각·로보틱스·온디바이스 AI 등 두 가지 주제로 나눠 신시아 브리질 미국 매사추세츠 공과대학(MIT) 미디어랩 교수, 베리 스미스 더블린대학교 교수, 드미리스 임페리얼 컬리지 런던 이아니스 교수, 위구연 하버드대학교 교수 등이 발표를 진행했다. 
한편 김현석 삼성전자 대표이사(삼성리서치 소장)는 이날 포럼에서 기자들과 만나 "단순 엔지니어 수준을 넘어 세계적으로 저명한 분들을 영입할 것"이라고 강조했다. 김 대표는 "쉽지는 않겠지만, AI 분야 전반이 커지고 있기 때문에 석학 중심의 인재풀을 확보하겠다"고 했다. 
삼성은 지난 8월 AI를 4대 미래 성장사업 중 하나로 정하고 연구 역량을 공격적으로 늘리고 있다. 지난해 11월 한국 AI 총괄센터 설립을 시작으로 미국 실리콘밸리, 영국 케임브리지 등에 이어 최근 미국 뉴욕에 6번째 글로벌 AI 연구센터를 설립했다. 2020년까지 글로벌 연구 거점에 약 1000명의 AI 선행 연구개발 인력을 확보할 방침이다."""
    comps = find_companies_in_content(txt)
    print(comps)


if __name__ == "__main__":
    test_findall_company_in_text()
