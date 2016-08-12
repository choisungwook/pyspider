from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from tutorial.items import TutorialItem


class Harvester1(CrawlSpider):
    name = 'Harvester1' 
    session_id = -1
    start_urls = ["http://192.168.47.129"]
    rules = ( Rule (SgmlLinkExtractor(allow=("[^/]*", ),),
                callback="parse_items",  
                follow= True),
    )

    def __init__(self, session_id=-1, *args, **kwargs):
        super(Harvester1, self).__init__(*args, **kwargs)
        self.session_id = session_id

    def parse_items(self, response):        
        sel = Selector(response)
        items = []
        item = TutorialItem()
        item["session_id"] = self.session_id
        item["depth"] = response.meta["depth"]
        item["current_url"] = response.url
        referring_url = response.request.headers.get('Referer', None)
        item["referring_url"] = referring_url
        item["title"] = sel.xpath('//title/text()').extract()
        items.append(item)

        print response

        return items

    def filter_links(self, links):
        baseDomain = self.get_base_domain( self.response_url)
        filteredLinks = []
        for link in links:
            if link.url.find(baseDomain) < 0:
                filteredLinks.append(link)
        return filteredLinks

    def get_base_domain(self, url):
        base = urlparse(url).netloc
        if base.upper().startswith("WWW."):
            base = base[4:]
        elif base.upper().startswith("FTP."):
            base = base[4:]
        # drop any ports
        base = base.split(':')[0]