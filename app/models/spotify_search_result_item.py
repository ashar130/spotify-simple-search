
class SpotifySearchResultItem():

    def __init__(self, name, weblink, image={}):
        self.name = name
        self.weblink = weblink
        self.image = image

    def __str__(self):
        return str(self.__dict__)


class Track(SpotifySearchResultItem):

    def __init__(self, name, weblink, image, artist, album, release_date):
        super().__init__(name, weblink, image)
        self.artist = artist
        self.album = album
        self.release_date = release_date


class Album(SpotifySearchResultItem):

    def __init__(self, name, weblink, image, artist, release_date):
        super().__init__(name, weblink, image)
        self.artist = artist
        self.release_date = release_date


class Artist(SpotifySearchResultItem):

    def __init__(self, name, weblink, image, genres, followers):
        super().__init__(name, weblink, image)
        self.genres = genres
        self.followers = followers
