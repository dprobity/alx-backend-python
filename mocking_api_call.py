import requests
import unittest
from unittest.mock import patch

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None




class TestFetchData(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_data_success(self, mock_get):
        #   set up a mock response 
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"temp": "19C"}

        # call function under test

        result = fetch_data("http://example.com/api")

        self.assertEqual(result, {"temp": "19C"})
        mock_get.assert_called_once_with("http://example.com/api")



####    Mocking a Database call 
def get_user(db, user_id):
    return db.find_one("id": user_id)

import unittest
from unittest.mock import MagicMock

class TestGetUser(unittest.TestCase):
    def test_get_user_found(self):
        mock_db = MagicMock()
        mock_db.find_one.return_value = {"id": 1, "name": "Alice"}

        user = get_user(mock_db, 1)

        self.assertEqual(user, {"id": 1, "name": "Alice"})
        mock_db.find_one.assert_called_once_with({"id": 1})
 

