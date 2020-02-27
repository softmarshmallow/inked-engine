## Spam document classification

### 접근방법 - 제목 우선
1. rule based 로 스팸이 확실한 뉴스의 셋을 구축한다.
    * 예 `[연예]` `[포토]` `[날씨]` 등과같이 박싱된 제목은 거의 90% 이상 스팸으로 분류해도 무관하다.

2. 스팸이 아닌 문서는 전채문서 빼기 스팸문서 셋 중 사람이 선별하여 동일한 숫자의 셋을 준비한다.

3. 

### 접근방법 - 문서 내용 포함
준비 되지 않았다.

### references
* Text Classification in Python[https://towardsdatascience.com/text-classification-in-python-dd95d264c802]
* https://towardsdatascience.com/text-classification-in-keras-part-1-a-simple-reuters-news-classifier-9558d34d01d3