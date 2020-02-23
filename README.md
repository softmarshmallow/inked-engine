# inked engine

| 뉴스 분석을 위한 툴킷입니다. 

Main features

* news data indexing

* news data processing

* provide api for service server

  

Inked-news-crawler 에서 새로운 뉴스데이터를 받아온후, 인덱싱과 pre-proccessing 을 합니다. 서비스 서버에서 요청하는 정보를 분석하여 서비스 서버로 전달하며, 서비스 서버에서 클라이언트로 뉴스 정보를 제공합니다.


## News data model

- tags : { company : [], namedEntities: [], keywords: []}
- content
- originUrl
- title
- time

develped by softmarshmallow