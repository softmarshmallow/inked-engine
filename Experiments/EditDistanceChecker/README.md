## news duplication checker for multiple crawling source
this feature is used when using multiple news source, in my case ebest, and naver.
ebest news is realtime, and naver news is crawled 1~2 minute late, containing more detailed information.

- time (not crawled time, but publish time) should match in max of  2 minute diff
- title will must match 100% (ignoring whitespaces)
- content should match removing ad section & non html plain text -> higher than 80%
- provider must match (but ignore when unknown provider)


**sensitive cases** (need exception handling)
- when content is small or empty
- when actually different news, but with same title
- when actually different news, but with same title, and similar content
