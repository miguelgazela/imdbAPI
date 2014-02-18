#!/usr/bin/env python

from imdb import IMDB


def main():
    api = IMDB()

    print api.get_movies_near_you()

    # query = raw_input("Search: ")
    # print len(api.search_movie(query))


if __name__ == "__main__":
    main()