import random
import string
import unittest

from h_cipher_tools import encrypt, decrypt, share, combine


class TestStringMethods(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)
        self.KEY = 'Password'
        self.PLAIN_TEXT = 'Clear Text Data'
        self.CIPHER_TEXT = '2071fb981465f2ea3524d993c31929116d4bd7023d2b8e8984563f9420036fe3'
        self.CIPHER_TEXT_WITH_IV = '1147d2539b3ba1acbd5a3a8e363b410b'
        self.IV = 'SG33FJ9RGRRGBLKI'
        self.SECRET_SHARE = [(2, '11f69217bf2a576f229e1599d41efa4e'), (4, 'd624d7f2b48ae5288cebc0fa6ee92947')]
        self.SECRET_COMBINED = 'SGQKFJ9RGMYGBLKI'

    def test_random_iv(self):
        cipher_text = encrypt(self.PLAIN_TEXT, self.KEY)
        self.assertNotEqual(cipher_text, self.CIPHER_TEXT, 'Random data generator is not reliable')

    def test_aes_flow(self):
        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        plain_text = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64))
        cipher_text = encrypt(plain_text, key)
        self.assertNotEqual(cipher_text, plain_text, 'Encryption not Successful')
        decrypted_plain_text = decrypt(cipher_text, key)
        self.assertEqual(plain_text, decrypted_plain_text, 'Decryption failed')

    def test_aes_decrypt(self):
        plain_text = decrypt(self.CIPHER_TEXT, self.KEY)
        self.assertEqual(self.PLAIN_TEXT, plain_text, 'Decryption failed for old data')

    def test_aes_decrypt_with_iv(self):
        cipher_text = encrypt(self.PLAIN_TEXT, self.KEY, iv=self.IV)
        self.assertEqual(self.CIPHER_TEXT_WITH_IV, cipher_text, 'Encryption failed with IV')
        plain_text = decrypt(self.CIPHER_TEXT_WITH_IV, self.KEY, iv=self.IV)
        self.assertEqual(self.PLAIN_TEXT, plain_text, 'Decryption failed for old data with IV')

    def test_aes_decrypt_fail(self):
        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        self.assertRaises(Exception, decrypt, self.CIPHER_TEXT, key)

    def test_shamir_share_flow(self):
        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        shares = share(key)
        shares.pop()
        shares.pop(2)
        shares.pop(1)
        combined = combine(shares)
        self.assertEqual(combined, key, 'Secret Reconstruction failed')

    def test_shamir_share_combine(self):
        combined = combine(self.SECRET_SHARE)
        self.assertEqual(combined, self.SECRET_COMBINED, 'Secret Reconstruction failed for old data')


if __name__ == '__main__':
    unittest.main()
