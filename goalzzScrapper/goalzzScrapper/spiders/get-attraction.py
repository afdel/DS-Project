from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
from goalzzScrapper.items import GoalzzscrapperItem

class AttractionSpider(BaseSpider):
	name = "get-attraction"
	allowed_domains = ["goalzz.com"]
	start_urls = [
		"http://www.goalzz.com/?region=-1&dd=29&mm=11&yy=2015&doff=-1"
	]
	
	def __init__(self, name=None, **kwargs):
		super(AttractionSpider, self).__init__(name, **kwargs)
		self.items_buffer = {}
		self.base_url = "http://goalzz.com"
		from scrapy.conf import settings
		settings.overrides['DOWNLOAD_TIMEOUT'] = 360

	def parse(self, response):
		print "Start scrapping ..............."
		try:
			#hxs = HtmlXPathSelector(response)


			text = response.xpath('/html/body/center//a')
			print text

			#links = hxs.select("//center/table[2]/tbody/tr/td/table/tbody/tr[position()>2 and position()<9]/td[1]/a/@href")
			#links = response.xpath('//center/table[2]/tbody/tr/td/table/tbody/tr[position()>2 and position()<9]/td[1]/a/@href')

			links = response.xpath('//td[@class="tt"]/a/@href').extract()

			if not links:
				log.msg("No Data to scrap")
				return

			print links

			for link in links:
				v_url = ''.join( link.extract() )
				
				log.msg("*************************** link ****************")
				if not v_url:
					continue
				else:
					_url = self.base_url + v_url
					yield Request( url= _url, callback=self.parse_details )		
		
        		#filename = response.url.split("/")[-2] + '.html'
        		#with open(filename, 'wb') as f:
        		#    f.write(response.body)

		except Exception as e:
			log.msg("Parsing failed for URL {%s}"%format(response.request.url))
			raise 



	def parse_details(self, response):
		print "Start scrapping Detailed Info...."
		try:
			hxs = HtmlXPathSelector(response)
			l_stat = GoalzzscrapperItem()

			v_team = hxs.select("//center/table[2]/tbody/tr/td/table[3]/tbody/tr/td/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[1]/td/table/tbody/tr/td[1]").extract() 
			v_matchId = 1 
			v_date = 1
			v_goals = hxs.select("//center/table[2]/tbody/tr/td/table[3]/tbody/tr/td/table[1]/tbody/tr[1]/td[1]/table/tbody/tr[2]/td[1]").extract()
			
			
                        l_stat["goals"] = v_goals[0].strip()
          
		 	yield l_stat
		except Exception as e:
			log.msg("Parsing failed for URL {%s}"%format(response.request.url))
			raise             







