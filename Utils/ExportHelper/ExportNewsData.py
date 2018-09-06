import os
import xlsxwriter
from typing import List

from bs4 import BeautifulSoup

from Api.misc.LocalJsonDatabaseService import GetLocalNewsData
from DataModels.news_models import NewsDataModel


def Export(rows:int, exportPath:str):
    # Create file
    path = os.path.join(exportPath, "demo.xlsx")
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    worksheet.write(2, 0, 123)
    worksheet.write(3, 0, 123.456)



    # Read data
    newsDataList: List[NewsDataModel] = GetLocalNewsData(100, True)
    index = 0
    for newsData in newsDataList:
        # Polish content
        bs = BeautifulSoup(newsData.newsContent, "lxml")


        worksheet.write(index, 0, newsData.newsTime)
        worksheet.write(index, 1, newsData.newsTitle)
        worksheet.write(index, 2, str(bs.get_text()))
        worksheet.write(index, 3, newsData.providerId)

        index += 1


    workbook.close()


if __name__ == "__main__":
    Export(100, "/Users/softmarshmallow/Desktop/Temp")