## news duplication checker for multiple crawling source
this feature is used when using multiple news source, in my case ebest, and naver.
ebest news is realtime, and naver news is crawled 1~2 minute late, containing more detailed information.

> this is duplicate checker, not similar content checker. (internally uses similarity checking but still not purposed on checking similarity) 

- time (not crawled time, but publish time) should match in max of  2 minute diff
- title will must match 100% (ignoring whitespaces)
- content should match removing ad section & non html plain text -> higher than 80%
- provider must match (but ignore when unknown provider)


**sensitive cases** (need exception handling)리
- when content is small or empty
- when actually different news, but with same title
- when actually different news, but with same title, and similar content
- 표, 사진 only 뉴스 처리 방법



## content similarity check with nltk.jarccard_distance

> output without processing was. `0.1456953642384106`
> after removing html tags & tab, new line will bring us, `0.11231884057971014` 
> after removing html tags & `em`, `a` tag will bring us, `0.013333333333333334` 

`MAX_ACCEPTED_JACCARD_DISTANCE = 0.05`


## differently distributed contents
