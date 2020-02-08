import base64
import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class AES256CBC(object):
    """
    实现AES256-CBC模式的加解密
    """

    def __init__(self, aes_key, iv):
        self._key = self.decode_base64(aes_key)
        self._iv = self.decode_base64(iv)

    def encode_base64(self, data: bytes) -> bytes:
        return base64.urlsafe_b64encode(data)

    def decode_base64(self, data: bytes) -> bytes:
        return base64.urlsafe_b64decode(data)

    @staticmethod
    def generate_key():
        return base64.urlsafe_b64encode(os.urandom(32))

    @staticmethod
    def generate_iv():
        return base64.urlsafe_b64encode(os.urandom(16))

    def encrypt(self, data: str) -> bytes:
        return self.encode_base64(self._cbc_encrypt(data))

    def decrypt(self, data: bytes) -> str:
        return self._cbc_decrypt(self.decode_base64(data))

    def _cbc_encrypt(self, data):
        if not isinstance(data, bytes):
            data = data.encode()

        cipher = Cipher(algorithms.AES(self._key),
                        modes.CBC(self._iv),
                        backend=default_backend())
        encryptor = cipher.encryptor()

        padded_data = encryptor.update(self._pkcs7_padding(data))

        return padded_data

    def _cbc_decrypt(self, data):
        if not isinstance(data, bytes):
            data = data.encode()

        cipher = Cipher(algorithms.AES(self._key),
                        modes.CBC(self._iv),
                        backend=default_backend())
        decryptor = cipher.decryptor()

        uppaded_data = self._pkcs7_unpadding(decryptor.update(data))

        uppaded_data = uppaded_data.decode()
        return uppaded_data

    def _pkcs7_padding(self, data):
        if not isinstance(data, bytes):
            data = data.encode()

        padder = padding.PKCS7(algorithms.AES.block_size).padder()

        padded_data = padder.update(data) + padder.finalize()

        return padded_data

    def _pkcs7_unpadding(self, padded_data):
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data)

        try:
            uppadded_data = data + unpadder.finalize()
        except ValueError:
            raise ValueError('无效的加密信息!')
        else:
            return uppadded_data


if __name__ == '__main__':
    key = AES256CBC.generate_key()
    iv = AES256CBC.generate_iv()
    f = AES256CBC(key, iv)
    data = f.encrypt("AES256-CBC")
    print(data)
    print(f.decrypt(data))
