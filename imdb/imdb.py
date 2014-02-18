from utils import get_soup
from constants import SEARCH_MOVIE_TITLE

class IMDB(object):
    """
    Class that parses the IMDb pages and returns the request data
    """

    def get_movies_near_you(self):
        """
        Returns the list of movies playing near you, including the theaters
        and showtimes for each movie
        """

        soup = get_soup('/showtimes/')
        list_movies = soup.find_all(class_='list_item')
        movies = []

        for item in list_movies:
            movie = {}

            page = item.find('a')['href']
            soup = get_soup(page)
            movie_info = soup.select('.article > .article .overview-top')[0]
            
            # fill in the movie info
            movie['title'] = movie_info.h4.a.text
            movie['url'] = movie_info.h4.a['href']
            movie['runtime'] = movie_info.p.time.text
            movie['ratingValue'] = movie_info.select(
                '.rating_txt meta[itemprop="ratingValue"]')[0]['content']
            movie['description'] = movie_info.select('.outline')[0]\
                .text.strip()

            # add the list of theaters where the movie is playing
            movie['theaters'] = []
            list_theaters = soup.find_all(class_='list_item')

            for item in list_theaters:
                theater = {}
                theater['name'] = item.select('h3 > a > span')[0].text
                theater['address'] = item.select(
                    '.address span[itemprop="streetAddress"]')[0].text
                theater['city'] = item.select(
                    '.address span[itemprop="addressLocality"]')[0].text
                theater['postalCode'] = item.select(
                    '.address span[itemprop="postalCode"]')[0].text
                theater['phone'] = item.select(
                    '.address span[itemprop="telephone"]')[0].text

                # add today's showtimes
                showtimes = item.find(class_='showtimes').select(
                    'meta[itemprop="startDate"]')
                theater['showtimes'] = [x['content'] for x in showtimes]

                movie['theaters'].append(theater)

            movies.append(movie)
        return movies


    def search_movie(self, query):
        """
        Returns the list of results of a movie search, each one
        containing the image, title and link to its imdb page
        """
        soup = get_soup(SEARCH_MOVIE_TITLE, {'q': query})
        results = []

        for item in soup.find_all(class_="findResult"):
            result = {}
            result['text'] = item.find('td', class_="result_text").text.strip()
            result['url'] = item.find('td', class_="result_text").a['href']
            result['image'] = item.find('td', class_="primary_photo").a.img['src']
            results.append(result)

        return results


    def search_tv_show(self, query):
        """
        Returns the list of results of a tv show sarch, each one
        containing the image, title and url to its imdb page
        """
        pass
