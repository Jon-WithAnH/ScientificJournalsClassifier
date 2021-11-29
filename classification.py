from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from sklearn.svm import SVC
import csvWriter


class Modeling:

    def __init__(self, disease_name: str):
        self.disease_name = disease_name
        self._classifier = None
        self._activeClassifier = ''

        # used for training
        allArticlesInDiseaseCsv = csvWriter.readArticleData(self.disease_name)[:10]
        documents = csvWriter.readArticleData("false")[:10]
        self.target_train = target_train = []
        for eachArticle in allArticlesInDiseaseCsv:
            target_train.append(1)
        for eachArticle in documents:
            target_train.append(0)
        self.texts_train = allArticlesInDiseaseCsv + documents

        # preparing tests
        texts_test = csvWriter.readArticleData(self.disease_name)[11:] + csvWriter.readArticleData("false")[11:]
        self.target_test = target_test = []
        for eachArticle in csvWriter.readArticleData(self.disease_name)[11:]:
            target_test.append(1)
        for eachArticle in csvWriter.readArticleData("false")[11:]:
            target_test.append(0)

        tfidf = TfidfVectorizer(max_features=2000)  # helps format data for fit
        self.texts_train = tfidf.fit_transform(self.texts_train)
        self.texts_test = tfidf.transform(texts_test)

    def setNaiveBayes(self):
        self._classifier = MultinomialNB()
        self._classifier.fit(self.texts_train, self.target_train)
        self._activeClassifier = "Naive Bayes"

    def setSVC(self):
        self._classifier = SVC()
        self._classifier.fit(self.texts_train, self.target_train)
        self._activeClassifier = "SVC"

    def setLogisticRegression(self):
        self._classifier = LogisticRegression()
        self._classifier.fit(self.texts_train, self.target_train)
        self._activeClassifier = "Logistic Regression"

    def printMetrics(self):
        predictions = self._classifier.predict(self.texts_test)
        print(f'{self._activeClassifier}:')
        print('accuracy:', metrics.accuracy_score(self.target_test, predictions))
        print("Precision:", metrics.precision_score(self.target_test, predictions))
        print("Recall:", metrics.recall_score(self.target_test, predictions))
        print("F1 score:", metrics.f1_score(self.target_test, predictions))

    def printMetrics_ForEachModel(self):
        print(f'{self.disease_name.rjust(75)}')
        self.setNaiveBayes()
        self._prettyMetricPrint()
        self.setSVC()
        self._prettyMetricPrint()
        self.setLogisticRegression()
        self._prettyMetricPrint()
        print()

    def _prettyMetricPrint(self):
        predictions = self._classifier.predict(self.texts_test)
        print(f'{self._activeClassifier.ljust(20)}:', end='')
        print(' accuracy:', str(metrics.accuracy_score(self.target_test, predictions)).ljust(18),end='')
        print(" Precision:", str(metrics.precision_score(self.target_test, predictions)).ljust(18),end='')
        print(" Recall:", str(metrics.recall_score(self.target_test, predictions)).ljust(18), end='')
        print(" F1 score:", str(metrics.f1_score(self.target_test, predictions)).ljust(18))


if __name__ == '__main__':
    diseases = ['acute rheumatic arthritis', 'disease, lyme', 'abnormalities, cardiovascular', 'knee osteoarthritis']
    for eachDisease in diseases:
        model = Modeling(eachDisease)
        model.printMetrics_ForEachModel()
