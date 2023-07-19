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


""" Creating a basic crawler and using its tags for other urls """

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


class Crawling_TopBoxOfficeUS(BaseCrawler):
    name = "Crawler_TopBoxOfficeUS"
    start_urls = ["https://www.imdb.com/chart/boxoffice/?ref_=nv_ch_cht"]

    def parse_start_url(self, response):
        block_movies = response.css(".ipc-metadata-list-summary-item.sc-bca49391-0.eypSaE.cli-parent")

        for block in block_movies:
            movie_data = self.parse_movie(block)

            data = block.css(".sc-ee64acb1-0.kCMURQ.sc-14dd939d-8.ipueKh > li > span::text").getall()
            movie_data["data"] = data
            
            yield movie_data


#TODO scroll more 
class Crawling_MovieNews(BaseCrawler):
    name = "Crawler_MovieNews"
    start_urls = ["https://www.imdb.com/news/movie/?ref_=nv_nw_mv"]


    def parse_start_url(self, response):
        news = response.css(".ipc-list-card--border-line.ipc-list-card.sc-bec740f7-0.QvRgg.ipc-list-card--base")

        for new in news:
            title = new.css(".ipc-link.ipc-link--base.sc-bec740f7-3.dKUtuz::text").get()
            url = new.css(".ipc-link.ipc-link--base.sc-bec740f7-3.dKUtuz::attr(href)").get()
            description = new.css(".ipc-html-content-inner-div::text").getall()
            data = new.css(".ipc-inline-list.ipc-inline-list--show-dividers.ipc-inline-list--inline.sc-bec740f7-14.hptXtT.base > li::text").getall()
            img = new.css(".ipc-image::attr(src)").get()

            yield {
                "title": title,
                "url": url,
                "description": description,
                "data": data,
                "img": img
            }


class Crawling_IndiaMovieSpotlight(CrawlSpider):
    name = "Crawler_IndiaMovieSpotlight"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/india/toprated/?ref_=nv_mv_in"]

    def parse_start_url(self, response):
    
        blocks_top = response.css(".ipc-page-section.ipc-page-section--base.sc-48edd91f-0.dOPmaK")

        for block in blocks_top:
            title_top = block.css(".ipc-title__text::text").get()
            title_movie = block.css('span[data-testid="title"]::text').getall()
            rating = block.css(".ipc-rating-star.ipc-rating-star--base.ipc-rating-star--imdb.ipc-rating-star-group--imdb::text").getall()
            img = block.css(".ipc-image::attr(src)").getall()
            url = block.css(".ipc-lockup-overlay.ipc-focusable::attr(href)").getall()

            yield {
                "title_top": title_top,
                "title_movie": title_movie,
                "rating": rating,
                "img": img,
                "url": url
            }