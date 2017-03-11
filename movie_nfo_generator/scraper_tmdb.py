"""The Movie DataBase utilities"""

import tmdbsimple as tmdb
from movie_nfo_generator.config import INI, ini_set
from movie_nfo_generator.utilities import choose_result

if not INI.has_section("TMDB"):
    INI.add_section("TMDB")

if not INI.has_option("TMDB", "API_KEY"):
    API_KEY = ""
    while not API_KEY:
        API_KEY = input('Enter "The Movie Database" API key: ').strip()
    ini_set("TMDB", "API_KEY", API_KEY)
tmdb.API_KEY = INI.get("TMDB", "API_KEY")

LANGUAGE = INI.get("General", "language")


def _search(title, search_method, title_key, date_key, year_query, year):
    """
    Search by title and return TMDB ID

    Args:
        title (str): Media title.
        search_method (str): Search method (movie, tv, ...).
        title_key (str): Key for title.
        date_key (str): Key for date.
        year_query (str): Key for year.
        year (str or int): Year.

    Returns:
        dict: Response.
    """
    search = tmdb.Search()
    results = None
    search_params = {"query": title, "language": LANGUAGE}
    if year:
        search_params[year_query] = int(year)
    while not results:
        getattr(search, search_method)(**search_params)
        results = search.results
        if not results:
            if year_query in search_params:
                del search_params[year_query]
                continue
            search_params["query"] = input("No matching result, enter title: ")

    return choose_result(
        [
            {
                "title": result[title_key],
                "year": result[date_key].split("-", 1)[0],
                "id": result["id"],
            }
            for result in results
        ]
    )


def search_movie(title, year):
    """
    Search a movie by title and return TMDB ID

    Args:
        title (str): Movie title.
        year (int or str): Movie year.

    Returns:
        dict: Response.
    """
    return _search(title, "movie", "title", "release_date", "year", year)


def search_tv_show(title, year):
    """
    Search a TV show by title and return TMDB ID

    Args:
        title (str): TV show title.
        year (int or str): TV show start year.

    Returns:
        dict: Response.
    """
    return _search(title, "tv", "name", "first_air_date", "first_air_date_year", year)


def _response_names_only(response):
    """
    List names only for response in form ID + Name

    Args:
        response (dict): Response.

    Returns:
        list of str: Names.
    """
    return [value["name"] for value in response]


def _crew_member_by_job(credits, job):
    """
    Return names by job

    Args:
        credits (dict): Credits.
        job (str): Job name.

    Returns:
    list of str: Names
    """
    names = []
    job = job.lower()
    add_name = names.append
    for credit in credits["crew"]:
        if credit["job"].lower() == job:
            add_name(credit["name"])
    return names


def get_movie_infos(title, year):
    """
    Return NFO fields and link for a movie.

    Args:
        title (str): Movie title.
        year (int or str): Movie year.

    Returns:
        tuple: Fields, The Movie Database URL.
    """
    tmdb_id = search_movie(title, year)

    movie = tmdb.Movies(tmdb_id)
    infos = movie.info(language=LANGUAGE)
    credits = movie.credits(language=LANGUAGE)

    nfo_fields = {
        "title": infos["title"],
        "originaltitle": infos["original_title"],
        "year": infos["release_date"].split("-", 1)[0],
        "plot": infos["overview"],
        "outline": infos["overview"],
        "tagline": infos["tagline"],
        "genre": _response_names_only(infos["genres"]),
        "studio": _response_names_only(infos["production_companies"]),
        "country": _response_names_only(infos["production_countries"]),
        "director": _crew_member_by_job(credits, "director"),
        "credits": _crew_member_by_job(credits, "novel"),
    }

    return nfo_fields, f"https://www.themoviedb.org/movie/{tmdb_id}"


def get_tv_show_infos(title=None, year=None, tmdb_id=None):
    """
    Return NFO fields and link for a TV show.

    Args:
        title (str): TV show title.
        year (int or str): TV show start year.
        tmdb_id (str): The Movie Database ID.

    Returns:
        tuple: Fields, The Movie Database URL, The Movie Database ID, original language
    """
    if not tmdb_id:
        tmdb_id = search_tv_show(title, year)

    serie = tmdb.TV(tmdb_id)
    infos = serie.info(language=LANGUAGE)

    nfo_fields = {
        "title": infos["name"],
        "originaltitle": infos["original_name"],
        "plot": infos["overview"],
        "outline": infos["overview"],
        "premiered": infos["first_air_date"],
        "studio": _response_names_only(infos["production_companies"]),
        "genre": _response_names_only(infos["genres"]),
    }

    return (
        nfo_fields,
        f"https://www.themoviedb.org/tv/{tmdb_id}",
        tmdb_id,
        infos["original_language"],
    )


def get_tv_episode_infos(tmdb_id, season_num, episode_num, original_language):
    """
    Return NFO fields and link for a TV episode.

    Args:
        tmdb_id (str): The Movie Database ID.
        season_num (int): Season number.
        episode_num (int): Episode Number.
        original_language (str): Original language.

    Returns:
        tuple: Fields, The Movie Database URL.
    """

    episode = tmdb.TV_Episodes(tmdb_id, season_num, episode_num)
    infos = episode.info(language=LANGUAGE)
    original_info = episode.info(language=original_language)

    nfo_fields = {
        "title": infos["name"],
        "originaltitle": original_info["name"],
        "season": infos["season_number"],
        "episode": infos["episode_number"],
        "plot": infos["overview"],
        "aired": infos["air_date"],
    }

    return (
        nfo_fields,
        f"https://www.themoviedb.org/tv/{tmdb_id}"
        f"/season/{season_num}/episode/{episode_num}",
    )
