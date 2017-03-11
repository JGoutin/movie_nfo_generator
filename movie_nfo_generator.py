# J.GOUTIN 2017
""".NFO file generator for movies and series"""
from configparser import ConfigParser
from lxml.etree import Element, SubElement, ElementTree
import tmdbsimple as tmdb

# Get configuration file
INI = ConfigParser()
INI.read('config.ini')

def ini_set(*args, **kwargs):
    """Set config and save ini file"""
    INI.set(*args, **kwargs)
    with open('config.ini', 'wt') as ini_file:
        INI.write(ini_file)

# The Movie Database configuration
if not INI.has_section('TMDB'):
    # Initialize section
    INI.add_section('TMDB')

if not INI.has_option('TMDB', 'API_KEY'):
    # Initialize API key
    value = ''
    while not value:
        value = input('Enter "The Movie Database" API key: ').strip()
    ini_set('TMDB', 'API_KEY', value)

if not INI.has_option('TMDB', 'language'):
    # Initialize API language
    value = ''
    while not value:
        value = input('Enter language code (ISO 639-1): ').strip()
    ini_set('TMDB', 'language', value)
    
language = INI.get('TMDB', 'language')
tmdb.API_KEY = INI.get('TMDB', 'API_KEY')

# The Movie Database search functions

def _search(title, search_method, title_key, date_key):
    """Search by title and return TMDB ID"""
    # Search by title
    search = tmdb.Search()
    getattr(search, search_method)(query=title, language=language)

    # Get result
    results = search.results
    results_cnt = len(results)
    if not results_cnt:
        # No result
        return None

    elif results_cnt == 1:
        # Only one result
        result = results[0]
        print(f'One matching result: {result[title_key]} ({result[date_key].split("-", 1)[0]})')
        return result["id"]

    else:
        # Many results, let user choose the best one
        print('Many matching results, choose one :')
        id_list = []
        for i, result in enumerate(results):
            id_list.append(result["id"])
            print(f'{i + 1:3d}: {result[title_key]} ({result[date_key].split("-", 1)[0]})')

        choice = ''
        while not choice:
            choice = input('Enter number: ').strip()
            try:
                choice = int(choice)
            except Exception:
                choice = ''
                continue
            if choice < 1 or choice > len(id_list):
                choice = ''
                continue

        return id_list[choice - 1]

def search_movie(title):
    """Search a movie by title and return TMDB ID"""
    return _search(title, 'movie', 'title', 'release_date')

def search_serie(title):
    """Search a TV serie by title and return TMDB ID"""
    return _search(title, 'tv', 'name', 'first_air_date')

# The Movie Database help functions

def tmdb_response_names(response):
    """List names only for response in form ID + Name"""
    return [value['name'] for value in response]

def tmdb_crew_by_job(credits, job):
    """Return names by job"""
    names = []
    job = job.lower()
    add_name = names.append
    for credit in credits['crew']:
        if credit['job'].lower() == job:
            add_name(credit['name'])
    return names

# Create Nfo functions

def _write_nfo(root_name, nfo_fiels, filename, link=''):
    """Write nfo file"""
    # Create root
    nfo_root = Element(root_name)

    # Create fields
    for field_name in nfo_fiels:
        values = nfo_fiels[field_name]
        if not values:
            continue
        if not isinstance(values, list):
            values = [values]
        for value in values:
            SubElement(nfo_root, field_name).text = value

    # Write file
    ElementTree(nfo_root).write(filename, encoding='utf-8', xml_declaration=True, pretty_print=True)

    # Add link
    if link:
        with open(filename, 'at') as nfo_file:
            nfo_file.write(link)  
    print(f'"{filename}" successfully created...')

def nfo_movie(tmdb_id, movie_set='', sorttitle=''):
    """Create a NFO file for a movie."""
    # Movie infos from TMDB
    movie = tmdb.Movies(tmdb_id)
    infos = movie.info(language=language)
    credits = movie.credits(language=language)

    # Nfo fields
    nfo_fiels = {'title' : infos['title'],
                 'originaltitle': infos['original_title'],
                 'year': infos['release_date'].split("-", 1)[0],
                 'plot': infos['overview'],
                 'outline': infos['overview'],
                 'tagline': infos['tagline'], 
                 'genre': tmdb_response_names(infos['genres']),
                 'studio': tmdb_response_names(infos['production_companies']),
                 'country': tmdb_response_names(infos['production_countries']),
                 'sorttitle': sorttitle,
                 'set': movie_set,
                 'director': tmdb_crew_by_job(credits, 'director'),
                 'credits': tmdb_crew_by_job(credits, 'novel')}

    # Write file
    _write_nfo('movie', nfo_fiels, 'file.nfo', link=f'http://www.themoviedb.org/movie/{tmdb_id}')


#TEST
a = search_movie("bladerunner")
nfo_movie(a)