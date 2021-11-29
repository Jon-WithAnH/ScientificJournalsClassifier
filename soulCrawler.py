from sys import stderr
import requests
from bs4 import BeautifulSoup
from bs4 import Tag as bs4Tag
import csvWriter
import Normalizing


class Crawler:

    def __init__(self, search_term: str, year_time_frame: str, demo=False):
        """
        :param search_term: desired search query
        :param year_time_frame: time frame in years. eg 1990-2000
        :param demo: prevents appending to existing csv files
        """
        self.search_term = search_term
        self.time_frame = year_time_frame

        self._demo = demo
        self._currentPage = 1
        self._articles = []
        self._url = f"https://pubmed.ncbi.nlm.nih.gov/?term={search_term.replace(' ', '+')}" \
                   f"&filter=simsearch2.ffrft&filter=lang.english&filter=years.{year_time_frame}"
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Connection': 'close'
        }
        # print(url)
        self._queryPage(self._url)

    def beginCrawling(self, n=5):
        """

        :param n: amount of articles to retrieve
        :return: amount of articles successfully written
        """
        written = 0
        while written < n:
            if self._grabText():
                written += 1
                print(" #", written, sep='')
        return written

    def _queryPage(self, url: str) -> bool:
        """
        sets self._articles to a list of all the article links on the page
        :param url: url of search query
        :return: True on success
        """
        f = requests.get(url, headers=self._headers)
        soup = BeautifulSoup(f.content, 'lxml')
        self._articles = articles = soup.find_all("a", {"class": "docsum-title"})
        if not articles:
            raise AttributeError(f"search term yielded zero results")
        return True

    def _getNextArticle(self):
        """

        :return: web ID of next article
        """
        # works from the bottom of the webpage up
        if len(self._articles) == 0:
            self._currentPage += 1
            try: self._queryPage(self._url + f"&page={self._currentPage}")
            except AttributeError as e:
                print("End of results")  # no more results to query
                # TODO clean up this exit call
                exit(0)
        # print(self.articles.pop()['href'])
        return self._articles.pop()['href']

    def _beginSearchForArticleSource(self) -> str or None:
        """:return a valid link to where ever the webpage is located. or a list of a links"""
        # time.sleep(2) # pause for a little bit to not overload them
        articleID = self._getNextArticle()
        url = f"https://pubmed.ncbi.nlm.nih.gov{articleID}"
        f = requests.get(url, headers=self._headers)
        soup = BeautifulSoup(f.content, 'lxml')

        tmp = soup.find_all("a", {"class": "link-item pmc dialog-focus"})
        if not tmp:
            # might be a link with two dialog options which changes the class
            tmp = soup.find_all("a", {"class": "link-item pmc"})
            if not tmp:
                print(f"unable to find link to full text in url: {url}", file=stderr, flush=True)
            else:
                return tmp.pop()['href']
        else:
            return tmp.pop()['href']

        # nothing found
        return

    def _grabText(self) -> bool:
        """

        :return: True on success
        """
        url = self._beginSearchForArticleSource()
        if url is None:
            # above method didn't find anything and has already printed the error. return and try next article
            return False
        f = requests.get(url, headers=self._headers)
        soup = BeautifulSoup(f.content, 'lxml')
        tmp = soup.find_all("div", {"class": "jig-ncbiinpagenav"})
        if not tmp:
            print(f"Unable to find full text for url: {url}", file=stderr)
            return False
        cleanText = []
        for child in tmp.pop():  # removes tags within the text clipping
            if isinstance(child, bs4Tag):
                cleanText.append(child.text)
        cleanText = " ".join(cleanText[3:-3])

        self._updateCsvFile(url, cleanText)
        # return cleanText
        return True

    def _updateCsvFile(self, url, text) -> bool:
        """

        :param url: url to be written
        :param text: text to be written. Also gets the normalized version written
        :return: True on success
        """
        # FIXME writes below link as comment in csv file
        # https://www.ncbi.nlm.nih.gov/pmc/articles/pmid/31084592/,,,Counter()
        # https://www.ncbi.nlm.nih.gov/pmc/articles/pmid/26020139/,,,Counter()
        # https://www.ncbi.nlm.nih.gov/pmc/articles/pmid/14500407/,,,Counter()

        normalizedText = Normalizing.normalize(text)
        countedWords = Normalizing.countWords(normalizedText)
        csvWriter.writeHeader(self.search_term, self._demo)  # header info is only written once
        # csvWriter.writeHeader("false")
        csvWriter.writeToCsv([url, text, normalizedText, countedWords], self.search_term, self._demo)
        # csvWriter.writeToCsv([url, text, normalizedText, countedWords], "false")
        return True


def randomWordsCsv() -> None:
    """
    function to generate irrelivent articles to use for training
    :return: None
    """
    randomWords = ['wobble', 'rampant', 'one', 'strip', 'jellyfish', 'material', 'recess',
                   'threatening', 'corn', 'acoustic', 'rail', 'drawer', 'visit', 'fireman ', 'outstanding']
    # print(randomWords)
    # test = Crawler("wartz", "1900-2021")
    for eachWord in randomWords:
        tmpObj = Crawler(eachWord, "1900-2021")
        tmpObj.beginCrawling(n=1)


def demo():
    diseases = ['acute rheumatic arthritis', 'disease, lyme', 'abnormalities, cardiovascular', 'knee osteoarthritis']
    # for eachDisease in diseases:
    obj = Crawler('acute rheumatic arthritis', "1949-2021", demo=True)
    obj.beginCrawling(n=10)


def downloadABunchOfArticles(n=100):
    diseases = ['acute rheumatic arthritis', 'disease, lyme', 'abnormalities, cardiovascular', 'knee osteoarthritis']
    for eachDisease in diseases:
        obj = Crawler(eachDisease, "1949-2021")
        obj.beginCrawling(n=n)


if __name__ == '__main__':
    # demo()
    downloadABunchOfArticles()
    # test = Crawler("diease, lyme", "1949-1980")  # IMPORTANT: only produces 4 results. keep for testing
    # test = Crawler("disease, lyme", "1949-2021", demo=True)
    # test = Crawler("acute rheumatic arthritis", "1990-2021")
    # testtt = Crawler("cancer", "1990-2001", demo=True)
    # test = Crawler("abnormalities, cardiovascular", "1949-2021")
    # test.beginCrawling(n=35)
    # knee osteoarthritis
    # test = Crawler("knee osteoarthritis", "1949-2021")
    # test.beginCrawling(n=35)
    # generate csv for false classifcation
    # randomWordsCsv()
