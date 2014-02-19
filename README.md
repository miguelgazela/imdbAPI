imdbAPI
=======

![imdbAPI](https://raw.github.com/miguelgazela/imdbAPI/master/imdbAPI.png)

Unofficial Python API for the Internet Movie Database (IMDb).

## Features

## Installation

Right now, the only way to access this package is by manually cloning it.

In the future:

```sh
$ pip install imdbAPI
```

## Usage

```python
from imdb import IMDB

api = IMDB()

# search the movie 'Transformers' and get only the first result
res = api.search_movie('Transformers', lucky=True)
print res['title']

# search the tv show 'Breaking Bad' and print the url of each search result
for res in api.search_tv('Breaking Bad'):
  print res['url']
```

## Examples

## Contribute

If you want to add any new features, improve existing ones and/or the code, feel free to send a pull request.

## Tests
