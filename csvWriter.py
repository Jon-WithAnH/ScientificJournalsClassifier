import csv
import sys
from os import path


def writeToCsv(article: list, disease_name: str):
    """

    :param article: the article information with url at [0] and article contents as [1]
    :param disease_name: the name of the disease
    :return: True if successfully written. False is nothing was there to write.
    """
    disease_name = disease_name.replace(" ", "")
    if not article:
        # note: this shouldn't ever happen. exists just in case.
        print(f"No text found to write", file=sys.stderr)
        return False
    with open(f'{disease_name}.csv', 'a', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        # article[1] = article[1].replace(",", "").replace("(", "").replace(")", "").replace("\n", " ")
        article[1] = article[1].replace("\n", " ")
        writer.writerow(article)
        f.close()
    print('write complete')
    return True


def writeHeader(disease_name):
    """

    :param disease_name: the name of the disease
    :return: bool True if successful write. False if already exists.
    """
    disease_name = disease_name.replace(" ", "")+'.csv'
    # determine if file is already there
    # if it is, no need to write header
    if path.isfile(disease_name):
        # file & header info is already there.
        return False
    header = ['Link location', 'Article Data', 'Normalized Article', 'BoW\'d Article']
    with open(disease_name, 'w', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    return True


def readArticleData(disease_name) -> list:
    """
    :param disease_name: the name of the disease
    :return: string of article contents
    """
    nonnormalizedArticles = []
    disease_name = disease_name.replace(" ", "")+'.csv'
    with open(disease_name, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)  # skip over header
        for i, eachRow in enumerate(csv_reader):  # csv_reader uses a generator. cannot be indexed
            nonnormalizedArticles.append(eachRow[1])
    return nonnormalizedArticles

if __name__ == '__main__':
    # tmp = soulCrawler.Crawler("diease, lyme", "1949-1980")  # yields 4 results, all fail
    # writeHeader()
    # writeToCsv(tmp)
    print(readArticleData("acuterheumaticarthritis"))
