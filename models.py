class Artist:
    def __init__(self, name):
        self.name = name


class Album:
    def __init__(self, name, release_date, price, tracks=None):
        self.name = name
        self.release_date = release_date
        self.price = price
        self.tracks = tracks or []

