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

from gensim.models import Word2Vec

def tryingGensim():
    listofAllArticles = [csvWriter.readArticleData("acuterheumaticarthritis")[0], csvWriter.readArticleData("acuterheumaticarthritis")[1]]
    # listofAllArticles = listofAllArticles.split(" ")
    [tokenized_text, tokens2] = word_tokenize(listofAllArticles[0]), word_tokenize(listofAllArticles[1])
    test = []
    test.append(tokenized_text)
    test.append(tokens2)
    # print(tokenized_text)
    model = Word2Vec(test)
    # for word in listofAllArticles:
    #     print(word)
    # print(listofAllArticles)
    # vector = model.wv['dog']  # numpy vector of word
    print(model.wv.key_to_index)
    sims = model.wv.most_similar('of', topn=10)
    print(sims)
    # # print(listofAllArticles)
    # w2v_model = Word2Vec()
    # w2v_model.build_vocab(listofAllArticles)
    # for eachWord in w2v_model.wv.key_to_index:
    #     print(eachWord)
    # w2v_model.train(listofAllArticles, total_examples=w2v_model.corpus_count, epochs=w2v_model.epochs)
    # w2v_model.init_sims(replace=True)
    # w2v_model.
    # print(w2v_model.wv.most_similar(positive=["clinical"]))


if __name__ == '__main__':
    # test = csvWriter.readArticleData("acute rheumatic arthritis")
    # normalizeList(test)
    # countListOfWords(test)
    # print(countWords("im gonna spend all day applying for jobs"))
    tryingGensim()
    # print(test)
