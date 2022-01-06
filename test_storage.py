import unittest

from h_storage import FileStorage


class TestStringMethods(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.AES_KEY = {'key': 'Password', 'iv': 'SG33FJ9RGRRGBLKI'}
        self.ENDPOINT = 'storage'
        self.FILE_STORAGE = FileStorage(self.ENDPOINT, self.AES_KEY)

    def test_store(self):
        data = 'afjasfhaufhashfaskfjkasfh'
        is_value_added = self.FILE_STORAGE.put('street', 'house', 'room', 'seat', data)
        self.assertTrue(is_value_added, 'Data not stored')
        recovered = self.FILE_STORAGE.get('street', 'house', 'room', 'seat')
        self.assertEqual(recovered, data, 'Data retrieval failed')

    def test_delete(self):
        self.test_store()
        is_value_deleted = self.FILE_STORAGE.delete('street', 'house', 'room', 'seat')
        self.assertTrue(is_value_deleted, 'Data not deleted')
        recovered = self.FILE_STORAGE.get('street', 'house', 'room', 'seat')
        self.assertIsNone(recovered, 'Data not deleted properly')


if __name__ == '__main__':
    unittest.main()
