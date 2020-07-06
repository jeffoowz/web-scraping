import scrapy


class ParttimeSpider(scrapy.Spider):
    name = 'pt'
    start_urls = ['http://parttime.hk/information-communication-technology-jobs.aspx']

    def parse(self, response):
        detail_page_links = response.css('a.res-jobtitle')
        yield from response.follow_all(detail_page_links, self.parse_detail)

        for i in range(10):
            pagination_links = response.css('#pagination li:nth-child(8) a')
            yield from response.follow_all(pagination_links, self.parse)

    def parse_detail(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'Title': extract_with_css('h1::text'),
            'Employer': extract_with_css('#mainContent_summary_lblSummaryAdvertiser::text'),
            'PostedDate': extract_with_css('#mainContent_summary_lblSummaryDatePosted::text'),
            'Category': extract_with_css('#mainContent_summary_linkSummaryCategory::text'),
            'Salary': extract_with_css('#mainContent_summary_lblSummarySalary::text'),
            'Location': extract_with_css('#mainContent_summary_linkLocation::text'),
            'WorkType': extract_with_css('#mainContent_summary_linkWorkType::text'),
            'link': response.url
        }