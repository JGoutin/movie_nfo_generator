"""Configuration file"""
from configparser import ConfigParser
from os.path import exists, expanduser, expandvars, join
import os
from os import chmod, getenv, makedirs

APP_NAME = expanduser("movie_nfo_generator")
if os.name == "nt":
    CONFIG_DIR = join(expandvars("%APPDATA%"), APP_NAME)
else:
    CONFIG_DIR = join(getenv("XDG_CONFIG_HOME", expanduser("~/.config")), APP_NAME)
makedirs(CONFIG_DIR, exist_ok=True)
chmod(CONFIG_DIR, 0o700)

CONFIG_FILE = join(CONFIG_DIR, "config.ini")

INI = ConfigParser()
INI.read(CONFIG_FILE, encoding="utf-8")


def ini_set(*args, **kwargs):
    """Set config and save ini file"""
    INI.set(*args, **kwargs)
    with open(CONFIG_FILE, "wt", encoding="utf-8") as ini_file:
        INI.write(ini_file)


if not INI.has_section("General"):
    INI.add_section("General")
if not INI.has_section("Movies"):
    INI.add_section("Movies")
if not INI.has_section("Tv Shows"):
    INI.add_section("Tv Shows")

if not INI.has_option("General", "formats"):
    ini_set("General", "formats", ".mkv .mk3d")

if not INI.has_option("General", "language"):
    LANGUAGE = ""
    while not LANGUAGE:
        LANGUAGE = input("Enter language code (ISO 639-1): ").strip()
    ini_set("General", "language", LANGUAGE)

if not INI.has_option("Movies", "path"):
    PATH = ""
    while not PATH:
        PATH = input("Enter movies path: ").strip()
        if not exists(PATH):
            PATH = ""
    ini_set("Movies", "path", PATH)

if not INI.has_option("Tv Shows", "path"):
    PATH = ""
    while not PATH:
        PATH = input("Enter tv shows path: ").strip()
        if not exists(PATH):
            PATH = ""
    ini_set("Tv Shows", "path", PATH)
