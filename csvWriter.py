import csv
from sys import stderr
from os import path


def writeToCsv(article: list, disease_name: str, demo=False) -> bool:
    """

    :param article: the article information with url at [0] and article contents as [1]
    :param disease_name: the name of the disease
    :param demo: writes data to a file that can safely be deleted at any time
    :return: True if successfully written. False is nothing was there to write.
    """
    disease_name = 'demo' if demo else disease_name.replace(" ", "")

    if not article:
        # note: this shouldn't ever happen. exists just in case.
        print(f"No text found to write", file=stderr)
        return False
    with open(f'{disease_name}.csv', 'a', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        article[1] = article[1].replace("\n", " ")
        writer.writerow(article)
    print('write complete', end="")
    return True


def writeHeader(disease_name: str, demo=False) -> bool:
    """
    :param demo: writes data to a file that can safely be deleted at any time
    :param disease_name: the name of the disease
    :return: bool True if successful write. False if already exists.
    """
    disease_name = 'demo' if demo else disease_name.replace(" ", "")
    # determine if file is already there
    # if it is, no need to write header
    if path.isfile(disease_name + ".csv"):
        # file & header info is already there.
        return False
    header = ['Link location', 'Article Data', 'Normalized Article', 'BoW\'d Article']
    with open(f'{disease_name}.csv', 'w', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    return True


def readArticleData(disease_name: str) -> list:
    """
    :param disease_name: the name of the disease
    :return: string of article contents
    """
    nonnormalizedArticle = []
    disease_name = disease_name.replace(" ", "") +'.csv'
    with open(disease_name, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)  # skip over header
        for i, eachRow in enumerate(csv_reader):  # csv_reader uses a generator. cannot be indexed
            nonnormalizedArticle.append(eachRow[2])
    if not nonnormalizedArticle:
        raise AttributeError("No data was read")
    return nonnormalizedArticle

def readBoWfromArticleData(disease_name: str) -> list:
    """
    :param disease_name: the name of the disease
    :return: string of article contents
    """
    BoWArticles = []
    disease_name = disease_name.replace(" ", "") + '.csv'
    with open(disease_name, 'r', encoding='utf-8') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)  # skip over header
        for i, eachRow in enumerate(csv_reader):  # csv_reader uses a generator. cannot be indexed
            BoWArticles.append(eachRow[2])
    if not BoWArticles:
        raise AttributeError("No data was read")
    return BoWArticles


def readOneArticle(disease_name: str) -> list:
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
            return list(eachRow[1])
            # for eachword in eachRow[1]:
            #     nonnormalizedArticles.append(eachword)
            # return nonnormalizedArticles
    return []
