from setuptools import setup

with open('README.md', encoding="utf-8") as f:
    long_description = f.read()

setup(
    name = 'CENIPA_API',
    version = '0.0.1',
    description = 'Data about the NBA All-Time points leaders table.',
    long_description = long_description,
    long_description_content_type='text/markdown',
    author = 'Ana Beatriz Macedo',
    author_email = '<anabeatrizmacedo241@gmail.com>', 
    packages = ['NBA_AllTimePTS'],
    license= 'MIT',
    keywords = ['API', 'NBA', 'Basketball', 'Points', 'LeBron James','Assists','Player', 'Sports'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English (United States)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Topic :: Database',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    url = 'https://github.com/AnabeatrizMacedo241/NBA_analysis'
)