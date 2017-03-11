"""Utilities"""
from os.path import basename


def choose_result(results):
    """
    Search by title and return scraper ID

    Args:
        results (iterable of dict): Scrapper results.

    Returns:
        str: Scrapper media ID.
    """
    if not results:
        return None

    elif len(results) == 1:
        result = results[0]
        print(f'One matching result: {result["title"]} ({result["year"]})')
        return result["id"]

    else:
        print("Many matching results, choose one:")
        for i, result in enumerate(results):
            print(f'{i + 1:3d}: {result["title"]} ({result["year"]})')
        choices = tuple(results)
        while True:
            choice = input("Enter choice number: ").strip()
            try:
                choice = int(choice)
            except TypeError:
                continue
            if choice < 1 or choice > len(choices):
                continue
            return choices[choice - 1]["id"]


def choose_title(filename_title, scraper_title):
    """
    Choose a title.

    Args:
        filename_title (str): Filename title.
        scraper_title (str): Scrapper title.

    Returns:
        str: Selected title.
    """
    titles = [scraper_title]
    if filename_title != scraper_title:
        titles.append(filename_title)

    if len(titles) == 1:
        return titles[0]

    print("Available titles:")
    for i, title in enumerate(titles):
        print(f"{i + 1:3d}: {title}")

    while True:
        choice = input('Enter choice number, or "n" for new title: ').strip().lower()
        if choice == "n":
            break
        try:
            choice = int(choice)
        except TypeError:
            continue
        if choice < 1 or choice > len(titles):
            continue
        return titles[choice - 1]

    while True:
        title = input("Enter title: ").strip()
        if not title:
            continue
        return title


def filter_filename(filename, brackets=True, prefixed=False):
    """
    Return filtered filename.

    Args:
        filename (str): Filename.
        brackets (bool): True if contain brackets.
        prefixed (bool): True if prefixed file name.

    Returns:
        str: The filtered name.
    """
    filename = filename.strip(".")
    if brackets:
        filename = filename.split("(", 1)[0]
        filename = filename.split("[", 1)[0]
    if prefixed and "-" in filename:
        filename = filename.split("-", 1)[1]
    return filename.strip()


def filepath_to_titles(media_filepath, prefixed=False):
    """
    Long and short titles from filepath.

    Args:
        media_filepath (str): Media file path.
        prefixed (bool): True if prefixed file name.

    Returns:
        tuple: Short title, long title, year.
    """
    media_filename = basename(media_filepath)
    short_title = filter_filename(media_filename, True, prefixed)
    long_title = filter_filename(media_filename, False, prefixed)

    if "[" in long_title:
        title, suffix = long_title.split("[", 1)
        if "," in suffix:
            version, year = suffix.split(",", 1)
            long_title = f"{title.strip()} [{version.strip()}]"
            year = year.strip(" ]")
        else:
            long_title = title.strip()
            year = suffix.strip(" ]")
    else:
        year = ""
    return short_title, long_title, year


def filepath_to_episode_id(media_filepath, prefixed=False):
    """
    Episode name and number from filepath.

    Args:
        media_filepath (str): Episode file path.
        prefixed (bool): True if prefixed file name.

    Returns:
        tuple: Name, season number, episode number.
    """
    media_filename = basename(media_filepath)
    name = filter_filename(media_filename, False, prefixed)
    name, season_number = name.rsplit(".", 1)
    season, number = season_number.lower().strip("s").split("e")
    return name, int(season), int(number)
