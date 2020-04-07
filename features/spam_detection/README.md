## Spam document classification

### 접근방법 - 제목 우선
1. rule based 로 스팸이 확실한 뉴스의 셋을 구축한다.
    * 예 `[연예]` `[포토]` `[날씨]` 등과같이 박싱된 제목은 거의 90% 이상 스팸으로 분류해도 무관하다.
    
    * 날씨
    * 섹시
    * 포토
    * 포토뉴스
    * 인사
    * 부고
    * 부음
    * 로또
    * 착한
    
2. 주제 based 
    * 범죄
    * 사고 / 화재 / 사망
    * 기부금 전달
    * 건강
    * 광고
    * 날씨
    * 스포츠
    * 연예

3. html 분석    
    * 사진 여러장
    * 내용물 없음
    * 제목 5자 미만
    * 동영상 있음

사진이 첨부된 문서를 분류후 수작업 태깅진행

2. 스팸이 아닌 문서는 전채문서 빼기 스팸문서 셋 중 사람이 선별하여 동일한 숫자의 셋을 준비한다.

3. 

### 접근방법 - 문서 내용 포함
접근 - 뉴스 문서안의 링크는 99% 스팸성이다. 본문을 광고영역과 컨탠츠 영역으로 분리하고, 광고영역에 스팸 태그를, 일반 컨텐츠에 일반 태그를 부여한후, 트래인한다.
모델 사용시 입력은 본문 광고영역을 제외한 컨탠츠만 입력하는 식으로 분석결과를 확인한다.

### references
* Text Classification in Python[https://towardsdatascience.com/text-classification-in-python-dd95d264c802]
* https://towardsdatascience.com/text-classification-in-keras-part-1-a-simple-reuters-news-classifier-9558d34d01d3