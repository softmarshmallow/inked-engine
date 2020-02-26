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
- origin
- title
- time


# How to install virtualenv:

### Install **pip** first

    sudo apt-get install python3-pip

### Then install **virtualenv** using pip3

    sudo pip3 install virtualenv

### Now create a virtual environment

    virtualenv venv


## KoNlPy setup
http://konlpy.org/en/v0.4.4/install/
`sudo apt-get install g++ openjdk-8-jdk`
`bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)`


develped by softmarshmallow

