import scrapy
class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries: 
            name = country.xpath(".//text()").get() #to use xpath from response object-> use .//
            link = country.xpath(".//@href").get()  #to get string use .get()

            #absolute_url = f"https://www.worldometers.info{link}"  #----> manual way to convert relative URL to absolute URL
            #absolute_url = response.urljoin(link) #----> autmatically converts relative URL to absolute URL

            #yield scrapy.Request(url = absolute_url)   #---> needs absoulte url
            yield response.follow(url = link, callback = self.parse_country, meta = {'country_name':name})    #---> takes in relative url and automatically converts to absolute URL

    def parse_country(self, response):
        name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows: 
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            
            yield {
                'country_name':name,
                'year': year,
                'population' : population
            }
