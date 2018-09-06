from Api.misc.LocalJsonDatabaseService import GetLocalNewsData
from Utils.BoxRemover import RemoveTitleBox

if __name__ == "__main__":
     news = GetLocalNewsData(max=10000, hasMaxValue=False)
     for n in news:
         titleBox = RemoveTitleBox(n.newsTitle)
         box = titleBox[1]
         if box is not None:
            # print(titleBox[1])
            if box == "특징주":
                print(n.newsTitle)
                # content = GetLinkLessContent(n.newsContent, html=False)
                # print(content)
                # print("\n\n\n")
