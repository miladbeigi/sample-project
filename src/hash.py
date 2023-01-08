import hashlib
import constants


class Hash_File:

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.hash_value = self.hash_file(file_path)

    def hash_file(self, file_path: str):

        BUF_SIZE = constants.BUF_SIZE
        sha256 = hashlib.sha256()

        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha256.update(data)

        return sha256.hexdigest()

    def update_hash(self):
        self.hash_value = self.hash_file(self.file_path)
