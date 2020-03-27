from data.api import GetLocalNewsData
from nltk import edit_distance



def CheckAllDistance():
    newsDataSamples = GetLocalNewsData(max=5000, hasMaxValue=True)
    compareUntil = 5

    i = 0

    for newsDataSample in newsDataSamples:
        print(newsDataSample.newsTime, newsDataSample.newsTitle)
        sampleLength = len(newsDataSample.newsTitle)
        compareSamples = newsDataSamples[i-compareUntil:i]
        for compareSample in compareSamples:
            compareSampleLength = len(compareSample.newsTitle)
            # print("\tcompareSample", compareSample.newsTitle)
            lenSum = abs(compareSampleLength - sampleLength)
            editDistance = edit_distance(newsDataSample.newsTitle, compareSample.newsTitle)
            print("\tlenSum", lenSum, "editDistance", editDistance, "compareSample", compareSample.newsTitle)
            if editDistance < 15: # Percentage not count
                print("\tcompareSample", editDistance, compareSample.newsTitle)
                pass
            # print("\teditDistance", editDistance)

        i += 1



def Test():

    sentA = "라면 먹고 갈래?"
    sentALen = len(sentA)
    sentB = "라면 먹고 가지 않을래?"
    sentBLen = len(sentB)
    maxLen = max(sentALen, sentBLen)
    lenSum = abs(sentALen - sentBLen)
    editDistance = edit_distance(sentA, sentB)
    print("editDistance", editDistance, "lenSum", lenSum, "maxLen", maxLen)




if __name__ == "__main__":
    # CheckAllDistance()
    Test()