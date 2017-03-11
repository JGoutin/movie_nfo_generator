#!/usr/bin/env python3
""".NFO file generator for movies and series"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from os import walk
from os.path import relpath, basename, splitext, join, exists
from threading import Lock

from requests import HTTPError

from os.path import dirname, realpath
import sys

sys.path.insert(0, dirname(dirname(realpath(__file__))))

from movie_nfo_generator.config import INI
import movie_nfo_generator.scraper_tmdb as tmdb
from movie_nfo_generator.nfo import write_nfo
from movie_nfo_generator.utilities import (
    choose_title,
    filter_filename,
    filepath_to_titles,
    filepath_to_episode_id,
)


_UI_LOCK = Lock()
_workers = ThreadPoolExecutor(max_workers=2)

#: Media formats
FORMATS = [_format.lower().strip() for _format in INI.get("General", "formats").split()]


def nfo_movie(media_filepath, movie_set="", sorttitle=""):
    """
    Create a NFO file for a movie.

    Args:
        media_filepath (str): Movie file path.
        movie_set (str): Movie set name.
        sorttitle (str): Sort title.
    """
    short_title, long_title, year = filepath_to_titles(
        media_filepath, True if movie_set else False
    )

    nfo_fields, nfo_link = tmdb.get_movie_infos(short_title, year)

    with _UI_LOCK:
        print(f'Creating NFO file for "{media_filepath}"')
        nfo_fields["title"] = choose_title(long_title, nfo_fields["title"])
    nfo_fields["set"] = movie_set
    nfo_fields["sorttitle"] = sorttitle

    write_nfo("movie", nfo_fields, media_filepath, link=nfo_link)


def nfo_tv_show(media_filedir):
    """
    Create a NFO file for a serie.

    Args:
        media_filedir (str): Serie directory path.
    """
    title, _, year = filepath_to_titles(media_filedir)

    nfo_fields, nfo_link, scraper_id, original_language = tmdb.get_tv_show_infos(
        title, year
    )

    with _UI_LOCK:
        print(f'Creating NFO file for "{media_filedir}"')
        nfo_fields["title"] = choose_title(title, nfo_fields["title"])

    write_nfo("tvshow", nfo_fields, media_filedir, link=nfo_link, filename="tvshow.nfo")

    return scraper_id, original_language


def nfo_tv_episode(scraper_id, media_filepath, original_language, number):
    """
    Create a NFO file for a serie.

    Args:
        scraper_id:
        media_filepath (str): Episode file path.
        original_language (str): Language
        number (int): Episode number.
    """

    name, season_num, episode_num = filepath_to_episode_id(media_filepath, True)

    nfo_fields, nfo_link = tmdb.get_tv_episode_infos(
        scraper_id, season_num, episode_num, original_language
    )

    with _UI_LOCK:
        print(f'Creating NFO file for "{media_filepath}"')
        nfo_fields["title"] = choose_title(name, nfo_fields["title"])
    nfo_fields["displayepisode"] = str(number)
    nfo_fields["displayseason"] = "1"

    write_nfo("episodedetails", nfo_fields, media_filepath, link=nfo_link)


def walk_movies():
    """Walk movies"""

    movie_path = INI.get("Movies", "path")
    print("Looking for movies...")
    futures = []
    for root, _, files in walk(movie_path):
        i = 0
        for file in sorted(files, key=str.lower):
            media_filename, ext = splitext(file)
            if ext.lower() not in FORMATS:
                continue

            i += 1
            movie_set = filter_filename(basename(relpath(root, movie_path)))
            sorttitle = f"{movie_set} {i}" if movie_set else ""

            # path
            media_filepath = join(root, media_filename)
            if not exists(f"{media_filepath}.nfo"):
                futures.append(
                    _workers.submit(
                        nfo_movie,
                        media_filepath,
                        movie_set=movie_set,
                        sorttitle=sorttitle,
                    )
                )

    for future in as_completed(futures):
        future.result()
    print("All movies have NFO...")


def walk_tv_shows():
    """Walk TV shows"""

    tv_shows_path = INI.get("Tv Shows", "path")
    print("Looking for TV shows...")
    for root, _, files in walk(tv_shows_path):
        tv_show = filter_filename(basename(relpath(root, tv_shows_path)))
        if not tv_show:
            continue

        nfo_file = join(root, "tvshow.nfo")
        if not exists(nfo_file):
            scraper_id, original_language = nfo_tv_show(root)
        else:
            with open(nfo_file, "rt") as file:
                url = file.read().rsplit("</tvshow>", 1)[1]
            try:
                scraper_id = url.rsplit("/", 1)[1]
            except IndexError:
                continue

            original_language = None

        number = 0
        futures = []
        for file in sorted(files, key=str.lower):
            media_filename, ext = splitext(file)
            if ext.lower() not in FORMATS:
                continue

            number += 1
            media_filepath = join(root, media_filename)
            if not exists(f"{media_filepath}.nfo"):

                if original_language is None:
                    original_language = tmdb.get_tv_show_infos(tmdb_id=scraper_id)[-1]

                futures.append(
                    _workers.submit(
                        nfo_tv_episode,
                        scraper_id,
                        media_filepath,
                        original_language,
                        number,
                    )
                )

        for future in as_completed(futures):
            try:
                future.result()
            except HTTPError as exception:
                if "404" not in str(exception):
                    raise
                else:
                    print(exception)

    print("All TV shows have NFO...")


def _run_command():
    """Entrypoint"""
    walk_movies()
    walk_tv_shows()


if __name__ == "__main__":
    _run_command()
