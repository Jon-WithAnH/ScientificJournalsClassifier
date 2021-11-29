from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from string import punctuation

from collections import Counter


def normalize(arg: str) -> str:
    """
    :param arg: string that will be normalized
    :return: normalized string
    """
    postr = PorterStemmer()
    wnl = WordNetLemmatizer()
    stopWords = stopwords.words('english')
    stopWords.append('’')  # special chars pick up by crawler
    stopWords.append('‘')
    text = word_tokenize(arg)
    # reverse iteration to aid in deletion of stopwords
    for i, word in reversed(list(enumerate(text))):
        for member in punctuation:
            if member == "-":
                # don't replace -
                continue
            text[i] = text[i].replace(member, " ")
        if word.lower() in stopWords:
            del text[i]
        else:
            text[i] = wnl.lemmatize(postr.stem(text[i].lower()))

    return " ".join(text)


def countWords(arg: str) -> Counter:
    return Counter(arg.split())


def normalizeList(arg: list) -> bool:
    """

    :param arg: list of strings to normalize
    :return: True on success
    """
    for j, eachArticle in enumerate(arg):
        eachArticle = normalize(eachArticle)
        arg[j] = eachArticle
    return True


def countListOfWords(arg: list) -> list:
    """
    :param arg: list of strings
    :return: Counter object of number occurrences of each word
    """
    wordOccurrence = []
    for eachArticle in arg:
        wordOccurrence.append(Counter(eachArticle.split()))
    return wordOccurrence

