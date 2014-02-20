#!/usr/bin/env python

from utils import get_soup
import constants as const
import re

class IMDB(object):
    """
    Class that parses the IMDb pages and returns the request data
    """

    def _category_search(self, category_url, query, lucky):
        """
        Returns a list of results of a category search on imdb.
        Each result consists of an dictionary containing the
        primary image, title, link to the result's imdb page 
        and its id.
        """
        results = []
        soup = get_soup(category_url, {'q': query})

        if lucky: # returns only the first search result
            first = soup.find(class_="findResult")
            results.append(self._search_title_results_parser(first))
        else:
            for item in soup.find_all(class_="findResult"):
                results.append(self._search_title_results_parser(item))

        return results


    def _search_title_results_parser(self, findResult):
        """
        Parses the information contained in a search result item
        and returns a dictionary with it.
        """

        return {
            'text': findResult.find('td', class_="result_text").text.strip(),
            'url': findResult.find('td', class_="result_text").a['href'],
            'image': findResult.find('td', class_="primary_photo").a.img['src'],
            'id': re.search('^/[a-z]{1,}/[a-z]{2}(\d+)/.*$', 
                            result['url']).group(1)
        }


    def search_name(self, query, lucky=False):
        """
        Returns the list of results of a search by the name
        of an actor, writer, director, etc.
        """
        return self._category_search(const.SEARCH_NAME, query, lucky)


    def search_title(self, query, lucky=False):
        """
        Returns the list of results of a search by title.
        """
        return self._category_search(const.SEARCH_TITLE, query, lucky)


    def search_movie(self, query, lucky=False):
        """
        Returns the list of results of a movie search.
        """
        return self._category_search(const.SEARCH_MOVIE, query, lucky)


    def search_tv(self, query, lucky=False):
        """
        Returns the list of results of a tv search.
        """
        return self._category_search(const.SEARCH_TV, query, lucky)


    def search_videogame(self, query, lucky=False):
        """
        Returns the list of results of a videogame search.
        """
        return self._category_search(const.SEARCH_VIDEOGAME, query, lucky)


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
            page = item.find('a')['href']
            soup = get_soup(page)
            movie_info = soup.select('.article > .article .overview-top')[0]
            
            # fill in the movie info
            movie = {
                'title': movie_info.h4.a.text,
                'url': movie_info.h4.a['href'],
                'runtime': movie_info.p.time.text,
                'ratingValue': movie_info.select(
                    '.rating_txt meta[itemprop="ratingValue"]')[0]['content'],
                'description': movie_info.select('.outline')[0].text.strip()
            }

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

