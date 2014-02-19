#!/usr/bin/env python

from imdb import IMDB


def main():
    api = IMDB()

    # print api.get_movies_near_you()

    query = raw_input("Search: ")
    print api.search_movie(query, lucky=True)


if __name__ == "__main__":
    main()