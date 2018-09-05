
from Api.NewsDataService import NewsDataService
import re

service = NewsDataService()

data_list = service.FetchNewsData(10)

print(data_list)
for data in data_list:
    content = data.get_news_content()
    print(content)
    fs = [int(s) for s in re.findall(r'[-+]?[0-9]+', content)]
    print(fs)
