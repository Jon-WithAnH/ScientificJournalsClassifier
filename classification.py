from nltk import NaiveBayesClassifier
from nltk import FreqDist
from nltk import classify
from sklearn.model_selection import train_test_split

import csvWriter
from sklearn.svm import SVC
from numpy import dtype
class NaiveBayes:

    def __init__(self, disease_name: str):
        self.disease_name = disease_name
        self._word_features = []
        self._classifier = None

    def _startTraining(self) -> bool:
        """

        :return: True on completion
        """
        allArticlesInDiseaseCsv = csvWriter.readArticleData(self.disease_name)

        if len(allArticlesInDiseaseCsv) < 19:
            # insufficent data to train
            raise Exception('Not enough data to train naive classifier')

        bigString = " ".join(allArticlesInDiseaseCsv[:10])  # join the lists together
        all_words = FreqDist(bigString.split(" "))  # split it all by words
        self._word_features = list(all_words)

        documents = allArticlesInDiseaseCsv[10:18]
        document2 = csvWriter.readArticleData("false")[:10]

        # inputing a word, outputting a class
        posSet = [(self._document_features(d), 'pos') for d in documents]  # feature
        negSet = [(self._document_features(d), 'neg') for d in document2]
        # print(posSet)
        train_set = posSet + negSet

        self._classifier = classifier = NaiveBayesClassifier.train(train_set)
        # self._classifier.prob_classify()
        # classifier.show_most_informative_features()
        return True

    def accuracy_tests(self):
        if self._classifier is None:
            # raise AttributeError('classifier has not been trained yet. call obj.startTraining first')
            self._startTraining()

        _classifier = self._classifier
        documents = csvWriter.readArticleData(self.disease_name)[18:]
        testFeats = [(self._document_features(f), 'pos') for f in documents]
        # NaiveBayesClassifier.classify()
        document2 = csvWriter.readArticleData("false")[10:]
        moreTestFeats = [(self._document_features(f), 'neg') for f in document2]
        print("Naive Bayes:")
        print(f'{self.disease_name} method1 accuracy:', classify.util.accuracy(_classifier, testFeats))
        # print(self._classifier.classify(documents[4]))
        # print(f'{self.disease_name} method1 accuracy:', classify.util.accuracy(_classifier, testFeats))
        # print('accuracy:', metrics.accuracy_score(target_test, predictions))
        # print("Precision:", metrics.precision_score(target_test, predictions))
        # print("Recall:", metrics.recall_score(target_test, predictions))
        # print(f'{self.disease_name} neg accuracy:', classify.util.accuracy(_classifier, moreTestFeats))
        # print(f'{self.disease_name} pos accuracy:', classify.util. (_classifier, testFeats))

    def _document_features(self, document):
        document_words = set(document.split(" "))
        features = {}
        # for word in document.split(" "):
        #     print(word)
        for word in self._word_features:
            # print(word)
            features['contains({})'.format(word)] = (word in document_words)
        return features

