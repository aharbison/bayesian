import unittest

import pytest
import requests

import database

base_url = 'http://127.0.0.1:5000'

@pytest.fixture(autouse=True)
def setup_and_cleanup_database():
    database.create_tables()
    yield
    database.clear()


class TestCases(unittest.TestCase):
    def test_create_artist(self):
        url = base_url + '/artists'
        data = {'name': 'John Doe'}

        response = requests.post(url, json=data)
        self.assertEqual(200, response.status_code)
        response = response
        self.assertEqual({'message': 'Artist created successfully'}, response.json())

    def test_get_albums(self):
        url = base_url + '/albums'
        print(url)
        response = requests.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json()['albums'])

    def test_get_albums_with_params(self):
        url = base_url + '/albums'
        params = {'artist_id': 1, 'include_tracklist': True}
        response = requests.get(url, params=params)
        print(response.json())
        self.assertEqual(200, response.status_code)

    def test_create_album(self):
        url = base_url + '/albums'
        data = {'artist_id': 1, 'album': {'name': 'Album 1', 'release_date': '2023-01-01', 'price': 9.99}}
        response = requests.post(url, json=data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), {'message': 'Album created successfully'})


if __name__ == '__main__':
    unittest.main()
