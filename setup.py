#!/usr/bin/env python3
"""Setup script

run "./setup.py --help-commands" for help.
"""
from os.path import abspath, dirname, join

PACKAGE_INFO = dict(
    name="movie_nfo_generator",
    description="A simple tool to generate NFO files for Kodi.",
    long_description_content_type="text/markdown; charset=UTF-8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Multimedia",
    ],
    keywords="kodi nfo",
    author="J.Goutin",
    url="https://github.com/JGoutin/movie_nfo_generator",
    project_urls={"Download": "https://pypi.org/project/movie_nfo_generator"},
    license="GPLv3",
    zip_safe=True,
    python_requires=">=3.6",
    install_requires=[
        "lxml",
        "tmdbsimple",
        "requests"
    ],
    setup_requires=["setuptools"],
    entry_points={
        "console_scripts": [
            "movie_nfo_generator=movie_nfo_generator.__main__:_run_command"
        ]
    },
)

SETUP_DIR = abspath(dirname(__file__))

with open(join(SETUP_DIR, "movie_nfo_generator/__init__.py")) as file:
    for line in file:
        if line.rstrip().startswith("__version__"):
            PACKAGE_INFO["version"] = line.split("=", 1)[1].strip(" \"'\n")
            break

with open(join(SETUP_DIR, "readme.md")) as file:
    PACKAGE_INFO["long_description"] = file.read()

if __name__ == "__main__":
    from os import chdir
    from setuptools import setup, find_packages

    chdir(SETUP_DIR)
    setup(**PACKAGE_INFO, packages=find_packages())
