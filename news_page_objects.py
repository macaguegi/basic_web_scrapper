# Imports
import requests
import bs4
from common import config

# Father class that has a configuration , some queries (selectors) and it HTML
class NewsPage:

    def __init__(self,news_site_uid,url):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None

        self._visit(url)

    def _select(self,query_string):
        return self._html.select(query_string)


    def _visit(self,url):
        response = requests.get(url)
        response.raise_for_status()
        self._html = bs4.BeautifulSoup(response.text , 'html.parser')

# Child class that extends from NewsPage
class HomePage(NewsPage):

    def __init__(self,news_site_uid,url):
        super().__init__(news_site_uid,url)

    # List all of the articles in the page (Non-repeat)
    @property
    def article_links(self):
        link_list = []
        for link in self._select(self._queries['homepage_article_links']):
            if link and link.has_attr('href'):
                link_list.append(link)

        return set(link['href'] for link in link_list)

# Child class that extends from NewsPage
class ArticlePage(NewsPage):

    def __init__8(self,news_site_uid,url):
        super().__init__(news_site_uid,url)

    # Get all the body of an article 
    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        return result[0].text if len(result) else ''

    # Get the title of an article 
    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0].text if len(result) else ''