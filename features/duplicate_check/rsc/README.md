## general handling
example data sets -> same title, same content with different html holder (source)
- ebest.json
- naver.json


## exception handling
**sensitive cases** (need exception handling)리
- when content is small or empty
- when actually different news, but with same title
- when actually different news, but with same title, and similar content

conflict examples
- conflict-example-n.json


## differently distributed content
- news-ebest.html
- news-naver.html

you can see those two are same news, but distributed with different header & footer sections, we can dangerously remove them with rule based removal.
- in header section, `em` tag is removalble
- in fotter section we can remove it by ad-section remover in `utils` 
    - for now, we are using remove `a` tag from content assuming it is not useful for comparing news contents.