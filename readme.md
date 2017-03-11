[![PyPI](https://img.shields.io/pypi/v/movie_nfo_generator.svg)](https://pypi.org/project/movie_nfo_generator)

# Movie NFO generator

Kodi NFO generator is a simple command line tool to generate NFO files for all movies
and TV show of a Kodi media library.

The aim of this tool is to keep a structure in the Kodi library that match the 
filesystem media structure (Including custom movies sets and episodes ordering).

Features list:

* Allow to define custom movies sets.
* Allow to define a custom display order for movies sets.
* Allow to define any custom TV shows episodes display order and ignore seasons (
  For instance to reorder episodes of a season to match the story timeline, or insert
  specials episodes between season episodes).
* Avoid bad media information by asking user to confirm the media to use if multiple
  results exists.
* Allow user to select between filename title, scrapper title or to type a new title.
* Generates a NFO files containing minimal information for each media.
* Generated NFO also contain a scrapper link to help Kodi to find missing information
  (Does not work for TV shows, Kodi only displays the minimal information even with the
  link).

## Media structure on the file system

This tool works with a specific media structure on the file system.

## Movies

All movies are stored in a same folder with names like `MOVIE_TITLE [RELEASE_YEAR].EXT`.

- `MOVIE_TITLE` is the Movie title.
- `RELEASE_YEAR` is the release year of the movie.
- `EXT` is the file format extension (`.mkv`, ...)

### Movies sets

Movies set are stored in subfolders with the name of the set. Movies in a set can
be prefixed to customize the movies ordering.
This give a format like:

`SET_TITLE/ORDER_PREFIX - TITLE [RELEASE_YEAR].EXT`

- `SET_TITLE` is the set title.
- `ORDER_PREFIX` is the ordering prefix. It is optional and is only required when
  the wished movie order is different from the filenames alphanumerical order.
  This prefix can be something like `SET_TITlE NUMBER`, `Episode NUMBER` or any other
  string.

## TV Shows

All TV shows are stored in a same folder. Each TV show is a directory with name like 
`TV_SHOW_TITLE [RELEASE_YEAR]`.

- `TV_SHOW_TITLE` is the TV Show title.
- `RELEASE_YEAR` is the release year of the first episode of the TV show.

Inside TV show folders, episodes are stored with names like:

`ORDER_PREFIX - EPISODE_TITLE.SXXEXX.EXT`

- `ORDER_PREFIX` is the ordering prefix. Like for movies it allows to set the order of
  episodes to display. This prefix can be something like `TV_SHOW_TITLE NUMBER` or 
  `TV_SHOW_TITLE SXXEXX`.
- `SXXEXX` is the aired season/episode numbers (For instance, `S01E02` for the second 
  episode of the first season). It is used by the scrapper to find what episode it is
  (Scrappers ignore episode titles). It must match the aired season/episode numbers in
  the scrapper.

## Usage

First install the utility:
```bash
pip install movie_nfo_generator
```

Then run the utility:
```bash
movie_nfo_generator
```
On the first run, the utility will ask you for various information like
* The language code to use for media information (For instance: `en`, `fr`)
* Paths of your movie and your TV shows directories.
* Your API key on The Movie Database (Used to retrieve information). You can request an
  API key by logging in to your account on TMDb and clicking the "API" link in the left
  hand side bar of your account page.

On futures runs, no more information are required.

The utility will generates NFO files only for medias with no existing NFO file.

By default, the utility only look for MKV files. You can add support to more formats
by editing the `formats` in the configuration file
`~/.config/movie_nfo_generator/config.ini`.
