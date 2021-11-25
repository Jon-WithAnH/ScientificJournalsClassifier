from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from string import punctuation
import csvWriter
from collections import Counter


def normalize(arg: str) -> str:
    """
    :param arg: string that will be normalized
    :return: normalized string
    """
    postr = PorterStemmer()
    wnl = WordNetLemmatizer()
    stopWords = stopwords.words('english')

    text = word_tokenize(arg)
    # reverse iteration to aid in deletion of stopwords
    for i, word in reversed(list(enumerate(text))):
        for member in punctuation:
            if member == "-":
                # don't replace -
                continue
            text[i] = text[i].replace(member, " ")
        if word in stopWords:
            del text[i]
        else:
            text[i] = wnl.lemmatize(postr.stem(text[i]))

    return " ".join(text)


def normalizeList(arg: list) -> bool:
    """

    :param arg: list of strings to normalize
    :return: True on success
    """
    for j, eachArticle in enumerate(arg):
        eachArticle = normalize(eachArticle)
        arg[j] = eachArticle
    return True


def countWords(arg: str) -> Counter:
    return Counter(arg.split())


def countListOfWords(arg: list) -> list:
    """
    :param arg: list of strings
    :return: Counter object of number occurrences of each word
    """
    wordOccurrence = []
    for eachArticle in arg:
        # print(Counter(eachArticle.split()).keys(), Counter(eachArticle.split()).values())
        wordOccurrence.append(Counter(eachArticle.split()))
    # print(Counter([arg[i].split() for i in range(len(arg))]))
    return wordOccurrence


if __name__ == '__main__':
    test = csvWriter.readArticleData("acute rheumatic arthritis")
    normalizeList(test)
    # countListOfWords(test)
    print(countWords("im gonna spend all day applying for jobs"))
    # print(test)
