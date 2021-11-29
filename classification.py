from nltk import NaiveBayesClassifier
from nltk import FreqDist
from nltk import classify
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.svm import SVC
import csvWriter


class Modeling:

    def __init__(self, disease_name: str):
        self.disease_name = disease_name
        self._word_features = []
        self._classifier = None
        self.NaiveBayes()

        tfidf = TfidfVectorizer(max_features=1000)

        allArticlesInDiseaseCsv = csvWriter.readArticleData(self.disease_name)[:10]
        documents = csvWriter.readArticleData("false")[:10]
        self.target_train = target_train = []
        for eachArticle in allArticlesInDiseaseCsv:
            target_train.append(1)
        for eachArticle in documents:
            target_train.append(0)
        self.texts_train = texts_train = allArticlesInDiseaseCsv + documents

        texts_test = csvWriter.readArticleData(self.disease_name)[11:] + csvWriter.readArticleData("false")[11:]
        self.target_test = target_test =[]
        for eachArticle in csvWriter.readArticleData(self.disease_name)[11:]:
            target_test.append(1)
        for eachArticle in csvWriter.readArticleData("false")[11:]:
            target_test.append(0)

        self.texts_train1 = tfidf.fit_transform(texts_train)
        self.texts_test1 = tfidf.transform(texts_test)

    def NaiveBayes(self):
        # self._classifier = _classifier = LinearSVC()
        # model = CalibratedClassifierCV(_classifier)

        self._classifier = classifier = MultinomialNB()
        classifier.fit(self.texts_train1, self.target_train)

        # predictions = classifier.predict(self.texts_test1)
        # print("Naive Bayes:")
        # print('accuracy:', metrics.accuracy_score(self.target_test, predictions))
        # print("Precision:", metrics.precision_score(self.target_test, predictions))
        # print("Recall:", metrics.recall_score(self.target_test, predictions))

    def printMetrics(self):
        predictions = self._classifier.predict(self.texts_test1)
        print('accuracy:', metrics.accuracy_score(self.target_test, predictions))
        print("Precision:", metrics.precision_score(self.target_test, predictions))
        print("Recall:", metrics.recall_score(self.target_test, predictions))

class SVM:

    def __init__(self, disease_name):
        self.disease_name = disease_name.replace(' ', '')
        # self._word_features = []
        self._classifier = None
        self.fifthTimeHere()

    def fifthTimeHere(self):
        # self._classifier = _classifier = LinearSVC()
        # model = CalibratedClassifierCV(_classifier)

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

        texts_train1 = tfidf.fit_transform(texts_train)
        texts_test1 = tfidf.transform(texts_test)

        self._classifier = classifier = SVC()
        classifier.fit(texts_train1, target_train)

        predictions = classifier.predict(texts_test1)
        print("SVM:")
        print('accuracy:', metrics.accuracy_score(target_test, predictions))
        print("Precision:", metrics.precision_score(target_test, predictions))
        print("Recall:", metrics.recall_score(target_test, predictions))

    '''svm = Pipeline([
                    ('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', LinearSVC()),
                  ])
    
    svm.fit(X_train, y_train)
    
    y_pred = svm.predict(X_test)
    
    print('accuracy %s' % accuracy_score(y_pred, y_test))
    print(classification_report(y_test, y_pred))'''

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
    for eachDisease in diseases:
        naiveBayes = NaiveBayes(eachDisease)
        print()
        test2 = LogisticRegressionClassification(eachDisease)
        print()
        svmTesting = SVM(eachDisease)
        print()
    # test.accuracy_tests()
