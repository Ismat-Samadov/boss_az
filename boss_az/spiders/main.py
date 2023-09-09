import scrapy


class MainSpider(scrapy.Spider):
    name             = "main"
    allowed_domains  = ["boss.az"]
    start_urls       = ["https://boss.az/vacancies.html?action=index&controller=vacancies&format=html&only_path=true&page=6&search%5Bcategory_id%5D=&search%5Bcompany_id%5D=&search%5Beducation_id%5D=&search%5Bexperience_id%5D=&search%5Bkeyword%5D=&search%5Bregion_id%5D=&search%5Bsalary%5D=&type=vacancies"]


    def parse(self, response):
        links = response.css('results-i-link::attr(href)').getall()

        for link in links:
            yield response.follow(link, self.parse_product, meta={'link': link})

        pagination_links = response.css('nav.pagination span.page a::attr(href)').getall()

        for next_page in pagination_links:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        link = response.request.meta['link']
        yield {
            'Link' : link,
            'Phone': response.css('phone::attr(href)').get(),
        }