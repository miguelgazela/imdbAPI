from utils import get_soup
from constants import SEARCH_MOVIE, SEARCH_TV_SHOW

class IMDB(object):
    """
    Class that parses the IMDb pages and returns the request data
    """

    def search_movie(self, query, lucky=False):
        """
        Returns the list of results of a movie search, each one
        containing the primary image, title and link to its imdb page
        """
        soup = get_soup(SEARCH_MOVIE, {'q': query})
        results = []

        # returns the first result immediately if lucky is True
        if lucky:
            first = soup.find(class_="findResult")
            results.append(self._search_results_parser(first))
        else:
            for item in soup.find_all(class_="findResult"):
                results.append(self._search_results_parser(item))

        return results


    def _search_results_parser(self, findResult):
        """
        Parses the information about a movie contained in a search result item
        and returns an object with it
        """
        result = {}
        result['text'] = findResult.find('td', 
            class_="result_text").text.strip()
        result['url'] = findResult.find('td',
            class_="result_text").a['href']
        result['image'] = findResult.find('td',
            class_="primary_photo").a.img['src']
        return result

    def search_tv(self, query, lucky=False):
        """
        Returns the list of results of a tv show sarch, each one
        containing the image, title and url to its imdb page
        """
        soup = get_soup(SEARCH_TV_SHOW, {'q': query})
        results = []

        if lucky:
            first = soup.find(class_="findResult")
            results.append(self._search_results_parser(first))
        else:
            for item in soup.find_all(class_="findResult"):
                results.append(self._search_results_parser(item))

        return results

    def get_movie(self, movieID):
        """
        Returns a movie object with all the info contained 
        in its imdb page
        """
        pass

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

                # parse address anc contact info
                properties = [
                    ('address', 'streetAddress'), ('city', 'addressLocality'), 
                    ('postalCode', 'postalCode'), ('phone', 'telephone'),
                ]
                for obj_prop, item_prop in properties:
                    theater[obj_prop] = item.select(
                        '.address span[itemprop="%s"]' % item_prop
                    )[0].text

                # add today's showtimes
                showtimes = item.find(class_='showtimes').select(
                    'meta[itemprop="startDate"]')
                theater['showtimes'] = [x['content'] for x in showtimes]

                movie['theaters'].append(theater)

            movies.append(movie)
        return movies

