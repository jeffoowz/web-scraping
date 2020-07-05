import scrapy

class HotelSpider(scrapy.Spider):
    name = 'a'
    allowed_domains = ["travelweekly.com"]
    start_urls = ["https://www.travelweekly.com/Hotels/New-Zealand", ]

    def parse(self, response):
        region_page_links = response.css('div.search-list a')
        yield from response.follow_all(region_page_links, self.parse)

        detail_page_links = response.css('a.title')
        yield from response.follow_all(detail_page_links, self.parse_detail)

        pagination_links = response.css('a.next')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        en = extract_with_css('div.contact a::attr(href)')

        if en == "":
            enc = None
        else:
            enc = en.replace('/cdn-cgi/l/email-protection#', '')

            def decodeEmail(self):
                de = ""
                k = int(self[:2], 16)

                for i in range(2, len(self) - 1, 2):
                    de += chr(int(self[i:i + 2], 16) ^ k)
                return de

        title = extract_with_css('h1.title-xxxl::text')
        address = extract_with_css('div.address::text') + " " + response.xpath('/html/body/form/div[4]/div[2]/div/div[1]/div/div/div[1]/article/div/div[1]/div[1]/text()[2]').get()

        if title is None:
            title = 'Not Found!'
        if address is None:
            address = 'Not Found!'

        yield {
            'name': title,
            'address': address,
            'region': extract_with_css('div.breadcrumb a:nth-child(4)::text'),
            'email': decodeEmail(enc),
            'phone': response.xpath('//*[@id="aspnetForm"]/div[4]/div[2]/div/div[1]/div/div/div[1]/article/div/div[1]/div[2]/text()[2]').get()
        }
