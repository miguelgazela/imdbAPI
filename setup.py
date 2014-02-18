from setuptools import setup

setup(
    name="imdbAPI",
    author="Miguel Oliveira",
    author_email="miguel.gazela@gmail.com",
    version='0.1.1',
    tests_require=['pytest'],
    install_requires=['BeautifulSoup4>=4.3.2', 
                    'requests>=2.2.1',
                    ],
    packages=['imdb'],
    license='The MIT License (MIT)',
    description='Unofficial Python API for the Internet Movie Database (IMDb)',
    long_description=open('README.md').read(),
    extras_require={
        'testing': ['pytest'],
    }
)