import feedparser

#create a variable that holds the parsed rss feed
feed = feedparser.parse("https://medium.com/feed/tag/ai")

class Article:
    def __init__(self, entry):
        self.title = entry.get('title')
        self.link = entry.get('link')
    def __str__(self):
        return f"The title of the artile is {self.title} and the the link is {self.link}"
class ArticleContainer:
    def __init__(self, entries):
        self.articles = [Article(article) for article in entries]
    
def feedreader(feed):
    container = ArticleContainer(feed.get('entries'))
    articles_dict = {}
    for i in container.articles:
        articles_dict[i.title] = i.link
    return articles_dict
print(feedreader(feed))

