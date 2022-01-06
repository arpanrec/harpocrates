import logging
from abc import ABC, abstractmethod
from pathlib import Path
import yaml
from h_cipher_tools import encrypt, decrypt
from h_exceptions import HarpocratesException

logger = logging.getLogger(__name__)


class StorageSolution(ABC):
    def __init__(self, endpoint, aes_key_and_iv):
        self.endpoint = endpoint
        self.__aes_key = aes_key_and_iv['key']
        self.__aes_iv = aes_key_and_iv['iv']

    def __enc(self, street, house, room, seat, identity=None):
        street_enc = None if street is None else encrypt(street, self.__aes_key, iv=self.__aes_iv)
        house_enc = None if house is None else encrypt(house, self.__aes_key, iv=self.__aes_iv)
        room_enc = None if room is None else encrypt(room, self.__aes_key, iv=self.__aes_iv)
        seat_enc = None if seat is None else encrypt(seat, self.__aes_key, iv=self.__aes_iv)
        identity_enc = None if identity is None else encrypt(identity, self.__aes_key, iv=self.__aes_iv)
        return street_enc, house_enc, room_enc, seat_enc, identity_enc

    def delete(self, street, house, room, seat):
        return self.put(street, house, room, seat, None)

    def put(self, street, house, room, seat, identity):
        street_enc, house_enc, room_enc, seat_enc, identity_enc = self.__enc(street, house, room, seat, identity)
        return self._abc_store(street_enc, house_enc, room_enc, seat_enc, identity_enc)

    @abstractmethod
    def _abc_store(self, street, house, room, seat, identity):
        ...

    def get(self, street, house, room, seat):
        street_enc, house_enc, room_enc, seat_enc, identity_enc = self.__enc(street, house, room, seat)
        encrypted_identity = self._abc_retrieve(street_enc, house_enc, room_enc, seat_enc)
        if encrypted_identity is not None:
            identity = decrypt(encrypted_identity, self.__aes_key, iv=self.__aes_iv)
            return identity

    @abstractmethod
    def _abc_retrieve(self, street, house, room, seat):
        ...


class FileStorage(StorageSolution, ABC):
    def __init__(self, endpoint, aes_key_and_iv):
        super().__init__(endpoint, aes_key_and_iv)
        self.root_dir = Path(self.endpoint).absolute()
        logger.info(f'Initializing File Storage {self.root_dir}')

    def _abc_store(self, street, house, room, seat, identity):
        directory = self.root_dir.joinpath(street, house)
        directory.mkdir(mode=511, parents=True, exist_ok=True)
        file = directory.joinpath(f'{room}.yaml')
        if file.is_dir():
            raise HarpocratesException(f'Storage Changed out of context {file}')
        if file.exists():
            with open(file, 'r+') as f:
                data = yaml.full_load(f)
                if identity is None and seat in data:
                    del data[seat]
                else:
                    data[seat] = identity
                f.seek(0)
                yaml.dump(data, f, indent=4)
                f.truncate()
                return True
        elif identity is not None and not file.exists():
            with open(file, 'w') as f:
                data = {seat: identity}
                yaml.dump(data, f, indent=4)
                return True
        elif identity is None and not file.exists():
            return True

    def _abc_retrieve(self, street, house, room, seat):
        file = self.root_dir.joinpath(street, house, f'{room}.yaml')
        if file.exists():
            with open(file, 'r') as f:
                data = yaml.full_load(f)
                if seat in data:
                    return data[seat]


if __name__ == '__main__':
    ...
