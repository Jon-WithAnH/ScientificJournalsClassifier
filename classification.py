from nltk import NaiveBayesClassifier
from nltk import FreqDist
from nltk import classify
import csvWriter


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

        posSet = [(self._document_features(d), 'pos') for d in documents]
        negSet = [(self._document_features(d), 'neg') for d in document2]
        train_set = posSet + negSet

        self._classifier = classifier = NaiveBayesClassifier.train(train_set)
        # classifier.show_most_informative_features()
        return True

    def accuracy_tests(self):
        if self._classifier is None:
            # raise AttributeError('classifier has not been trained yet. call obj.startTraining first')
            self._startTraining()

        _classifier = self._classifier

        documents = csvWriter.readArticleData(self.disease_name)[18:]
        testFeats = [(self._document_features(f), 'pos') for f in documents]

        document2 = csvWriter.readArticleData("false")[10:]
        moreTestFeats = [(self._document_features(f), 'neg') for f in document2]

        print(f'{self.disease_name} pos accuracy:', classify.util.accuracy(_classifier, testFeats))
        print(f'{self.disease_name} neg accuracy:', classify.util.accuracy(_classifier, moreTestFeats))

    def _document_features(self, document):
        document_words = set(document.split(" "))
        features = {}
        # for word in document.split(" "):
        #     print(word)
        for word in self._word_features:
            # print(word)
            features['contains({})'.format(word)] = (word in document_words)
        return features


class SVM:
    pass


class LogisticRegression:
    pass


if __name__ == '__main__':
    diseases = ['acute rheumatic arthritis', 'disease, lyme', 'abnormalities, cardiovascular', 'knee osteoarthritis']
    # test = NaiveBayes("acute rheumatic arthritis")
    for eachDisease in diseases:
        test = NaiveBayes(eachDisease)
        test.accuracy_tests()
