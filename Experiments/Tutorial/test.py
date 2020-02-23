from nltk.tokenize import sent_tokenize, word_tokenize
exampleText = "Hello Mr. Smith, how are tou doing today? The weather is great and Python is awesome. The sky is pinkish-blue. You should not eat cardboard"
exampleText_KOR = "안녕하세요 우주님? 오늘은 날씨가 참좋구 파이썬은 개쩝니다. 하늘은 보라-파랑 빛이고 당신은 음주를 해야합니다."
print(sent_tokenize(exampleText_KOR))


for i in word_tokenize(exampleText):
    print(i)