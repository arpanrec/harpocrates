import hashlib
from binascii import hexlify, unhexlify
import logging
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.SecretSharing import Shamir

logger = logging.getLogger(__name__)

__BLOCK_SIZE = AES.block_size
__AES_MODE = AES.MODE_CBC


def __pad(plain_text, block_size=__BLOCK_SIZE):
    number_of_bytes_to_pad = block_size - len(plain_text) % block_size
    ascii_string = chr(number_of_bytes_to_pad)
    padding_str = number_of_bytes_to_pad * ascii_string
    padded_plain_text = plain_text + padding_str
    return padded_plain_text


def __unpad(plain_text=None):
    last_character = plain_text[len(plain_text) - 1:]
    bytes_to_remove = ord(last_character)
    return plain_text[:-bytes_to_remove]


def __aes_key_transformation(key=None):
    return hashlib.sha256(key.encode()).digest()


def encrypt(simple: str, key: str, iv: str = None):
    """
    :param iv:
    :param simple: Plain Text Data type(str)
    :param key: AES Key type(str)
    :return: hexlify the encrypted bytes
    """
    if iv is None:
        iv_gen = Random.new().read(__BLOCK_SIZE)
    else:
        iv_gen = iv.encode('UTF-8')

    key_transformed = __aes_key_transformation(key)
    simple_padded = __pad(simple)
    simple_padded_encoded = simple_padded.encode('UTF-8')
    simple_padded_encoded_encrypted = encrypt_core(key_transformed, iv_gen, simple_padded_encoded)

    if iv is None:
        simple_padded_encoded_encrypted_iv = simple_padded_encoded_encrypted + iv_gen
    else:
        simple_padded_encoded_encrypted_iv = simple_padded_encoded_encrypted

    simple_padded_encoded_encrypted_iv_hexlify = hexlify(simple_padded_encoded_encrypted_iv)
    simple_padded_encoded_encrypted_iv_hexlify_decoded = simple_padded_encoded_encrypted_iv_hexlify.decode("utf-8")
    return simple_padded_encoded_encrypted_iv_hexlify_decoded


def encrypt_core(key_transformed: bytes, iv: bytes, simple_padded_encoded: bytes):
    """
    :param simple_padded_encoded: Unencrypted data in bytes
    :param iv: Initial Vector in bytes
    :param key_transformed: AES Encryption Key in bytes
    :return Encrypted Data
    :rtype bytes
    """
    cipher = AES.new(key_transformed, __AES_MODE, iv)
    simple_padded_encoded_encrypted = cipher.encrypt(simple_padded_encoded)
    return simple_padded_encoded_encrypted


def decrypt(simple_padded_encoded_encrypted_iv_hexlify_decoded, key, block_size=__BLOCK_SIZE, iv: str = None):
    key_transformed = __aes_key_transformation(key)
    simple_padded_encoded_encrypted_iv_hexlify = simple_padded_encoded_encrypted_iv_hexlify_decoded.encode('UTF-8')
    simple_padded_encoded_encrypted_iv = unhexlify(simple_padded_encoded_encrypted_iv_hexlify)

    if iv is None:
        simple_padded_encoded_encrypted = simple_padded_encoded_encrypted_iv[:len(simple_padded_encoded_encrypted_iv) - block_size]
        iv = simple_padded_encoded_encrypted_iv[len(simple_padded_encoded_encrypted_iv) - block_size:]
    else:
        simple_padded_encoded_encrypted = simple_padded_encoded_encrypted_iv
        iv = iv.encode('UTF-8')

    simple_padded_encoded = decrypt_core(key_transformed, iv, simple_padded_encoded_encrypted)
    simple_padded = simple_padded_encoded.decode()
    simple = __unpad(simple_padded)
    return simple


def decrypt_core(key_transformed: bytes, iv: bytes, simple_padded_encoded_encrypted: bytes):
    """
    :param simple_padded_encoded_encrypted: Encrypted Data in bytes
    :param iv: Initial Vector in bytes
    :param key_transformed: AES Encryption Key in bytes
    :return Encrypted Data
    :rtype bytes
    """
    cipher = AES.new(key_transformed, __AES_MODE, iv)
    simple_padded_encoded = cipher.decrypt(simple_padded_encoded_encrypted)
    return simple_padded_encoded


def share(plain_text: str, shares=2, original=5):
    base64encoded_string_list: list = []
    shares = Shamir.split(shares, original, plain_text.encode('UTF-8'), ssss=None)
    for idx, share_data in shares:
        base64encoded_string_list.append((idx, hexlify(share_data).decode('UTF-8')))
    return base64encoded_string_list


def combine(shares: list):
    base64decoded_string_list: list = []
    for idx, share_data in shares:
        base64decoded_string_list.append((idx, unhexlify(share_data.encode('UTF-8'))))
    plain_text = Shamir.combine(base64decoded_string_list, ssss=None)
    return plain_text.decode()


if __name__ == '__main__':
    ...
