from fake_useragent import UserAgent
from scrapy.crawler import CrawlerRunner
from crawling_imdb.crawling_imdb.spiders.movies import ReleaseCalendar, Top250Movies, MostPopularMovies
from crawling_imdb.crawling_imdb.spiders.movies import TopBoxOfficeUS, MovieNews, IndiaMovieSpotlight, BrowseByGenre
from twisted.internet import reactor, defer


""" 
    File for start scraper asynsio and save in json file 
    Using library 'twisted' we run callback as soon as possible 
"""


fake_user_agent = UserAgent()
USER_AGENT = fake_user_agent.random


# settings for crawlers
runner_release_calendar = CrawlerRunner(settings={
    'FEEDS': {
        'results_calendar.json': {
            'format': 'json',
        },
    },
    'USER_AGENT': USER_AGENT,  
})

runner_most_popular_movies = CrawlerRunner(settings={
    'FEEDS': {
        'results_PopularMovies.json': {
            'format': 'json',
        },
    },
    'USER_AGENT': USER_AGENT,  
})

runner_top250Movies = CrawlerRunner(settings={
    'FEEDS': {
        'results_top250Movies.json': {
            'format': 'json',
        },
    },
    'USER_AGENT': USER_AGENT,  
})

runner_topBoxOfficeUs = CrawlerRunner(settings={
    'FEEDS': {
        'results_topBoxOfficeUs.json': {
            'format': 'json',
        },
    },
    'USER_AGENT': USER_AGENT,  
})

runner_MovieNews = CrawlerRunner(settings={
    'FEEDS': {
        'results_MovieNews.json': {
            'format': 'json',
        },
    },
    'USER_AGENT': USER_AGENT,  
})

runner_IndiaMovieSpotlight = CrawlerRunner(settings={
    'FEEDS': {
        'results_IndiaMovieSpotlight.json': {
            'format': 'json',
        },
    },
    'USER_AGENT': USER_AGENT,  
})

runner_BrowseByGenre = CrawlerRunner(settings={
    'FEEDS': {
        'results_BrowseByGenre.json': {
            'format': 'json',
        },
    },
    'USER_AGENT': USER_AGENT,  
})


# launch scrapers parallel
d_release_calendar = runner_release_calendar.crawl(ReleaseCalendar)
d_most_popular_movies = runner_most_popular_movies.crawl(MostPopularMovies)
d_top250Movies = runner_top250Movies.crawl(Top250Movies)
d_topBoxOfficeUs = runner_topBoxOfficeUs.crawl(TopBoxOfficeUS)
d_moviesNews = runner_MovieNews.crawl(MovieNews)
d_IndiaMovieSpotlight = runner_IndiaMovieSpotlight.crawl(IndiaMovieSpotlight)
d_BrowseByGenre = runner_BrowseByGenre.crawl(BrowseByGenre)


# Wait... until both scrapers complete
deferred_list = defer.DeferredList([d_release_calendar, d_most_popular_movies, d_top250Movies, d_topBoxOfficeUs, d_topBoxOfficeUs, d_moviesNews, d_IndiaMovieSpotlight, d_BrowseByGenre])

# After the completion of both scrapers, we stop the reactor
deferred_list.addBoth(lambda _: reactor.stop())

# Launch reactor
reactor.run()