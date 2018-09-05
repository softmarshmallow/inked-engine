import re


def get_quote_content(content):
    results = []
    quotes_regex = ['\'([^\']*)\'', '"([^"]*)"']
    for regex in quotes_regex:
        res = re.findall(regex, content)
        results.extend(res)
    return results



if __name__ == "__main__":
    content = "[슬라이드 포토] '웰컴 2018' 세계 곳곳 신년맞이 불꽃놀이"
    res = get_quote_content(content)
    print(res)
