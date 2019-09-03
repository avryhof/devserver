from bs4 import BeautifulSoup
import requests


def get_html(url):
    html = False
    try:
        resp = requests.get(url)
    except Exception:
        pass

    else:
        html = resp.text

    return html


def findlyrics(artist, song):
    searchUrl = "http://search.azlyrics.com/search.php?q=" + artist + "+" + song
    searchPage = get_html(searchUrl)

    if searchPage:
        searchSoup = BeautifulSoup(searchPage, "html.parser")

        lyricsFound = False

        # First Attempt - AZ Lyrics
        try:
            alltds = searchSoup.find_all("td")
            url = alltds[0].a["href"]  # Will invoke Index Error search results empty
            for td in alltds:
                if td.has_attr("class"):
                    url = td.a["href"]
                    break
            lyricsFound = True
        except IndexError:
            pass

    if lyricsFound:
        mainPage = get_html(url)
        if mainPage:
            soup = BeautifulSoup(mainPage, "html.parser")

            # Finding div that contains the div that contains the lyrics
            for div in soup.find_all("div"):
                if div.has_attr("class"):
                    if [u"col-xs-12", u"col-lg-8", u"text-center"] == div["class"]:
                        mainDiv = div
                        for div in mainDiv.find_all("div"):
                            if not div.has_attr("class"):
                                lyricsFound = div.text  # Returns Lyrics from AZLyrics
                        break

    return lyricsFound
