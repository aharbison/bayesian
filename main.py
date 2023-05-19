# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, jsonify, request
from models import Artist, Album
import database

app = Flask(__name__)


@app.route('/artists', methods=['POST'])
def create_artist():
    data = request.get_json()
    artist = Artist(data['name'])
    database.create_artist(artist)
    return jsonify({'message': 'Artist created successfully'})


@app.route('/albums', methods=['POST'])
def create_album():
    album_data = request.json.get('album')
    artist_id = request.json.get('artist_id')
    tracks = album_data.get('tracks')

    # Check if the artist exists
    artist = database.get_artist(artist_id)
    if not artist:
        return jsonify({'message': 'Artist not found'}), 404

    # Create the album
    album = {
        'name': album_data.get('name'),
        'release_date': album_data.get('release_date'),
        'price': album_data.get('price'),
        'artist_id': artist_id
    }
    album_id = database.add_album(album)

    if tracks:
        for track_data in tracks:
            track = {
                'title': track_data.get('title'),
                'duration': track_data.get('duration'),
                'album_id': album_id
            }
            database.add_track(track)

    return jsonify({'message': 'Album created successfully', 'album_id': album_id}), 200


@app.route('/artists', methods=['GET'])
def get_artists():
    artists = database.get_artists()
    return jsonify({'artists': artists})


@app.route('/albums', methods=['GET'])
def get_albums():
    artist_id = request.args.get('artist_id')
    include_tracklist = bool(request.args.get('include_tracklist'))
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    albums = database.get_albums(artist_id, include_tracklist, min_price, max_price)
    release_date = request.args.get('release_date')
    # Filter by release date if provided
    if release_date:
        albums = [album for album in albums if album['release_date'] == release_date]

    return jsonify({'albums': albums})


if __name__ == '__main__':
    database.create_tables()
    app.run()
