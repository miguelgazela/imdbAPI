#!/usr/bin/env python

from imdb import IMDB
import json


def main():
    api = IMDB()

    # print api.get_movies_near_you()

    query = raw_input("Search: ")
    # print api.search_movie(query, lucky=True)
    with open('results.json', 'w') as fout:
        fout.write(json.dumps(api.search_videogame(query, lucky=False), indent=1))
    


if __name__ == "__main__":
    main()