import pandas as pd
from collections import Counter
class SVM:

    def __init__(self, disease_name):
        self.disease_name = disease_name.replace(' ', '')
        # self._word_features = []
        self._classifier = None
        self.fifthTimeHere()

    def fifthTimeHere(self):
        pass
    '''svm = Pipeline([
                    ('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', LinearSVC()),
                  ])
    
    svm.fit(X_train, y_train)
    
    y_pred = svm.predict(X_test)
    
    print('accuracy %s' % accuracy_score(y_pred, y_test))
    print(classification_report(y_test, y_pred))'''


    def pandaVersion2(self):
        allArticlesInDiseaseCsv = csvWriter.readBoWfromArticleData(self.disease_name)
        svclassifier = SVC(kernel='linear')

        documents = allArticlesInDiseaseCsv[10:20]
        # print(documents[1].split(" "))
        # tmp = documents[1].split()
        BoW = Counter(documents[1].split(" "))
        # print(Counter(documents[1].split(" ")))
        print(BoW)
        del BoW[""]
        # print(BoW)
        print(BoW.keys())
        print(list(BoW.values()))
        # print((Counter(documents[1])).values())
        # print((Counter(documents[1])).keys())


    def pandaStuff(self):
        self.data = pd.read_csv(self.disease_name)
        print(self.data.shape)
        print(self.data.head())
        # X = self.data.drop("BoW'd Article", axis=1)
        X = self.data["BoW'd Article"]
        y = self.data["BoW'd Article"]

        # print(y)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
        svclassifier = SVC(kernel='linear')
        print(X_train, y_train)
        svclassifier.fit(X, y)

    def eyes(self, disease_name):
        self.disease_name = disease_name
        self._word_features = []
        self._classifier = None

        allArticlesInDiseaseCsv = csvWriter.readBoWfromArticleData(self.disease_name)
        svclassifier = SVC(kernel='linear')

        bigString = " ".join(allArticlesInDiseaseCsv[:10])  # join the lists together
        all_words = FreqDist(bigString.split(" "))  # split it all by words
        self._word_features = list(all_words)

        documents = allArticlesInDiseaseCsv[10:20]
        document2 = csvWriter.readBoWfromArticleData("false")[:10]
        # print(documents)
        # posSet =
        posSet = [(self._document_features(d), 'pos') for d in documents]
        negSet = [(self._document_features(d), 'neg') for d in document2]
        train_set = posSet + negSet
        # X = data.iloc[:, 5:17].values
        # y = data.iloc[:, 17:18].values
        # print(posSet, negSet)
        X_train, X_test, y_train, y_test = train_test_split(posSet, negSet, test_size=0.20)
        print(X_train.dtype, y_train.dtype)
        # print(X_train, y_train)
        # svclassifier.fit(X_train, y_train)

    # def _document_features(self, document):
    #     document_words = set(document.split(" "))
    #     features = {}
    #     # for word in document.split(" "):
    #     #     print(word)
    #     for word in self._word_features:
    #         # print(word)
    #         features['contains({})'.format(word)] = (word in document_words)
    #     return features

from sklearn.linear_model import LogisticRegression
# import pandas
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer

class LogisticRegressionClassification:
    # y needs to be the label
    # normalized words as columns
    # each article as a row
    # number of word occurance as the row value for each word
    def __init__(self, disease_name):
        self.disease_name = disease_name.replace(' ', '')
        self.thirdFunctionsTheCharm()
        self._classifier = None

    def thirdFunctionsTheCharm(self):

        tfidf = TfidfVectorizer(max_features=1000)  # stop_words='english',)# norm = None)#)

        allArticlesInDiseaseCsv = csvWriter.readArticleData(self.disease_name)[:10]
        documents = csvWriter.readArticleData("false")[:10]
        target_train = []
        for eachArticle in allArticlesInDiseaseCsv:
            target_train.append(1)
        for eachArticle in documents:
            target_train.append(0)
        texts_train = allArticlesInDiseaseCsv + documents

        texts_test = csvWriter.readArticleData(self.disease_name)[11:] + csvWriter.readArticleData("false")[11:]
        target_test = []
        for eachArticle in csvWriter.readArticleData(self.disease_name)[11:]:
            target_test.append(1)
        for eachArticle in csvWriter.readArticleData("false")[11:]:
            target_test.append(0)
        # print(target_test)
        texts_train1 = tfidf.fit_transform(texts_train)
        texts_test1 = tfidf.transform(texts_test)

        self._classifier = classifier = LogisticRegression()
        classifier.fit(texts_train1, target_train)
        predictions = classifier.predict(texts_test1)
        print("Logistic Regression:")
        print('accuracy:', metrics.accuracy_score(target_test, predictions))
        print("Precision:", metrics.precision_score(target_test, predictions))
        print("Recall:", metrics.recall_score(target_test, predictions))
        # print(tfidf.get_feature_names_out())

    def printRatings(self):
        # predictions = self._classifier.predict(texts_test1)
        # print("Logistic Regression:")
        # print('accuracy:', metrics.accuracy_score(target_test, predictions))
        # print("Precision:", metrics.precision_score(target_test, predictions))
        # print("Recall:", metrics.recall_score(target_test, predictions))
        pass


if __name__ == '__main__':
    diseases = ['acute rheumatic arthritis', 'disease, lyme', 'abnormalities, cardiovascular', 'knee osteoarthritis']
    # test = NaiveBayes("acute rheumatic arthritis")
    for eachDisease in diseases:
        test = NaiveBayes(eachDisease)
        test.accuracy_tests()
        print()
        test2 = LogisticRegressionClassification(eachDisease)
        # print('\n')
    # test.accuracy_tests()
