import urllib.request


class ShortLink:

    def short_link(self, long_link):
        url = 'https://clck.ru/--?url={}'.format(long_link)
        try:
            return urllib.request.urlopen(url).read().decode(encoding="utf-8")
        except:
            return long_link
