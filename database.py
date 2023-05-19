import sqlite3
import os

DB_NAME = 'music_catalog.db'


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH = os.path.join(ROOT_DIR, 'schema.sql')
    with open(FILE_PATH, 'r') as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()


def clear():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Clear all tables
    cursor.execute('DELETE FROM tracks')
    cursor.execute('DELETE FROM albums')
    cursor.execute('DELETE FROM artists')

    conn.commit()
    conn.close()


def create_artist(artist):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO artists (name) VALUES (?)", (artist.name,))
    conn.commit()
    conn.close()


def create_album(album, artist_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO albums (name, release_date, price, artist_id) VALUES (?, ?, ?, ?)",
                   (album.name, album.release_date, album.price, artist_id))
    album_id = cursor.lastrowid
    for track in album.tracks:
        cursor.execute("INSERT INTO tracks (title, duration, album_id) VALUES (?, ?, ?)",
                       (track.title, track.duration, album_id))
    conn.commit()
    conn.close()


def get_artists():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM artists")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_artist(artist_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM artists WHERE id = ?', (artist_id,))
    artist = cursor.fetchone()

    conn.close()

    return artist


def get_albums(artist_id, include_tracklist=False, min_price=None, max_price=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query = "SELECT * FROM albums WHERE artist_id = ?"
    params = [artist_id]

    if min_price is not None:
        query += " AND price >= ?"
        params.append(min_price)

    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    if include_tracklist:
        albums = []
        for row in rows:
            album_id = row[0]
            cursor.execute("SELECT * FROM tracks WHERE album_id = ?", (album_id,))
            tracks = cursor.fetchall()
            album = row + (tracks,)
            albums.append(album)
        conn.close()
        return albums

    conn.close()
    return rows


def add_album(album):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO albums (name, release_date, price, artist_id) VALUES (?, ?, ?, ?)',
                   (album['name'], album['release_date'], album['price'], album['artist_id']))
    album_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return album_id


def add_track(track):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO tracks (title, duration, album_id) VALUES (?, ?, ?)',
                   (track['title'], track['duration'], track['album_id']))

    conn.commit()
    conn.close()
