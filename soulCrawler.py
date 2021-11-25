import os.path
import sys
import requests
import lxml
from bs4 import BeautifulSoup
from bs4 import Tag as bs4Tag
import csvWriter
import Normalizing


class Crawler:

    def __init__(self, search_term: str, year_time_frame: str):
        """
        :param search_term: desired search query
        :param year_time_frame: time frame in years. eg 1990-2000
        """
        self.search_term = search_term
        self.currentPage = 1
        self.articles = []
        self.url = f"https://pubmed.ncbi.nlm.nih.gov/?term={search_term.replace(' ', '+')}" \
                   f"&filter=simsearch2.ffrft&filter=lang.english&filter=years.{year_time_frame}"
        # self.headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0'
        # }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Connection': 'close'
        }
        # print(url)
        self.queryPage(self.url)

    def queryPage(self, url):
        f = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(f.content, 'lxml')
        self.articles = articles = soup.find_all("a", {"class": "docsum-title"})
        if not articles:
            raise AttributeError(f"search term yielded zero results")

    def getNextArticle(self):
        # works from the bottom of the webpage up
        if len(self.articles) == 0:
            self.currentPage += 1
            try: self.queryPage(test.url + f"&page={self.currentPage}")
            except AttributeError as e:
                print("End of results")  # no more results to query
                exit(0)
        # print(self.articles.pop()['href'])
        return self.articles.pop()['href']

    def beginSearchForArticleSource(self) -> str or None:
        """:return a valid link to whereever the webpage is located. or a list of a links"""
        # time.sleep(2) # pause for a little bit to not overload them
        articleID = self.getNextArticle()
        url = f"https://pubmed.ncbi.nlm.nih.gov{articleID}"
        f = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(f.content, 'lxml')
        # tmp = soup.find_all("div", {"class": "full-text-links-list"})
        tmp = soup.find_all("a", {"class": "link-item pmc dialog-focus"})
        # print(tmp)
        # exit(-1)
        if not tmp:
            # might be a link with two dialog options which changes the class
            tmp = soup.find_all("a", {"class": "link-item pmc"})
            if not tmp:
                print(f"unable to find link to full text in url: {url}", file=sys.stderr, flush=True)
            else:
                return tmp.pop()['href']
        else:
            return tmp.pop()['href']
            # return None
        # nothing found
        return

    def grabText(self) -> str or None:  # hopefully
        """

        :return: None or article contents
        """
        url = self.beginSearchForArticleSource()
        if url is None:
            # above method didn't find anything and has already printed the error. return and try next article
            return
        f = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(f.content, 'lxml')
        tmp = soup.find_all("div", {"class": "jig-ncbiinpagenav"})
        if not tmp:
            print(f"Unable to find full text for url: {url}", file=sys.stderr)
            return
        cleanText = []
        for child in tmp.pop():  # removes tags within the text clipping
            if isinstance(child, bs4Tag):
                cleanText.append(child.text)
        cleanText = " ".join(cleanText[3:-3])

        self.updateCsvFile(url, cleanText)
        return cleanText

    def updateCsvFile(self, url, text) -> bool:
        """

        :param url: url to be written
        :param text: text to be written. Also gets the normalized version written
        :return: True on success
        """
        normalizedText = Normalizing.normalize(text)
        countedWords = Normalizing.countWords(normalizedText)

        csvWriter.writeHeader(self.search_term)  # header info is only written once
        csvWriter.writeToCsv([url, text, normalizedText, countedWords], self.search_term)
        return True


if __name__ == '__main__':
    test = Crawler("acute rheumatic arthritis", "1990-2021")
    # test = Crawler("diease, lyme", "1949-1980")
    for i in range(10):
        # print(f"{i+1} ", end='')
        test.grabText()
        # if not test.articles:
        #     currentPage += 1
        #     # ran out of articles to process, query for more
        #     try: test.queryPage(test.url + f"&page={currentPage}")
        #     except AttributeError as e:
        #         print("End of results")  # no more results to query
        #         exit(0)
