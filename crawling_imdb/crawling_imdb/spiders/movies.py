from scrapy.spiders import CrawlSpider

codes_regions = []

class Crawling_ReleaseCalendar(CrawlSpider):
    name = "Crawler_ReleaseCalendar"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/calendar/"]

    
    """ 
    Scraping beggening page, take code regions, pass urls regions in next func "parse_movies" 
    Parse info for movies 
    """

    def parse_start_url(self, response):

        # parse code region
        regions = response.css("#country-selector option::attr(value)").getall()
        codes_regions.extend(regions)         

        # parse all url release calendar regions 
        for code in codes_regions:  
            url = r"https://www.imdb.com/calendar/\?ref_=rlm&region=" + code + "&type=MOVIE"

            # pass urls regions in next func
            yield response.follow(url, callback=self.parse_movies)


    # parse info for movies
    def parse_movies(self, response):

        region = response.css(".ipc-simple-select__selected-option::text").get()
        block_movies = response.css(".ipc-metadata-list.ipc-metadata-list--dividers-after.sc-48add019-2.hqwybd.ipc-metadata-list--base")

        for movies in block_movies:
            
            title = movies.css(".ipc-metadata-list-summary-item__t::text").get()
            genre = movies.css(".ipc-inline-list.ipc-inline-list--show-dividers.ipc-inline-list--no-wrap.ipc-inline-list--inline.ipc-metadata-list-summary-item__tl.base > li > span::text").getall()
            actors = movies.css(".ipc-inline-list.ipc-inline-list--show-dividers.ipc-inline-list--no-wrap.ipc-inline-list--inline.ipc-metadata-list-summary-item__stl.base > li > span::text").getall()
            img = movies.css(".ipc-media.ipc-media--poster-27x40.ipc-image-media-ratio--poster-27x40.ipc-media--base.ipc-media--custom.ipc-poster__poster-image.ipc-media__img > img::attr(src)").get()
            url = movies.css(".ipc-metadata-list-summary-item__t::attr(href)").get()
            

            yield {
                "region": region,    
                "title": title,
                "genre": genre,
                "actors": actors,
                "img": img,
                "url": url
            }


class BaseCrawler(CrawlSpider):
    allowed_domains = ["imdb.com"]

    def parse_movie(self, movie):

        title = movie.css(".ipc-title__text::text").get()
        rating = movie.css(".ipc-rating-star.ipc-rating-star--base.ipc-rating-star--imdb.ratingGroup--imdb-rating::text").get()
        img = movie.css(".ipc-image::attr(src)").get()
        url = movie.css(".ipc-lockup-overlay.ipc-focusable::attr(href)").get()
        data = movie.css(".sc-14dd939d-5.cPiUKY.cli-title-metadata > span::text").getall()


        return {
            "title": title,
            "rating": rating,
            "data": data,
            "url": url,
            "img": img
        }


class Crawling_Top250Movies(BaseCrawler):

    name = "Crawler_Top250Movies"
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    def parse_start_url(self, response):
        movies = response.css(".ipc-metadata-list-summary-item.sc-bca49391-0.eypSaE.cli-parent")

        for movie in movies:
            yield self.parse_movie(movie)


class Crawling_MostPopularMovies(BaseCrawler):
    name = "Crawler_MostPopularMovies"
    start_urls = ["https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"]

    def parse_start_url(self, response):
        block_movies = response.css(".ipc-metadata-list-summary-item.sc-bca49391-0.eypSaE.cli-parent")

        for block in block_movies:
            yield self.parse_movie(block)