from pprint import pprint
from Utils.news_box_util import remove_box, extract_boxes
from Api.NewsDataService import NewsDataService
ns = NewsDataService()
news_data_list = ns.FetchNewsData()


def get_all_feature_stock_news():
    feature_stock_news_list = []
    for news_data in news_data_list:
        result = extract_boxes(news_data.newsTitle)
        if len(result) > 0:
            if "특징주" in result[0].innerBoxContent:
                feature_stock_news_list.append(news_data)

    return feature_stock_news_list


if __name__ == "__main__":
    data = get_all_feature_stock_news()
    for record in data:
        print("[NEWS]")
        print(record.newsTitle)
        print(record.newsContent)
        # print('\n\n\n')

